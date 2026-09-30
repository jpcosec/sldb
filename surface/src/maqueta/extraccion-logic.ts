/**
 * Extracción · lógica pura (sin DOM ni ProseMirror): traduce entre offsets del `body` del acta y
 * posiciones del documento ProseMirror de la maqueta (un nodo `paragraph` por párrafo), calcula
 * los subrayados a partir de los offsets reales del átomo y ordena/filtra las tarjetas.
 *
 * Posiciones ProseMirror: el párrafo k empieza en `1 + Σ_{j<k}(len_j + 2)`. Offsets del body: el
 * párrafo k empieza en `paragraphsOf(body)[k].start` (con los "\n\n" que se pierden al dividir).
 */
import { paragraphsOf, type Paragraph } from "../core/atom-text";
import { anchorState, repairAnchor } from "../core/atoms";
import type { AtomKind } from "../core/contract";
import type { MockAtom } from "./adapter";

export type AnchorKind = "intact" | "drifted" | "orphan";

export interface HighlightRange {
  id: string;
  type: AtomKind;
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
export function orderAtoms(atoms: MockAtom[], ranges: HighlightRange[], kind: AtomKind | null, lowConfFirst: boolean): MockAtom[] {
  const from = new Map(ranges.map((r) => [r.id, r.from]));
  const pos = (a: MockAtom) => from.get(a.id) ?? Number.POSITIVE_INFINITY;
  return atoms
    .filter((a) => !kind || a.type === kind)
    .sort((a, b) => (lowConfFirst ? a.conf - b.conf : pos(a) - pos(b)));
}
