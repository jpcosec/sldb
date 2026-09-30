/**
 * Lógica pura del Compositor de la maqueta: estado de cada átomo por slot, cálculo de los
 * "nuevos, sin revisar" (no se persisten), chips de filtro y opciones del "Agregar filtro".
 * Reutiliza `core/atoms` y `core/atom-report`.
 */
import { ATOM_STATUSES, atomRelationTypes, KIND_LABELS, kindLabel, matchQuery } from "../core/atoms";
import { parseQuery, type ParseQueryOptions, type QueryToken, type QueryTokenKind } from "../core/atom-report";
import { basesTree } from "../core/caso";
import type { Atom, Edge, Informe, InformeSlot, RelationTypeSpec } from "../core/contract";

/** Estado de un átomo dentro de un slot (las claves de la maqueta). */
export type CardState = "regla" | "pin" | "nuevo" | "excluido";

export const STATE_LABELS: Record<CardState, string> = {
  regla: "Por consulta",
  pin: "Fijado a mano",
  nuevo: "Nuevo, sin revisar",
  excluido: "Excluido a mano",
};

/** Rótulo por defecto de los slots del informe VIEJO (sin `_rotulo`). */
export const OLD_SLOT_ROTULOS: Record<string, string> = {
  resumen: "Contexto del problema",
  decisiones: "Decisiones tomadas",
  riesgos: "Riesgos y a qué afectan",
  pendientes: "Temas sin resolver",
};

export interface SlotItem {
  path: string;
  state: CardState;
}

/** Opciones de `parseQuery` para este store: tipos válidos = los conocidos y los de los átomos. */
export function queryOptions(atoms: Atom[], grupos: ParseQueryOptions["grupos"] = []): ParseQueryOptions {
  return { kinds: [...new Set([...Object.keys(KIND_LABELS), ...atoms.map((a) => a.kind)])], grupos };
}

/**
 * Rutas que hoy devuelve la consulta del slot (átomos no descartados) y no están en lista, pins ni
 * excluidos. Una consulta vacía no trae nada: un slot sin filtros no jala todo el store.
 */
export function newPaths(
  slot: Pick<InformeSlot, "atomos" | "pins" | "excluidos" | "query">,
  atoms: Atom[],
  edges: Edge[] = [],
  opts: ParseQueryOptions = {},
): string[] {
  const { tokens, filters } = parseQuery(slot.query, opts);
  if (!tokens.some((t) => t.active)) return [];
  const known = new Set([...slot.atomos, ...slot.pins, ...slot.excluidos]);
  const pool = atoms.filter((a) => a.status !== "descartado");
  return [...new Set(matchQuery(pool, filters, edges).map((a) => a.path))].filter((p) => !known.has(p));
}

/** Nuevos por slot (clave = nombre del slot), en el orden del informe. */
export function newBySlot(informe: Pick<Informe, "slotList">, atoms: Atom[], edges: Edge[] = [], opts: ParseQueryOptions = {}): Record<string, string[]> {
  return Object.fromEntries(informe.slotList.map((s) => [s.name, newPaths(s, atoms, edges, opts)]));
}

/** Tarjetas del slot: los nuevos primero, luego lista/pins (orden del informe) y al final los excluidos. */
export function slotItems(slot: InformeSlot, nuevos: string[]): SlotItem[] {
  const seen = new Set<string>();
  const out: SlotItem[] = [];
  const push = (path: string, state: CardState) => {
    if (seen.has(path)) return;
    seen.add(path);
    out.push({ path, state });
  };
  for (const p of nuevos) push(p, "nuevo");
  for (const p of slot.atomos) push(p, slot.pins.includes(p) ? "pin" : "regla");
  for (const p of slot.pins) push(p, "pin");
  for (const p of slot.excluidos) push(p, "excluido");
  return out;
}

/** Lo que entra al documento final: `regla` y `pin`. */
export const isIncluded = (state: CardState): boolean => state === "regla" || state === "pin";

/** Chip de filtro (`Base: Paciente`): un token de la consulta que no es texto libre, con su posición. */
export interface FilterChip {
  index: number;
  /** Etiqueta con prefijo, `Base: Paciente`. */
  label: string;
  /** Prefijo (`Base`) y valor (`Paciente`) por separado, como los pinta la maqueta. */
  prefix: string;
  value: string;
  active: boolean;
}

export function filterChips(query: string, opts: ParseQueryOptions = {}): FilterChip[] {
  const out: FilterChip[] = [];
  parseQuery(query, opts).tokens.forEach((t: QueryToken, index) => {
    if (t.kind === "texto") return;
    const cut = t.label.indexOf(": ");
    out.push({ index, label: t.label, prefix: cut < 0 ? t.label : t.label.slice(0, cut), value: cut < 0 ? "" : t.label.slice(cut + 2), active: t.active });
  });
  return out;
}

export type FilterKind = Exclude<QueryTokenKind, "texto">;

/** Tipos de filtro del desplegable "Agregar filtro", en el orden de la maqueta. */
export const FILTER_KINDS: { kind: FilterKind; label: string }[] = [
  { kind: "tipo", label: "Tipo" },
  { kind: "estado", label: "Estado" },
  { kind: "base", label: "Base" },
  { kind: "tag", label: "Tag" },
  { kind: "distancia", label: "Distancia" },
  { kind: "relacion", label: "Relación" },
];

export interface FilterOption {
  value: string;
  label: string;
}

/** Valores válidos de cada tipo de filtro, sacados de los datos. */
export function filterOptions(
  kind: FilterKind,
  data: { atoms: Atom[]; grupos?: ParseQueryOptions["grupos"]; relationTypes?: RelationTypeSpec[] },
): FilterOption[] {
  switch (kind) {
    case "tipo":
      return [...new Set(data.atoms.map((a) => a.kind))].map((k) => ({ value: k, label: kindLabel(k) }));
    case "estado":
      return ATOM_STATUSES.map((s) => ({ value: s, label: s[0]!.toUpperCase() + s.slice(1) }));
    case "base":
      return basesTree(data.atoms, data.grupos).map((b) => ({ value: b.base, label: b.title }));
    case "tag":
      return basesTree(data.atoms, data.grupos).flatMap((b) => b.subgroups.map((s) => ({ value: s.tag, label: `${b.title} · ${s.title}` })));
    case "distancia":
      return [0, 1, 2, 3].map((n) => ({ value: String(n), label: `${n} ${n === 1 ? "salto" : "saltos"}` }));
    case "relacion":
      return atomRelationTypes(data.relationTypes ?? []).map((t) => ({ value: t.name, label: t.name.replace(/_/g, " ") }));
  }
}

/** Agrega un token `<kind>:<valor>` al final de la consulta. */
export function addQueryFilter(query: string, kind: FilterKind, value: string): string {
  return `${query.trim()} ${kind}:${value.trim()}`.trim();
}
