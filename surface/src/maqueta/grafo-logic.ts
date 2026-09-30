/**
 * Vista Grafo de la maqueta · lógica pura (sin DOM ni red): layout de regiones, plegado, fusión de
 * aristas, elección de lados y validación de una conexión. Los tamaños son los de la maqueta
 * (`Xa`): átomos de 210 de ancho en rejilla de paso 90, regiones a 500/240 de ancho.
 */
import { NO_GROUP, primaryGroup } from "../core/atom-graph";
import { GROUP_MODEL, groupGid } from "../core/atom-groups";
import { ATOM_MODEL, atomRelationTypes, inGroup, validRelationTypesBetween } from "../core/atoms";
import type { Edge, RelationTypeSpec } from "../core/contract";
import type { MockAtom, MockRelation } from "./adapter";

export const NODE_W = 210;
export const NODE_STEP = 90;
export const REGION_PAD = 20;
export const REGION_HEAD = 50;
export const COL_GAP = 60;
export const REGION_GAP = 40;
/** Centro del átomo respecto de su esquina (ancho 210, alto ~64). */
export const NODE_CENTER: [number, number] = [105, 32];

export const KIND_LABEL: Record<string, string> = { entidad: "Entidad", hecho: "Hecho", decision: "Decisión", pendiente: "Pendiente", riesgo: "Riesgo" };

export const capitalize = (s: string): string => (s ? s.charAt(0).toUpperCase() + s.slice(1) : s);

/** Grupo (raíz) de un átomo: el primer segmento de su primer tag; `NO_GROUP` si no tiene tags. */
export const groupOf = (atom: Pick<MockAtom, "tags">): string => primaryGroup(atom);

/** Regiones con color propio en la maqueta; el resto usa el neutro de grafo.css. */
const KNOWN_REGIONS: Record<string, string> = { infra: "infra", infraestructura: "infra", equipo: "equipo", riesgos: "riesgos" };
export const regionClass = (tag: string): string | null => KNOWN_REGIONS[tag.toLowerCase()] ?? null;

export const groupNodeId = (tag: string): string => `g:${tag}`;
export const isGroupNodeId = (id: string): boolean => id.startsWith("g:");
export const tagOfNodeId = (id: string): string => id.slice(2);

// ---------------------------------------------------------------- layout

export interface RegionBox {
  /** Grupo raíz (`infra`, o `NO_GROUP`). */
  tag: string;
  x: number;
  y: number;
  w: number;
  h: number;
}

export interface GrafoLayout {
  regions: RegionBox[];
  /** Posición del átomo RELATIVA a su región. */
  atoms: Record<string, { tag: string; x: number; y: number }>;
}

const columnsFor = (n: number) => (n <= 4 ? 1 : n <= 12 ? 2 : 3);

/**
 * Determinista: regiones ordenadas por tamaño (y nombre) y repartidas en dos columnas, cada una
 * bajo la que tenga menos alto; átomos en rejilla de fila mayor dentro de la región.
 */
export function computeLayout(atoms: MockAtom[]): GrafoLayout {
  const byGroup = new Map<string, MockAtom[]>();
  for (const a of atoms) {
    const g = groupOf(a);
    byGroup.set(g, [...(byGroup.get(g) ?? []), a]);
  }
  const sized = [...byGroup.entries()]
    .map(([tag, list]) => {
      const cols = columnsFor(list.length);
      const rows = Math.ceil(list.length / cols);
      // Ancho 240 con una columna y 500 con dos, como en la maqueta.
      return { tag, list, cols, w: cols * (NODE_W + 30 + REGION_PAD) - REGION_PAD, h: REGION_HEAD + rows * NODE_STEP };
    })
    .sort((a, b) => b.list.length - a.list.length || a.tag.localeCompare(b.tag));

  const bottoms = [0, 0];
  const placed: { col: number; y: number; item: (typeof sized)[number] }[] = [];
  for (const item of sized) {
    const col = bottoms[1]! < bottoms[0]! ? 1 : 0;
    const y = bottoms[col]! > 0 ? bottoms[col]! + REGION_GAP : 0;
    bottoms[col] = y + item.h;
    placed.push({ col, y, item });
  }
  const col0W = Math.max(0, ...placed.filter((p) => p.col === 0).map((p) => p.item.w));
  const colX = [0, col0W + COL_GAP];

  const layout: GrafoLayout = { regions: [], atoms: {} };
  for (const { col, y, item } of placed) {
    layout.regions.push({ tag: item.tag, x: colX[col]!, y, w: item.w, h: item.h });
    item.list.forEach((a, i) => {
      layout.atoms[a.id] = {
        tag: item.tag,
        x: REGION_PAD + (i % item.cols) * (NODE_W + 30),
        y: REGION_HEAD + Math.floor(i / item.cols) * NODE_STEP,
      };
    });
  }
  return layout;
}

