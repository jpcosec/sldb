/**
 * BANDEJA · lo anotado sin ubicar (§6.4).
 *
 * La propuesta describe la bandeja con sugerencias por similitud (`Corpus.rank()`)
 * y destino por vecindad. `Corpus.rank()` NO está cableado al CLI ni servido por
 * HTTP (§5), y `/graph/neighborhood` devuelve solo el nodo consultado en este
 * store. Sin eso, la bandeja LISTA pero no SUGIERE — y eso se dice en la vista,
 * no se simula con una heurística inventada.
 *
 * Lo que sí es derivable hoy, de `/graph` y `/schema`:
 *
 * - SIN PROCEDENCIA: el documento declara `provenance` en su modelo y lo tiene
 *   vacío. Regla 2 de la propuesta: "todo atom tiene origen; sin provenance no es
 *   conocimiento, es opinión". Es el criterio de bandeja que el store sí sostiene.
 * - SIN UBICAR POR TAG: `status:draft` y equivalentes, cuando se usen.
 *
 * Un documento cuyo modelo NO declara `provenance` no es un borrador: es un tipo
 * de documento al que la procedencia no le aplica. Distinguirlo es el punto.
 */
import type { GraphDocument, SchemaIndexLike } from "./contract";

/** Tags que marcan algo anotado y todavía sin ubicar. */
const DRAFT_TAGS = new Set(["status:draft", "status:borrador", "draft", "borrador"]);

export type TrayReason = "sin-procedencia" | "marcado-borrador";

export interface TrayEntry {
  doc: string;
  model: string;
  path: string;
  title: string;
  reasons: TrayReason[];
  /** Texto corto del documento, para reconocerlo sin abrirlo. */
  excerpt: string;
}

function textOf(value: unknown): string {
  return typeof value === "string" ? value.trim() : "";
}

function tagsOf(doc: GraphDocument): string[] {
  const tags = doc.payload.tags;
  return Array.isArray(tags) ? tags.filter((tag): tag is string => typeof tag === "string") : [];
}

export function isDraftTagged(doc: GraphDocument): boolean {
  return tagsOf(doc).some((tag) => DRAFT_TAGS.has(tag.toLowerCase()));
}

/**
 * `true` solo si el modelo DECLARA `provenance` y el documento lo tiene vacío.
 * Si el modelo no lo declara, la procedencia no aplica y el documento no es un
 * borrador: devolver `true` ahí llenaría la bandeja de ruido.
 */
export function lacksProvenance(doc: GraphDocument, declares: (model: string, field: string) => boolean): boolean {
  if (!declares(doc.model_name, "provenance")) return false;
  return textOf(doc.payload.provenance) === "";
}

function excerptOf(doc: GraphDocument): string {
  const summary = textOf(doc.payload.summary) || textOf(doc.payload.answer) || textOf(doc.payload.motive);
  return summary.length > 220 ? `${summary.slice(0, 220)}…` : summary;
}

export function titleOf(doc: GraphDocument): string {
  return textOf(doc.payload.title) || doc.id;
}

/** Los documentos que están en la bandeja, con el motivo por el que cayeron ahí. */
export function collectTray(docs: GraphDocument[], schema: SchemaIndexLike | null): TrayEntry[] {
  const declares = (model: string, field: string) => (schema ? schema.field(model, field) !== undefined : false);
  const entries: TrayEntry[] = [];
  for (const doc of docs) {
    const reasons: TrayReason[] = [];
    if (isDraftTagged(doc)) reasons.push("marcado-borrador");
    if (lacksProvenance(doc, declares)) reasons.push("sin-procedencia");
    if (reasons.length === 0) continue;
    entries.push({ doc: doc.id, model: doc.model_name, path: doc.path, title: titleOf(doc), reasons, excerpt: excerptOf(doc) });
  }
  return entries;
}

/** Cuenta por modelo, para que la bandeja no sea una lista plana de 90 ítems. */
export function groupByModel(entries: TrayEntry[]): { model: string; entries: TrayEntry[] }[] {
  const byModel = new Map<string, TrayEntry[]>();
  for (const entry of entries) byModel.set(entry.model, [...(byModel.get(entry.model) ?? []), entry]);
  return [...byModel.entries()]
    .map(([model, list]) => ({ model, entries: list }))
    .sort((a, b) => b.entries.length - a.entries.length || a.model.localeCompare(b.model));
}
