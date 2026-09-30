/**
 * Vista Grafo de la maqueta · lógica pura (sin DOM ni red): layout de bases y subgrupos anidados,
 * plegado, fusión de aristas, elección de lados y validación de una conexión. Los tamaños son los
 * de la maqueta (`Sn`/`Rs` en `om`): átomos de 210 de ancho en una pila de paso 82 dentro de un
 * subgrupo de 250, subgrupos en columnas de paso 270, bases separadas por 160.
 */
import { NO_GROUP, primaryGroup } from "../core/atom-graph";
import { GROUP_MODEL, groupGid } from "../core/atom-groups";
import { ATOM_MODEL, atomRelationTypes, inGroup, validRelationTypesBetween } from "../core/atoms";
import { baseOf, subgroupOf } from "../core/caso";
import type { Edge, RelationTypeSpec } from "../core/contract";
import type { MockAtom, MockRelation } from "./adapter";

export const NODE_W = 210;
export const ATOM_STEP = 82;
export const SUB_W = 250;
export const SUB_HEAD = 40;
export const SUB_PAD = 8;
export const COL_STEP = 270;
export const BASE_PAD = 20;
export const BASE_HEAD = 44;
export const CELL_GAP = 16;
export const BASE_GAP = 160;
/** Alto de un subgrupo con `n` átomos (`Rs` de la maqueta). */
export const subHeight = (n: number): number => SUB_HEAD + n * ATOM_STEP + SUB_PAD;

/** Tipo de relación con espacios en lugar de `_`: `consulta_por` -> `consulta por`. */
export const typeLabel = (name: string): string => name.replace(/_/g, " ");

/** Base (raíz) de un átomo: el 1er segmento de su primer tag; `NO_GROUP` si no tiene tags. */
export const groupOf = (atom: Pick<MockAtom, "tags">): string => primaryGroup(atom);

/** Tag del subgrupo de un átomo (`programa.asistente`), o `null` si va directo a la base. */
export function cellTagOf(atom: Pick<MockAtom, "tags">): string | null {
  const base = groupOf(atom);
  if (base === NO_GROUP) return null;
  const first = atom.tags.find((t) => baseOf(t) !== "") ?? "";
  const sub = subgroupOf(first);
  return sub ? `${base}.${sub}` : null;
}

/** Colores de fondo (`--region-*` de maqueta.css). Los nombres conocidos tienen el suyo; el resto rota. */
const REGION_CLASSES = ["infra", "riesgos", "equipo"] as const;
const KNOWN_REGIONS: Record<string, string> = { programa: "infra", infra: "infra", infraestructura: "infra", paciente: "riesgos", riesgos: "riesgos", equipo: "equipo" };
export const regionClass = (tag: string, index = 0): string | null => {
  if (tag === NO_GROUP) return null;
  return KNOWN_REGIONS[tag.toLowerCase()] ?? REGION_CLASSES[index % REGION_CLASSES.length]!;
};

export const groupNodeId = (tag: string): string => `g:${tag}`;
export const isGroupNodeId = (id: string): boolean => id.startsWith("g:");
export const tagOfNodeId = (id: string): string => id.slice(2);

// ---------------------------------------------------------------- layout

const TIPO_RANK: Record<string, number> = { prompt: 0, acta: 0, folleto: 1, mensaje: 2 };

/**
 * Orden de lectura de los átomos: por fuente (prompt, folleto, mensaje como la maqueta; el resto
 * detrás, en su orden) y, dentro de cada una, por posición en el texto. De él salen el orden de
 * las bases y de los subgrupos (primera aparición), que es el de la barra lateral.
 */
export function readingOrder(atoms: MockAtom[], fuentes: { gid: string; tipo: string }[]): MockAtom[] {
  const rank = (a: MockAtom): number => {
    const i = fuentes.findIndex((f) => f.gid === a.atom.source);
    if (i < 0) return 100;
    return TIPO_RANK[fuentes[i]!.tipo] ?? 3 + i;
  };
  return atoms
    .map((a, i) => [a, i] as const)
    .sort((x, y) => rank(x[0]) - rank(y[0]) || x[0].atom.start - y[0].atom.start || x[1] - y[1])
    .map(([a]) => a);
}

export interface CellBox {
  /** Tag completo del subgrupo (`programa.asistente`); `null` = átomos directos de la base (sin caja). */
  tag: string | null;
  /** Posición y alto dentro de la base. */
  x: number;
  y: number;
  h: number;
  atomIds: string[];
}

export interface BaseBox {
  /** Base (`programa`) o `NO_GROUP`. */
  tag: string;
  x: number;
  y: number;
  w: number;
  h: number;
  cells: CellBox[];
}

