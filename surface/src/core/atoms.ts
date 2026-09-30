/**
 * ÁTOMOS · lógica pura de las vistas de átomos (OPERACIONALIZACION-VISTAS.md).
 *
 * Un átomo es un documento `AtomDoc` anclado a un tramo del campo `body` de un `ActaDoc`.
 * Nada acá toca DOM ni red: recibe documentos/aristas ya leídos y devuelve valores nuevos.
 *
 * Identidad: `Atom.id` es el id de documento (`a3`, el de `/document` y `/save`);
 * `Atom.gid` es `AtomDoc:a3`, el que usan las aristas. Las listas de un informe (slots,
 * pins, excluidos) guardan RUTAS de átomo (`Atom.path`, p. ej. `docs/atoms/a3.md`).
 */
import type {
  Acta,
  AnchorState,
  Atom,
  AtomKind,
  AtomStatus,
  Edge,
  GraphDocument,
  Informe,
  InformeSlot,
  Payload,
  RelationTypeSpec,
  SlotMode,
  SlotName,
} from "./contract";

export const ATOM_MODEL = "AtomDoc";
export const ATOM_KINDS: AtomKind[] = ["entidad", "hecho", "decision", "pendiente", "riesgo"];
export const ATOM_STATUSES: AtomStatus[] = ["propuesto", "confirmado", "descartado"];
export const SLOT_NAMES: SlotName[] = ["resumen", "decisiones", "riesgos", "pendientes"];
export const SLOT_MODES: SlotMode[] = ["viñetas", "prosa", "tabla"];
/** Largo máximo del `text` de un átomo creado desde una selección. */
export const ATOM_TEXT_MAX = 80;

const str = (v: unknown, fallback = ""): string => (typeof v === "string" ? v : fallback);
const num = (v: unknown, fallback = 0): number => (typeof v === "number" && Number.isFinite(v) ? v : fallback);
const strings = (v: unknown): string[] => (Array.isArray(v) ? v.filter((x): x is string => typeof x === "string") : []);

// ---------------------------------------------------------------- lectura de documentos

/** Convierte los `AtomDoc` de `/graph`. Valores fuera de enum caen a `hecho` / `propuesto`. */
export function atomsFromDocuments(docs: GraphDocument[]): Atom[] {
  return docs
    .filter((d) => d.model_name === ATOM_MODEL)
    .map((d) => {
      const p = d.payload;
      const kind = ATOM_KINDS.includes(p.kind as AtomKind) ? (p.kind as AtomKind) : "hecho";
      const status = ATOM_STATUSES.includes(p.status as AtomStatus) ? (p.status as AtomStatus) : "propuesto";
      return {
        id: d.id,
        gid: `${ATOM_MODEL}:${d.id}`,
        path: d.path,
        version: d.version,
        kind,
        status,
        source: str(p.source),
        source_field: str(p.source_field, "body"),
        start: num(p.start),
        end: num(p.end),
        tags: strings(p.tags),
        text: str(p.text),
        quote: str(p.quote),
        conf: num(p.conf, 1),
      };
    });
}

export function relationTypesFromDocuments(docs: GraphDocument[]): RelationTypeSpec[] {
  return docs
    .filter((d) => d.model_name === "RelationTypeDoc")
    .map((d) => ({
      id: d.id,
      name: str(d.payload.name, d.id),
      source_types: strings(d.payload.source_types),
      target_types: strings(d.payload.target_types),
      cardinality: str(d.payload.cardinality),
      description: str(d.payload.description),
    }));
}

export function actasFromDocuments(docs: GraphDocument[]): Acta[] {
  return docs
    .filter((d) => d.model_name === "ActaDoc")
    .map((d) => ({
      id: d.id,
      gid: `ActaDoc:${d.id}`,
      path: d.path,
      version: d.version,
      title: str(d.payload.title, d.id),
      body: str(d.payload.body),
    }));
}

