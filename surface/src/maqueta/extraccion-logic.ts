/**
 * Extracción · lógica pura (sin DOM ni ProseMirror): traduce entre offsets del `body` del acta y
 * posiciones del documento ProseMirror de la maqueta (un nodo `paragraph` por párrafo), calcula
 * los subrayados a partir de los offsets reales del átomo y ordena/filtra las tarjetas.
 *
 * Posiciones ProseMirror: el párrafo k empieza en `1 + Σ_{j<k}(len_j + 2)`. Offsets del body: el
 * párrafo k empieza en `paragraphsOf(body)[k].start` (con los "\n\n" que se pierden al dividir).
 */
import { paragraphsOf, type Paragraph } from "../core/atom-text";
import { anchorState, KIND_LABELS, repairAnchor } from "../core/atoms";
import type { MockAtom } from "./adapter";

export type AnchorKind = "intact" | "drifted" | "orphan";

export interface HighlightRange {
  id: string;
  type: string;
  /** Posiciones ProseMirror. */
  from: number;
  to: number;
  draft: boolean;
  /** Cuántos rangos más chicos... más grandes lo contienen (altura de la línea, como la maqueta). */
  layer: number;
  anchor: AnchorKind;
}

/** Posición ProseMirror donde empieza el contenido de cada párrafo. */
export function pmStarts(paras: Paragraph[]): number[] {
  const out: number[] = [];
  let pos = 1;
  for (const p of paras) {
    out.push(pos);
    pos += p.text.length + 2;
  }
  return out;
}

/**
 * Offset del body → posición ProseMirror. Si cae en un separador "\n\n" se ajusta al borde más
 * cercano del lado `side` (`start` → inicio del párrafo siguiente, `end` → fin del anterior).
 */
export function bodyToPm(paras: Paragraph[], offset: number, side: "start" | "end"): number | null {
  const starts = pmStarts(paras);
  for (let i = 0; i < paras.length; i++) {
    const p = paras[i]!;
    if (offset >= p.start && offset <= p.end) {
      // el borde exacto entre dos párrafos no existe: end==p.end sólo vale como fin
      if (offset === p.end && side === "start" && i + 1 < paras.length) return starts[i + 1]!;
      return starts[i]! + (offset - p.start);
    }
    if (offset < p.start) return side === "start" ? starts[i]! : i > 0 ? starts[i - 1]! + paras[i - 1]!.text.length : null;
  }
  return side === "end" && paras.length ? starts[paras.length - 1]! + paras[paras.length - 1]!.text.length : null;
}

/** Posición ProseMirror → offset del body y párrafo al que pertenece; `null` si no cae en texto. */
export function pmToBody(paras: Paragraph[], pos: number): { offset: number; para: number } | null {
  const starts = pmStarts(paras);
  for (let i = 0; i < paras.length; i++) {
    const p = paras[i]!;
    if (pos >= starts[i]! && pos <= starts[i]! + p.text.length) return { offset: p.start + (pos - starts[i]!), para: i };
  }
  return null;
}

export type PmSelection = { ok: true; from: number; to: number } | { ok: false; reason: string };

/** Selección ProseMirror `[from,to]` → offsets reales del body; un solo párrafo y no vacía. */
export function selectionToBodyRange(body: string, from: number, to: number): PmSelection {
  const paras = paragraphsOf(body);
  const a = pmToBody(paras, Math.min(from, to));
  const b = pmToBody(paras, Math.max(from, to));
  if (!a || !b) return { ok: false, reason: "La selección no está dentro del texto." };
  if (a.para !== b.para) return { ok: false, reason: "La selección cruza un límite de párrafo; elige texto de un solo párrafo." };
  if (b.offset <= a.offset || body.slice(a.offset, b.offset).trim() === "") return { ok: false, reason: "La selección está vacía." };
  return { ok: true, from: a.offset, to: b.offset };
}

/** Rango del body con el que se subraya un átomo (offsets reales; movida → donde está la cita). */
export function atomBodyRange(body: string, a: MockAtom): { start: number; end: number; anchor: AnchorKind } | null {
  const check = anchorState(body, a.atom);
  if (check.state === "orphan") return null;
  if (check.state === "intact") return a.atom.end > a.atom.start ? { start: a.atom.start, end: a.atom.end, anchor: "intact" } : null;
  const fixed = repairAnchor(body, a.atom);
  return fixed ? { ...fixed, anchor: "drifted" } : null;
}

/** Subrayados (posiciones ProseMirror) de los átomos que tienen ancla; las huérfanas no aparecen. */
export function highlightRanges(body: string, atoms: MockAtom[]): HighlightRange[] {
  const paras = paragraphsOf(body);
  const raw: HighlightRange[] = [];
  for (const a of atoms) {
    const r = atomBodyRange(body, a);
    if (!r) continue;
    const from = bodyToPm(paras, r.start, "start");
    const to = bodyToPm(paras, r.end, "end");
    if (from === null || to === null || to <= from) continue;
    raw.push({ id: a.id, type: a.type, from, to, draft: a.status !== "confirmado", layer: 0, anchor: r.anchor });
  }
  return raw.map((o) => ({
    ...o,
    layer: raw.filter((i) => i !== o && i.from <= o.from && i.to >= o.to && i.to - i.from > o.to - o.from).length,
  }));
}

