/**
 * Lógica pura de la vista Respuesta (maqueta `lp`): qué átomos entran al slot del que se redactó,
 * qué frases quedaron obsoletas (`stale`), las verificaciones de las reglas del system prompt y el
 * gate "Antes de enviar". Sin React ni red.
 *
 * Verificaciones REALES (se calculan sobre las frases): `p5` (teleconsulta antes que centros) y
 * `p7` (menos de 150 palabras y cierre con pregunta). Las de la maqueta para `p1`, `p2` y `p3` eran
 * "siempre ok" escritas a mano y NO se pueden comprobar en el texto: aquí no existen y esas reglas
 * (igual que cualquier otra sin verificación) se muestran sin ✓ y como "sin verificación automática".
 */
import { parseQuery } from "../core/atom-report";
import { matchQuery } from "../core/atoms";
import { paragraphsOf } from "../core/atom-text";
import { resolveAtom, type BaseUse, type FraseProvenance } from "../core/caso";
import type { Atom, Fuente, Informe, InformeSlotEntry } from "../core/contract";

/** Párrafos del mensaje de la paciente (como los parte el resto de la maqueta). */
export const messageParagraphs = (body: string): string[] => paragraphsOf(body).map((p) => p.text);

/** Slot del informe por nombre (`respuesta.slot`); `undefined` si no existe. */
export function slotByName(informe: Informe | undefined, name: string): InformeSlotEntry | undefined {
  return informe?.slotList.find((s) => s.name === name);
}

/** Ids de los átomos del slot: lista + pins, sin excluidos, sin repetir (los que resuelven a un átomo). */
export function slotAtomIds(slot: Pick<InformeSlotEntry, "atomos" | "pins" | "excluidos"> | undefined, atoms: Atom[]): string[] {
  if (!slot) return [];
  const out: string[] = [];
  for (const ref of [...slot.atomos, ...slot.pins]) {
    if (slot.excluidos.includes(ref)) continue;
    const a = resolveAtom(ref, atoms);
    if (a && !out.includes(a.id)) out.push(a.id);
  }
  return out;
}

/**
 * Ids de átomo que hoy sostienen una frase: en lista o pins del slot, no excluidos y no descartados
 * (la maqueta: estado `regla` o `pin`).
 */
export function includedIds(slot: InformeSlotEntry | undefined, atoms: Atom[]): Set<string> {
  return new Set(slotAtomIds(slot, atoms).filter((id) => resolveAtom(id, atoms)?.status !== "descartado"));
}

export interface Frase {
  n: number;
  texto: string;
  /** Ids de los átomos resueltos (los que existen). */
  ids: string[];
  /** Referencias sin átomo. */
  missing: string[];
  /** Algún átomo ya no está incluido en el slot (o no existe). */
  stale: boolean;
}

/** Frases con su marca `stale` (maqueta: `from.some(k => !m(k))`). */
export function frasesConEstado(prov: FraseProvenance[], included: Set<string>): Frase[] {
  return prov.map((f) => ({
    n: f.n,
    texto: f.texto,
    ids: f.atomos.map((a) => a.id),
    missing: f.missing,
    stale: f.missing.length > 0 || f.atomos.some((a) => !included.has(a.id)),
  }));
}

/** Palabras del texto completo de la respuesta (todas las frases, también las stale, como la maqueta). */
export const countWords = (frases: Pick<Frase, "texto">[]): number => frases.map((f) => f.texto).join(" ").split(/\s+/).filter(Boolean).length;

export interface Check {
  ok: boolean;
  label: string;
}

const firstFresh = (frases: Frase[], id: string): number => frases.findIndex((f) => f.ids.includes(id) && !f.stale);

/** p5: la teleconsulta (`f3`) se ofrece antes que los centros (`f5`): primera frase vigente con f3 antes de la primera con f5. */
export function checkTeleconsultaAntes(frases: Frase[]): Check {
  const tele = firstFresh(frases, "f3");
  const centros = firstFresh(frases, "f5");
  const ok = tele > -1 && (centros === -1 || tele < centros);
  return { ok, label: ok ? "Ofrece la teleconsulta antes que la atención presencial" : "La teleconsulta tiene que ir antes que los centros" };
}