export function slotFromPayload(payload: Payload, slot: SlotName): InformeSlot {
  const modo = payload[`${slot}_modo`];
  return {
    atomos: strings(payload[slot]),
    query: str(payload[`${slot}_query`]),
    pins: strings(payload[`${slot}_pins`]),
    excluidos: strings(payload[`${slot}_excluidos`]),
    modo: SLOT_MODES.includes(modo as SlotMode) ? (modo as SlotMode) : "viñetas",
  };
}

export function informesFromDocuments(docs: GraphDocument[]): Informe[] {
  return docs
    .filter((d) => d.model_name === "InformeAvanceDoc")
    .map((d) => ({
      id: d.id,
      path: d.path,
      version: d.version,
      payload: d.payload,
      slots: Object.fromEntries(SLOT_NAMES.map((s) => [s, slotFromPayload(d.payload, s)])) as Informe["slots"],
    }));
}

// ---------------------------------------------------------------- ancla

export interface AnchorCheck {
  state: AnchorState;
  /** Solo en `drifted`: índice donde la cita está ahora (la ocurrencia más cercana a `start`). */
  movedTo?: number;
}

/** El ancla se calcula contra el texto actual del campo; nunca se guarda. */
export function anchorState(body: string, atom: Pick<Atom, "start" | "end" | "quote">): AnchorCheck {
  const { quote } = atom;
  if (!quote) return { state: "orphan" };
  if (body.slice(atom.start, atom.end) === quote) return { state: "intact" };
  let best = -1;
  let from = body.indexOf(quote);
  while (from !== -1) {
    if (best === -1 || Math.abs(from - atom.start) < Math.abs(best - atom.start)) best = from;
    from = body.indexOf(quote, from + 1);
  }
  return best === -1 ? { state: "orphan" } : { state: "drifted", movedTo: best };
}

/** Offsets nuevos para un ancla `drifted`; `null` si no hay nada que reparar (intacta u huérfana). */
export function repairAnchor(body: string, atom: Pick<Atom, "start" | "end" | "quote">): { start: number; end: number } | null {
  const check = anchorState(body, atom);
  if (check.state !== "drifted" || check.movedTo === undefined) return null;
  return { start: check.movedTo, end: check.movedTo + atom.quote.length };
}

// ---------------------------------------------------------------- grupos

export interface GroupNode {
  /** Ruta completa del grupo: `infra.ingesta`. */
  id: string;
  /** Último segmento: `ingesta`. */
  name: string;
  /** Átomos distintos en este grupo o en cualquier subgrupo. */
  count: number;
  /** Ids de los átomos cuyo tag es exactamente este grupo. */
  atomIds: string[];
  children: GroupNode[];
}

/** Árbol de grupos por tags con puntos. Un átomo con varios tags cuenta en cada rama. */
export function groupTree(atoms: Atom[]): GroupNode[] {
  interface Build extends GroupNode {
    all: Set<string>;
    kids: Map<string, Build>;
  }
  const roots = new Map<string, Build>();
  for (const atom of atoms) {
    for (const tag of atom.tags) {
      const parts = tag.split(".").filter(Boolean);
      let level = roots;
      let id = "";
      parts.forEach((part, i) => {
        id = id ? `${id}.${part}` : part;
        let node = level.get(part);
        if (!node) {
          node = { id, name: part, count: 0, atomIds: [], children: [], all: new Set(), kids: new Map() };
          level.set(part, node);
        }
        node.all.add(atom.id);
        if (i === parts.length - 1 && !node.atomIds.includes(atom.id)) node.atomIds.push(atom.id);
        level = node.kids;
      });
    }
  }
  const finish = (level: Map<string, Build>): GroupNode[] =>
    [...level.values()]
      .sort((a, b) => a.name.localeCompare(b.name))
      .map((n) => ({ id: n.id, name: n.name, count: n.all.size, atomIds: n.atomIds, children: finish(n.kids) }));
  return finish(roots);
}

/** ¿El átomo pertenece al grupo `group` (él mismo o un subgrupo)? */
export function inGroup(atom: Pick<Atom, "tags">, group: string): boolean {
  return atom.tags.some((t) => t === group || t.startsWith(`${group}.`));
}