export interface AtomPlace {
  /** Nodo padre: `g:<subgrupo>` o, si va directo, `g:<base>`. */
  parent: string;
  base: string;
  /** Posición RELATIVA al padre. */
  x: number;
  y: number;
}

export interface GrafoLayout {
  bases: BaseBox[];
  atoms: Record<string, AtomPlace>;
}

/** Columnas de subgrupos de una base: 1, 2 (hasta 4 subgrupos) o 3. */
export const columnsFor = (n: number): number => (n <= 1 ? 1 : n <= 4 ? 2 : 3);

/**
 * Determinista. Bases en fila, en orden de primera aparición (`NO_GROUP` al final); dentro de cada
 * una, los subgrupos (también por primera aparición; los átomos directos primero) se reparten en
 * 1-3 columnas en tandas consecutivas, las más largas a la derecha (5 -> 1+2+2, 4 -> 2+2), y se
 * apilan con 16 de separación. Con 30 átomos de Levira: Programa 830x?, Paciente 560x?.
 */
export function computeLayout(atoms: MockAtom[]): GrafoLayout {
  const bases: string[] = [];
  const cellsOf = new Map<string, Map<string | null, string[]>>();
  const at = (a: MockAtom) => {
    const base = groupOf(a);
    if (!cellsOf.has(base)) {
      cellsOf.set(base, new Map());
      bases.push(base);
    }
    const cells = cellsOf.get(base)!;
    const key = cellTagOf(a);
    cells.set(key, [...(cells.get(key) ?? []), a.id]);
  };
  atoms.forEach(at);
  bases.sort((a, b) => (a === NO_GROUP ? 1 : b === NO_GROUP ? -1 : 0));

  const layout: GrafoLayout = { bases: [], atoms: {} };
  let x = 0;
  for (const base of bases) {
    const map = cellsOf.get(base)!;
    const keys = [...map.keys()].sort((a, b) => (a === null ? -1 : b === null ? 1 : 0));
    const cols = columnsFor(keys.length);
    const per = Math.floor(keys.length / cols);
    const extra = keys.length % cols;
    const cells: CellBox[] = [];
    let k = 0;
    for (let c = 0; c < cols; c++) {
      const take = per + (c >= cols - extra ? 1 : 0);
      let y = BASE_HEAD;
      for (let j = 0; j < take; j++, k++) {
        const tag = keys[k]!;
        const ids = map.get(tag)!;
        const head = tag === null ? 0 : SUB_HEAD;
        const h = head + ids.length * ATOM_STEP + SUB_PAD;
        cells.push({ tag, x: BASE_PAD + c * COL_STEP, y, h, atomIds: ids });
        y += h + CELL_GAP;
      }
    }
    const w = BASE_PAD + cols * COL_STEP;
    const h = Math.max(0, ...cells.map((c) => c.y + c.h)) + BASE_PAD;
    layout.bases.push({ tag: base, x, y: 0, w, h, cells });
    for (const cell of cells) {
      cell.atomIds.forEach((id, i) => {
        layout.atoms[id] =
          cell.tag === null
            ? { parent: groupNodeId(base), base, x: cell.x + BASE_PAD, y: cell.y + i * ATOM_STEP }
            : { parent: groupNodeId(cell.tag), base, x: BASE_PAD, y: SUB_HEAD + i * ATOM_STEP };
      });
    }
    x += w + BASE_GAP;
  }
  return layout;
}

/** Posición de una base plegada (un nodo de 210 centrado arriba de su región). */
export const foldedBasePosition = (b: BaseBox): { x: number; y: number } => ({ x: b.x + b.w / 2 - 105, y: b.y + 40 });
/** Posición de un subgrupo plegado, relativa a su base. */
export const foldedCellPosition = (c: CellBox): { x: number; y: number } => ({ x: c.x + 20, y: c.y + 4 });

/** Caja y celda de un subgrupo por su tag. */
export function findCell(layout: GrafoLayout, tag: string): { base: BaseBox; cell: CellBox } | null {
  for (const base of layout.bases) {
    const cell = base.cells.find((c) => c.tag === tag);
    if (cell) return { base, cell };
  }
  return null;
}