/** p7: menos de 150 palabras y la última frase contiene una pregunta. */
export function checkLargoYCierre(frases: Frase[]): Check {
  const words = countWords(frases);
  const closes = frases.length > 0 && frases[frases.length - 1]!.texto.includes("?");
  return { ok: words < 150 && closes, label: `Largo: ${words} palabras (máximo 150); cierra ofreciendo ayuda` };
}

/** Verificaciones automáticas conocidas, por id de átomo de regla. El resto: sin verificación. */
export const RULE_CHECKS: Record<string, (frases: Frase[]) => Check> = {
  p5: checkTeleconsultaAntes,
  p7: checkLargoYCierre,
};

export interface RuleResult {
  atom: Atom;
  /** `null` = sin verificación automática (no se muestra ✓ ni !). */
  check: Check | null;
}

export function ruleResults(reglas: { atom: Atom }[], frases: Frase[]): RuleResult[] {
  return reglas.map(({ atom }) => {
    const fn = Object.prototype.hasOwnProperty.call(RULE_CHECKS, atom.id) ? RULE_CHECKS[atom.id] : undefined;
    return { atom, check: fn ? fn(frases) : null };
  });
}

/**
 * Átomos "nuevos, sin revisar" por slot: los que devuelve hoy la consulta del slot y no están en
 * lista, pins ni excluidos (misma definición que el Compositor). Consulta vacía = nada.
 */
export function nuevosPorSlot(informe: Informe | undefined, atoms: Atom[]): Record<string, string[]> {
  const out: Record<string, string[]> = {};
  for (const slot of informe?.slotList ?? []) {
    const { tokens, filters } = parseQuery(slot.query);
    if (!tokens.some((t) => t.active)) {
      out[slot.name] = [];
      continue;
    }
    const known = new Set([...slot.atomos, ...slot.pins, ...slot.excluidos]);
    const pool = atoms.filter((a) => a.status !== "descartado");
    out[slot.name] = [...new Set(matchQuery(pool, filters).map((a) => a.path))].filter((p) => !known.has(p));
  }
  return out;
}

export interface Pending {
  nuevos: number;
  stale: number;
  /** Avisos, como la lista de la maqueta. */
  avisos: string[];
  canSend: boolean;
}

export function pendientes(nuevos: number, stale: number): Pending {
  const avisos: string[] = [];
  if (nuevos) avisos.push(`${nuevos} ${nuevos === 1 ? "átomo nuevo sin revisar" : "átomos nuevos sin revisar"} en el Compositor`);
  if (stale) avisos.push(`${stale} ${stale === 1 ? "frase depende" : "frases dependen"} de átomos que ya no están`);
  return { nuevos, stale, avisos, canSend: avisos.length === 0 };
}

/** Texto de estado de la cabecera. */
export function estadoLabel(estado: string): string {
  if (estado === "enviada") return "Enviada (marcada en el store; no hay canal de entrega conectado)";
  if (estado === "borrador" || estado === "") return "Borrador, todavía no se envía.";
  return `Estado: ${estado}`;
}

/**
 * Bases en el orden de las fuentes del caso (system prompt y folleto = Programa, luego el mensaje =
 * Paciente), no en el del slot: así se ve como la maqueta (Programa primero). Estable.
 */
export function orderBases(bases: BaseUse[], fuentes: Pick<Fuente, "gid">[]): BaseUse[] {
  const rank = (b: BaseUse) => Math.min(...b.atoms.map((u) => { const i = fuentes.findIndex((f) => f.gid === u.atom.source); return i < 0 ? fuentes.length : i; }), fuentes.length);
  return bases.map((b, i) => ({ b, i, r: rank(b) })).sort((x, y) => x.r - y.r || x.i - y.i).map((x) => x.b);
}