// ---------------------------------------------------------------- relaciones

const admits = (types: string[], model: string) => types.length === 0 || types.includes(model);

/**
 * Tipos de relación propios de los átomos: los que nombran `AtomDoc` de forma explícita en
 * ambos extremos. Los 13 tipos estructurales del índice (`has_model`, `references`…) también
 * son `RelationTypeDoc`, pero traen extremos vacíos u otras clases y no se ofrecen ni filtran.
 */
export function atomRelationTypes(types: RelationTypeSpec[]): RelationTypeSpec[] {
  return types.filter((t) => t.source_types.includes(ATOM_MODEL) && t.target_types.includes(ATOM_MODEL));
}

/**
 * Tipos de relación ofrecibles al arrastrar `sourceAtom` → `targetAtom`: los tipos de átomo
 * (`atomRelationTypes`) que admiten `AtomDoc` en ambos extremos y para los que no existe ya la
 * misma arista en `edges`. Un átomo no se relaciona consigo mismo.
 */
export function validRelationTypes(types: RelationTypeSpec[], sourceAtom: Atom, targetAtom: Atom, edges: Edge[] = []): RelationTypeSpec[] {
  if (sourceAtom.gid === targetAtom.gid) return [];
  return atomRelationTypes(types).filter(
    (t) =>
      admits(t.source_types, ATOM_MODEL) &&
      admits(t.target_types, ATOM_MODEL) &&
      !edges.some((e) => e.type === t.name && e.source === sourceAtom.gid && e.target === targetAtom.gid),
  );
}

export interface InheritedEdge {
  /** Arista original, la del grupo. */
  edge: Edge;
  /** Átomo miembro que la hereda. */
  atomId: string;
  atomGid: string;
  /** Grupo del que viene. */
  via: string;
  /** Extremos con el grupo sustituido por el átomo: `Model:name`. */
  source: string;
  target: string;
  /** Siempre `true`: se calcula, no se guarda. */
  inherited: true;
}

/** Cómo puede nombrar una arista al grupo `tag` en sus extremos. */
export function groupEndpoints(tag: string): string[] {
  return [tag, `tag:${tag}`, `Group:${tag}`, `semantic_tag/${tag}`, `sldb://semantic_tag/${tag}`];
}

/**
 * Aristas heredadas: las que tocan al grupo `groupId` (tag con puntos) se proyectan sobre cada
 * átomo miembro (incluidos subgrupos). Si ambos extremos son grupos/miembros, se omite la
 * arista para no inventar producto cartesiano: solo se hereda cuando el otro extremo es fijo.
 */
export function inheritedEdges(edges: Edge[], groupId: string, atoms: Atom[]): InheritedEdge[] {
  const ends = groupEndpoints(groupId);
  const members = atoms.filter((a) => inGroup(a, groupId));
  const out: InheritedEdge[] = [];
  for (const edge of edges) {
    const srcIs = ends.includes(edge.source);
    const tgtIs = ends.includes(edge.target);
    if (srcIs === tgtIs) continue;
    for (const atom of members) {
      out.push({
        edge,
        atomId: atom.id,
        atomGid: atom.gid,
        via: groupId,
        source: srcIs ? atom.gid : edge.source,
        target: tgtIs ? atom.gid : edge.target,
        inherited: true,
      });
    }
  }
  return out;
}

// ---------------------------------------------------------------- slots de informe (§4)

/** Resultado de Actualizar: nada entra a la lista sin aceptarlo. */
export interface SlotRefresh {
  /** Rutas que salen de la consulta y no están en lista, pins ni excluidos. */
  nuevos: string[];
  /** Rutas de la lista que la consulta ya no devuelve y no están fijadas (la UI puede avisarlo). */
  salieron: string[];
}

export function refreshSlot(slot: Pick<InformeSlot, "atomos" | "pins" | "excluidos">, queryResults: string[]): SlotRefresh {
  const known = new Set([...slot.atomos, ...slot.pins, ...slot.excluidos]);
  const nuevos = [...new Set(queryResults)].filter((p) => !known.has(p));
  const results = new Set(queryResults);
  const pinned = new Set(slot.pins);
  return { nuevos, salieron: slot.atomos.filter((p) => !results.has(p) && !pinned.has(p)) };
}