/** Posición de un grupo plegado (un nodo de 200 de ancho centrado arriba de su región). */
export const foldedPosition = (r: RegionBox): { x: number; y: number } => ({ x: r.x + r.w / 2 - 100, y: r.y + 40 });

/** Centro de un nodo (átomo o grupo plegado) en coordenadas del lienzo, para elegir lados. */
export function nodeCenter(id: string, layout: GrafoLayout, folded: ReadonlySet<string>): [number, number] | null {
  if (isGroupNodeId(id)) {
    const r = layout.regions.find((x) => x.tag === tagOfNodeId(id));
    if (!r) return null;
    return folded.has(r.tag) ? [r.x + r.w / 2, r.y + 85] : [r.x + r.w / 2, r.y + r.h / 2];
  }
  const p = layout.atoms[id];
  const r = p && layout.regions.find((x) => x.tag === p.tag);
  return p && r ? [r.x + p.x + NODE_CENTER[0], r.y + p.y + NODE_CENTER[1]] : null;
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
}

/**
 * Aristas dibujables: descarta los tipos ocultos, lleva cada extremo al grupo plegado que lo
 * contiene (`g:<raíz>`), suprime las que quedan dentro de un mismo nodo y fusiona las paralelas.
 */
export function fuseEdges(
  flat: FlatRelation[],
  atoms: MockAtom[],
  folded: ReadonlySet<string>,
  hiddenTypes: readonly string[],
): FusedEdge[] {
  const rootOf = new Map(atoms.map((a) => [a.id, groupOf(a)]));
  const nodeOf = (id: string) => {
    const root = rootOf.get(id);
    return root !== undefined && folded.has(root) ? groupNodeId(root) : id;
  };
  const acc = new Map<string, FusedEdge>();
  for (const f of flat) {
    if (hiddenTypes.includes(f.rel.type)) continue;
    const s = nodeOf(f.source);
    const t = nodeOf(f.target);
    if (s === t) continue;
    const key = `${s}->${t}${f.inherited ? ":inh" : ""}`;
    const cur = acc.get(key) ?? { key, source: s, target: t, list: [], inherited: f.inherited };
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
  /** Solo en un grupo: su tag raíz (para crear el `GrupoDoc` si falta). */
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
    return { gid: groupGid(tag), label: `Grupo ${groupLabel(tag)}`, model: GROUP_MODEL, tag };
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
  if (exists) return { ok: false, message: `Ya existe «${input.typeName}» de ${clip(s.label)} a ${clip(t.label)}.` };
  const hint = valid.length ? ` Entre estos nodos sirven: ${valid.map((v) => v.name).join(", ")}.` : "";
  return { ok: false, message: `«${input.typeName}» no es válido entre ${clip(s.label)} y ${clip(t.label)}.${hint}` };
}

const clip = (s: string, n = 32) => (s.length > n ? `${s.slice(0, n - 1)}…` : s);

/** Tipos de relación de los átomos (nombres), en el orden del store. */
export const relationTypeNames = (types: RelationTypeSpec[]): string[] => atomRelationTypes(types).map((t) => t.name);
