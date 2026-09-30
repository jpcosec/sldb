/**
 * Lógica pura del Compositor de la maqueta: estado de cada átomo por slot, cálculo de los
 * "nuevos, sin revisar" (no se persisten) y el gate. Reutiliza `core/atoms` y `core/atom-report`.
 */
import { matchQuery, SLOT_NAMES } from "../core/atoms";
import { parseQuery, type QueryToken } from "../core/atom-report";
import type { Atom, Informe, InformeSlot, SlotName } from "../core/contract";

/** Estado de un átomo dentro de un slot (las claves de la maqueta). */
export type CardState = "regla" | "pin" | "nuevo" | "excluido";

export const STATE_LABELS: Record<CardState, string> = {
  regla: "Por consulta",
  pin: "Fijado a mano",
  nuevo: "Nuevo, sin revisar",
  excluido: "Excluido a mano",
};

/** Rótulo del slot (`Ms.sections[].slot` de la maqueta). */
export const SLOT_TITLES: Record<SlotName, string> = {
  resumen: "Contexto del problema",
  decisiones: "Decisiones tomadas",
  riesgos: "Riesgos y a qué afectan",
  pendientes: "Temas sin resolver",
};

export interface SlotItem {
  path: string;
  state: CardState;
}

/**
 * Rutas que hoy devuelve la consulta del slot (átomos no descartados) y no están en lista, pins ni
 * excluidos. Una consulta vacía no trae nada: un slot sin filtros no jala todo el store.
 */
export function newPaths(slot: Pick<InformeSlot, "atomos" | "pins" | "excluidos" | "query">, atoms: Atom[]): string[] {
  const { tokens, filters } = parseQuery(slot.query);
  if (!tokens.some((t) => t.active)) return [];
  const known = new Set([...slot.atomos, ...slot.pins, ...slot.excluidos]);
  const pool = atoms.filter((a) => a.status !== "descartado");
  return [...new Set(matchQuery(pool, filters).map((a) => a.path))].filter((p) => !known.has(p));
}

export function newBySlot(informe: Informe, atoms: Atom[]): Record<SlotName, string[]> {
  return Object.fromEntries(SLOT_NAMES.map((s) => [s, newPaths(informe.slots[s], atoms)])) as Record<SlotName, string[]>;
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

/** Chips de filtro (`Tipo: hecho`): los tokens de la consulta que no son texto libre, con su posición. */
export interface FilterChip {
  index: number;
  label: string;
  value: string;
  active: boolean;
}

const LABELS: Record<string, string> = { tipo: "Tipo", tag: "Tag", estado: "Estado" };

export function filterChips(query: string): FilterChip[] {
  const out: FilterChip[] = [];
  parseQuery(query).tokens.forEach((t: QueryToken, index) => {
    if (t.kind === "texto") return;
    out.push({ index, label: LABELS[t.kind] ?? t.kind, value: t.value, active: t.active });
  });
  return out;
}

/** Agrega un token `tipo:x` / `tag:x` / `estado:x` al final de la consulta. */
export function addQueryFilter(query: string, kind: "tipo" | "tag" | "estado", value: string): string {
  return `${query.trim()} ${kind}:${value.trim()}`.trim();
}