/** Centro de un nodo (átomo, subgrupo o base) en coordenadas del lienzo, para elegir lados. */
export function nodeCenter(id: string, layout: GrafoLayout, folded: ReadonlySet<string>): [number, number] | null {
  if (isGroupNodeId(id)) {
    const tag = tagOfNodeId(id);
    const b = layout.bases.find((x) => x.tag === tag);
    if (b) return folded.has(tag) ? [b.x + b.w / 2, b.y + 85] : [b.x + b.w / 2, b.y + b.h / 2];
    const f = findCell(layout, tag);
    return f ? [f.base.x + f.cell.x + 125, f.base.y + f.cell.y + (folded.has(tag) ? 50 : f.cell.h / 2)] : null;
  }
  const p = layout.atoms[id];
  const b = p && layout.bases.find((x) => x.tag === p.base);
  if (!p || !b) return null;
  if (p.parent === groupNodeId(p.base)) return [b.x + p.x + NODE_W / 2, b.y + p.y + 32];
  const cell = b.cells.find((c) => c.tag !== null && groupNodeId(c.tag) === p.parent)!;
  return [b.x + cell.x + p.x + NODE_W / 2, b.y + cell.y + p.y + 32];
}

/** Lados `[origen, destino]` (`r|l|b|t`) según la posición relativa de los centros. */
export function edgeSides(a: [number, number], b: [number, number]): [string, string] {
  const dx = b[0] - a[0];
  const dy = b[1] - a[1];
  if (Math.abs(dx) / 2.2 > Math.abs(dy)) return dx > 0 ? ["r", "l"] : ["l", "r"];
  return dy > 0 ? ["b", "t"] : ["t", "b"];
}

// ---------------------------------------------------------------- aristas

/** Relación con los extremos-grupo ya repartidos entre los átomos del grupo. */
export interface FlatRelation {
  rel: MockRelation;
  source: string;
  target: string;
  inherited: boolean;
}

/**
 * Las relaciones sobre un grupo (`g:<tag>`, cualquier nivel) las hereda cada átomo del grupo:
 * una arista punteada por átomo. Se omite entre dos grupos, consigo mismo y cuando ya existe la
 * directa (mismo par y tipo).
 */
export function expandRelations(relations: MockRelation[], atoms: MockAtom[]): FlatRelation[] {
  const members = (id: string): string[] => (isGroupNodeId(id) ? atoms.filter((a) => inGroup(a, tagOfNodeId(id))).map((a) => a.id) : [id]);
  const known = new Set(atoms.map((a) => a.id));
  const direct = new Set<string>();
  const out: FlatRelation[] = [];
  for (const rel of relations) {
    if (isGroupNodeId(rel.source) && isGroupNodeId(rel.target)) continue;
    const inherited = isGroupNodeId(rel.source) || isGroupNodeId(rel.target);
    if (!inherited && (!known.has(rel.source) || !known.has(rel.target))) continue;
    for (const s of members(rel.source)) {
      for (const t of members(rel.target)) {
        if (s === t || !known.has(s) || !known.has(t)) continue;
        if (!inherited) direct.add(`${s}|${t}|${rel.type}`);
        out.push({ rel, source: s, target: t, inherited });
      }
    }
  }
  return out.filter((f) => !f.inherited || !direct.has(`${f.source}|${f.target}|${f.rel.type}`));
}

export interface FusedEdge {
  key: string;
  source: string;
  target: string;
  list: MockRelation[];
  inherited: boolean;
  /** Une dos bases distintas (la maqueta la pinta azul). */
  crossBase: boolean;
}

/**
 * Aristas dibujables: descarta los tipos ocultos, lleva cada extremo a la base o al subgrupo
 * plegado que lo contiene (`g:<tag>`; la base gana), suprime las que quedan dentro de un mismo
 * nodo y fusiona las paralelas.
 */
export function fuseEdges(
  flat: FlatRelation[],
  atoms: MockAtom[],
  folded: ReadonlySet<string>,
  hiddenTypes: readonly string[],
): FusedEdge[] {
  const info = new Map(atoms.map((a) => [a.id, { base: groupOf(a), cell: cellTagOf(a) }]));
  const nodeOf = (id: string) => {
    const i = info.get(id);
    if (!i) return id;
    if (folded.has(i.base)) return groupNodeId(i.base);
    return i.cell !== null && folded.has(i.cell) ? groupNodeId(i.cell) : id;
  };
  const baseOfNode = (id: string) => (isGroupNodeId(id) ? tagOfNodeId(id).split(".")[0]! : (info.get(id)?.base ?? ""));
  const acc = new Map<string, FusedEdge>();
  for (const f of flat) {
    if (hiddenTypes.includes(f.rel.type)) continue;
    const s = nodeOf(f.source);
    const t = nodeOf(f.target);
    if (s === t) continue;
    const key = `${s}->${t}${f.inherited ? ":inh" : ""}`;
    const cur = acc.get(key) ?? { key, source: s, target: t, list: [], inherited: f.inherited, crossBase: baseOfNode(s) !== baseOfNode(t) };
    if (!cur.list.some((r) => r.id === f.rel.id)) cur.list.push(f.rel);
    acc.set(key, cur);
  }
  return [...acc.values()];
}