/** Estado de ancla de cada átomo, por id. */
export function anchorKinds(body: string, atoms: MockAtom[]): Map<string, AnchorKind> {
  return new Map(atoms.map((a) => [a.id, anchorState(body, a.atom).state]));
}

/** Tarjetas visibles: filtra por tipo y ordena por posición en el texto o por confianza ascendente. */
export function orderAtoms(atoms: MockAtom[], ranges: HighlightRange[], kind: string | null, lowConfFirst: boolean): MockAtom[] {
  const from = new Map(ranges.map((r) => [r.id, r.from]));
  const pos = (a: MockAtom) => from.get(a.id) ?? Number.POSITIVE_INFINITY;
  return atoms
    .filter((a) => !kind || a.type === kind)
    .sort((a, b) => (lowConfFirst ? a.conf - b.conf : pos(a) - pos(b)));
}

/** Tipos con color propio en `maqueta.css` (`--t-*`); el resto usa el neutro de `extraccion.css`. */
const COLORED_KINDS = new Set(["regla", "criterio", "logistica", "paciente", "pregunta", "entidad", "hecho", "decision", "pendiente", "riesgo"]);
/** Sufijo de las clases `t-<x>`, `bg-t-<x>`, `tx-t-<x>`, `bl-t-<x>`. */
export const kindClass = (kind: string): string => (COLORED_KINDS.has(kind) ? kind : "otro");

const CASO_KINDS = ["regla", "criterio", "logistica", "paciente", "pregunta"];
const ACTA_KINDS = ["entidad", "hecho", "decision", "pendiente", "riesgo"];

/**
 * Tipos de átomo del caso: los presentes en los datos, completados con su familia (los del caso
 * Levira o los del acta vieja, porque el modelo los restringe) y ordenados como `KIND_LABELS`.
 */
export function caseKinds(present: string[]): string[] {
  const set = new Set(present);
  if (CASO_KINDS.some((k) => set.has(k))) CASO_KINDS.forEach((k) => set.add(k));
  if (ACTA_KINDS.some((k) => set.has(k))) ACTA_KINDS.forEach((k) => set.add(k));
  const known = Object.keys(KIND_LABELS);
  const rank = (k: string) => (known.indexOf(k) < 0 ? known.length : known.indexOf(k));
  return [...set].sort((a, b) => rank(a) - rank(b) || a.localeCompare(b));
}

/** Tipo de un átomo nuevo: `regla` (caso), `hecho` (acta vieja) o el primero disponible. */
export function defaultKind(kinds: string[]): string {
  return kinds.includes("regla") ? "regla" : kinds.includes("hecho") ? "hecho" : (kinds[0] ?? "hecho");
}

/** Ícono de la pestaña de fuente, tal cual la maqueta (`lM`). */
export function fuenteIcon(tipo: string): string {
  if (tipo === "prompt") return "\u2699\uFE0F";
  if (tipo === "mensaje" || tipo === "paciente") return "\u{1F4AC}";
  return "\u{1F4C4}";
}

/** Clase de tipografía del texto (`src-prompt` monoespaciada, `src-paciente` sans; el resto serif). */
export function fuenteFontClass(tipo: string): string {
  if (tipo === "prompt") return "src-prompt";
  if (tipo === "mensaje" || tipo === "paciente") return "src-paciente";
  return "";
}

/**
 * Id nuevo para un átomo creado desde el texto: prefijo por tipo de fuente (`p` prompt, `f` folleto,
 * `c` mensaje del paciente; `a` en el resto) y el siguiente número libre de ese prefijo.
 */
export function nextAtomId(existing: string[], fuenteTipo: string): string {
  const prefix = fuenteTipo === "prompt" ? "p" : fuenteTipo === "folleto" ? "f" : fuenteTipo === "mensaje" || fuenteTipo === "paciente" ? "c" : "a";
  const used = new Set(existing);
  let max = 0;
  for (const id of existing) {
    const m = new RegExp(`^${prefix}(\\d+)$`).exec(id);
    if (m) max = Math.max(max, Number(m[1]));
  }
  let n = max + 1;
  while (used.has(`${prefix}${n}`)) n++;
  return `${prefix}${n}`;
}

const TIPO_RANK: Record<string, number> = { prompt: 0, folleto: 1, mensaje: 2, paciente: 2 };
/** Orden de las pestañas como la maqueta (prompt, folleto, mensaje); el resto al final, en su orden. */
export function orderFuentes<T extends { tipo: string }>(fuentes: T[]): T[] {
  const rank = (f: T) => TIPO_RANK[f.tipo] ?? 3;
  return fuentes.map((f, i) => [f, i] as const).sort((a, b) => rank(a[0]) - rank(b[0]) || a[1] - b[1]).map(([f]) => f);
}