const uniq = (xs: string[]) => [...new Set(xs)];
const without = (xs: string[], x: string) => xs.filter((y) => y !== x);

/** Acepta un `nuevo`: entra a la lista (y sale de excluidos si estaba). */
export function acceptAtom(slot: InformeSlot, path: string): InformeSlot {
  return { ...slot, atomos: uniq([...slot.atomos, path]), excluidos: without(slot.excluidos, path) };
}

/** Excluye: sale de la lista y de pins; no volverá como `nuevo` en próximas actualizaciones. */
export function excludeAtom(slot: InformeSlot, path: string): InformeSlot {
  return { ...slot, atomos: without(slot.atomos, path), pins: without(slot.pins, path), excluidos: uniq([...slot.excluidos, path]) };
}

/** Fija: entra a pins y a la lista, y sobrevive a la consulta. */
export function pinAtom(slot: InformeSlot, path: string): InformeSlot {
  return { ...slot, pins: uniq([...slot.pins, path]), atomos: uniq([...slot.atomos, path]), excluidos: without(slot.excluidos, path) };
}

/** Suelta el pin; el átomo se queda en la lista. */
export function unpinAtom(slot: InformeSlot, path: string): InformeSlot {
  return { ...slot, pins: without(slot.pins, path) };
}

/** Deshace una exclusión: el átomo vuelve a poder aparecer como `nuevo`. */
export function unexcludeAtom(slot: InformeSlot, path: string): InformeSlot {
  return { ...slot, excluidos: without(slot.excluidos, path) };
}

// ---------------------------------------------------------------- consulta local

export interface AtomFilters {
  kind?: AtomKind | AtomKind[];
  status?: AtomStatus | AtomStatus[];
  /** Grupo por prefijo: `infra` incluye `infra.ingesta`. */
  tag?: string;
  /** Subcadena, sin distinguir mayúsculas, sobre `text`, `quote` y tags. */
  text?: string;
}

/**
 * Resolvedor de consulta de v1, EN CLIENTE: la consulta por servidor (composición por query,
 * OPERACIONALIZACION §4 [falta]) no existe aún. Cuando exista, `refreshSlot` recibe sus
 * resultados en lugar de estos.
 */
export function matchQuery(atoms: Atom[], filters: AtomFilters): Atom[] {
  const list = <T,>(v: T | T[] | undefined): T[] | null => (v === undefined ? null : Array.isArray(v) ? v : [v]);
  const kinds = list(filters.kind);
  const statuses = list(filters.status);
  const needle = filters.text?.trim().toLowerCase();
  return atoms.filter((a) => {
    if (kinds && !kinds.includes(a.kind)) return false;
    if (statuses && !statuses.includes(a.status)) return false;
    if (filters.tag && !inGroup(a, filters.tag)) return false;
    if (needle && !`${a.text} ${a.quote} ${a.tags.join(" ")}`.toLowerCase().includes(needle)) return false;
    return true;
  });
}

// ---------------------------------------------------------------- creación

/** Payload de un átomo nuevo desde una selección `[from, to)` del campo `body` del acta. */
export function selectionToAtomPayload(body: string, from: number, to: number, kind: AtomKind, source: string): Payload {
  const start = Math.max(0, Math.min(from, to));
  const end = Math.min(body.length, Math.max(from, to));
  const quote = body.slice(start, end);
  return {
    kind,
    status: "propuesto",
    source,
    source_field: "body",
    start,
    end,
    tags: [],
    text: quote.slice(0, ATOM_TEXT_MAX),
    quote,
    conf: 1,
  };
}

/** Siguiente nombre `aN` libre. */
export function nextAtomName(existingNames: string[]): string {
  let max = 0;
  for (const name of existingNames) {
    const m = /^a(\d+)$/.exec(name);
    if (m) max = Math.max(max, Number(m[1]));
  }
  return `a${max + 1}`;
}