/** Relaciones que tocan al átomo: directas o sobre un grupo al que pertenece. */
export function relationsOfAtom(atom: MockAtom, relations: MockRelation[]): MockRelation[] {
  const hits = (end: string) => end === atom.id || (isGroupNodeId(end) && inGroup(atom, tagOfNodeId(end)));
  return relations.filter((r) => hits(r.source) || hits(r.target));
}

// ---------------------------------------------------------------- conexión

export interface ConnectEnd {
  gid: string;
  label: string;
  model: string;
  /** Solo en un grupo o base: su tag (`programa`, `programa.red`), para crear el `GrupoDoc` si falta. */
  tag?: string;
}

export type ConnectPlan =
  | { ok: true; source: ConnectEnd; target: ConnectEnd; type: RelationTypeSpec }
  | { ok: false; message: string };

export interface ConnectInput {
  sourceId: string;
  targetId: string;
  typeName: string;
  atoms: MockAtom[];
  types: RelationTypeSpec[];
  edges: Edge[];
  groupLabel(tag: string): string;
}

function endOf(id: string, atoms: MockAtom[], groupLabel: (tag: string) => string): ConnectEnd | { error: string } {
  if (isGroupNodeId(id)) {
    const tag = tagOfNodeId(id);
    if (tag === NO_GROUP) return { error: "«Sin grupo» no es un grupo real: no admite relaciones." };
    return { gid: groupGid(tag), label: `${tag.includes(".") ? "Grupo" : "Base"} ${groupLabel(tag)}`, model: GROUP_MODEL, tag };
  }
  const atom = atoms.find((a) => a.id === id);
  return atom ? { gid: atom.atom.gid, label: atom.text, model: ATOM_MODEL } : { error: "El nodo ya no existe." };
}

/** ¿Se puede crear `typeName` entre los dos nodos? Si no, dice por qué (mensaje para el aviso). */
export function planConnection(input: ConnectInput): ConnectPlan {
  const s = endOf(input.sourceId, input.atoms, input.groupLabel);
  const t = endOf(input.targetId, input.atoms, input.groupLabel);
  if ("error" in s) return { ok: false, message: s.error };
  if ("error" in t) return { ok: false, message: t.error };
  if (s.gid === t.gid) return { ok: false, message: "Un nodo no se relaciona consigo mismo." };
  if (s.model === GROUP_MODEL && t.model === GROUP_MODEL) return { ok: false, message: "No se relaciona un grupo con otro grupo: suelta sobre un átomo." };
  const valid = validRelationTypesBetween(input.types, s, t, input.edges);
  const type = valid.find((v) => v.name === input.typeName);
  if (type) return { ok: true, source: s, target: t, type };
  const exists = input.edges.some((e) => e.type === input.typeName && e.source === s.gid && e.target === t.gid);
  if (exists) return { ok: false, message: `Ya existe «${typeLabel(input.typeName)}» de ${clip(s.label)} a ${clip(t.label)}.` };
  const spec = atomRelationTypes(input.types).find((x) => x.name === input.typeName);
  const groupEnd = [s, t].find((e) => e.model === GROUP_MODEL && spec && !endAdmits(spec, e, s === e ? "source" : "target"));
  if (spec && groupEnd) {
    const withGroup = valid.map((v) => typeLabel(v.name)).join(", ");
    return { ok: false, message: `«${typeLabel(input.typeName)}» no admite un grupo o una base como extremo (${clip(groupEnd.label)}).${withGroup ? ` Con grupos sirven: ${withGroup}.` : ""}` };
  }
  const hint = valid.length ? ` Entre estos nodos sirven: ${valid.map((v) => typeLabel(v.name)).join(", ")}.` : "";
  return { ok: false, message: `«${typeLabel(input.typeName)}» no es válido entre ${clip(s.label)} y ${clip(t.label)}.${hint}` };
}

const endAdmits = (spec: RelationTypeSpec, end: ConnectEnd, side: "source" | "target"): boolean => {
  const list = side === "source" ? spec.source_types : spec.target_types;
  return list.length === 0 || list.includes(end.model);
};

const clip = (s: string, n = 32) => (s.length > n ? `${s.slice(0, n - 1)}…` : s);

/** Tipos de relación de los átomos (nombres), en el orden del store. */
export const relationTypeNames = (types: RelationTypeSpec[]): string[] => atomRelationTypes(types).map((t) => t.name);
