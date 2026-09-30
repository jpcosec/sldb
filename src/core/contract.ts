/**
 * Contrato con SLDB. Espeja los modelos Pydantic del HANDOFF (§3).
 * Este módulo no depende de React ni del DOM: es reutilizable por cualquier superficie.
 */

export type Payload = Record<string, unknown>;

export type FieldKind =
  | "string"
  | "enum"
  | "stringlist"
  | "enumlist"
  | "list"
  | "boolean"
  | "integer"
  | "number"
  | "object"
  | "unknown";

/** Tipo del marcador en el template: `rev`/`optrev` son editables; `render`/`py` se navegan. */
export type MarkerKind = "rev" | "optrev" | "render" | "py" | "compose" | (string & {});

export type Display = "inline" | "block";

export interface TextRange {
  start: number;
  end: number;
  text: string;
}

export interface LiteralSegment extends TextRange {
  type: "literal";
}

/** De qué documento viene un tramo compuesto; es a donde se escribe al editarlo. */
export interface SourceRef {
  doc: string | null;
  path: string;
  model: string;
}

export interface CompositionSpec {
  name: string;
  source_field: string | null;
  model: string | null;
  /** `document`: refs a documentos (hoy). `field`: refs a atoms `docs/<doc>/<field>` (HANDOFF parte D). */
  ref: "document" | "field";
}

interface SegmentBase extends TextRange {
  path: string;
  marker: MarkerKind;
  traits: string[];
  editable: boolean;
  display: Display;
  source: SourceRef | null;
  children: Segment[];
}

export interface FieldSegment extends SegmentBase {
  type: "field";
  kind?: FieldKind;
  value?: unknown;
  composition?: CompositionSpec;
}

export interface CompositionPiece extends SegmentBase {
  type: "composition";
  source: SourceRef;
  ref_index: number;
  ref: string;
}

export type Segment = LiteralSegment | FieldSegment | CompositionPiece;

export interface DocumentSegments {
  id: string;
  doc: string;
  model: string;
  path: string;
  text: string;
  /** `false` cuando el archivo en disco no coincide con el render canónico. */
  canonical: boolean | null;
  payload: Payload;
  segments: Segment[];
}

export interface ExtractedField extends TextRange {
  path: string;
  marker: MarkerKind;
  traits: string[];
  editable: boolean;
  display: Display;
  kind?: FieldKind;
  value?: unknown;
  alignment: "exact" | "approximate";
}

export interface ExtractionSegments {
  model: string;
  text: string;
  payload: Payload;
  canonical_text: string;
  fields: ExtractedField[];
  /** Tramos del texto crudo que no salen ni del template ni de un field. */
  unmatched: TextRange[];
  coverage: number;
}

export interface SchemaField {
  name: string;
  kind: FieldKind;
  required: boolean;
  enum?: unknown[];
  default?: unknown;
  description?: string;
  /** Patrón declarado por el field, cuando el store lo expone. Se valida con ESE patrón. */
  pattern?: string;
}

export interface SchemaModel {
  id: string;
  model_ref: string;
  fields: SchemaField[];
  template?: string;
}

export interface SchemaResponse {
  models: SchemaModel[];
  errors?: { model: string; error: string }[];
}

export interface GraphDocument {
  id: string;
  model_name: string;
  path: string;
  payload: Payload;
  semantic_tags?: string[];
}

export interface StoredDocument {
  id: string;
  model_name: string;
  path: string;
  payload: Payload;
}

export type SaveAction = "create" | "update" | "delete";

export interface SaveChange {
  id: string;
  action: SaveAction;
  model?: string;
  payload?: Payload;
  expected?: Payload;
}

export interface SaveResult {
  ok: boolean;
  saved?: string[];
  error?: string;
  completed?: string[];
}

/**
 * Hallazgos de salud derivados de los endpoints que existen hoy (`/graph`, `/schema`,
 * `/document/segments`). No provienen de ningún endpoint de diagnóstico.
 *
 * `StructuralNoiseFinding` no es corrupción: es un contrato incompleto. Los headings
 * que viven dentro del valor de un field son secciones que el modelo no declara.
 */
export interface StructuralNoiseFinding {
  doc: string;
  model: string;
  path: string;
  /** Títulos (sin `#`) de los headings que aparecen dentro de valores de field. */
  headings: string[];
}

/** Documento que no se pudo leer, o cuyo archivo en disco no coincide con el render. */
export interface DocumentFinding {
  doc: string;
  model: string;
  path: string;
  detail: string;
}

export interface HealthReport {
  /** Ruido estructural: headings sin declarar dentro de fields. */
  structural: StructuralNoiseFinding[];
  /** `canonical:false`: el archivo en disco no coincide con el render del payload. */
  noncanonical: DocumentFinding[];
  /** `/document/segments` no respondió: no se pudo derivar nada de ese documento. */
  unreadable: DocumentFinding[];
  /** Modelos que `/schema` reportó como no importables. */
  modelErrors: { model: string; error: string }[];
  /** Documentos sondeados con `/document/segments`. */
  checked: number;
  /** `/lint` de SLDB. `null` si la ruta no respondió. */
  lint: LintProblem[] | null;
  /** `/graph/isolated`, solo documentos. `null` si la ruta no respondió. */
  isolated: GraphNodeRef[] | null;
  /** `/graph/cycles`. `null` si la ruta no respondió. */
  cycles: GraphNodeRef[][] | null;
}

/**
 * Análisis de grafo servido por SLDB. Estas rutas EXISTEN en `sldb serve`
 * (`cli/serve/routes.py`) y `graph_ui` ya las consume; no hay que derivarlas
 * en el cliente. Los ids vienen como URI `sldb://document/<Modelo>:<id>` o
 * `sldb://field/<Modelo>.<campo>`.
 */
export interface LintProblem {
  kind: string;
  severity: string;
  doc: string;
  detail: string;
}

export interface LintReport {
  problems: LintProblem[];
  count: number;
}

/**
 * Lo mínimo que la lógica pura necesita del schema: saber si un modelo declara un
 * campo. Se declara acá para que `core/` no dependa de `react/context`.
 */
export interface SchemaIndexLike {
  field(model: string, path: string): SchemaField | undefined;
}

/** Un nodo del grafo, tal como lo nombran los endpoints de análisis. */
export interface GraphNodeRef {
  /** La URI cruda que devolvió SLDB. */
  uri: string;
  /** `document` o `field`; otra cosa si SLDB agrega tipos. */
  kind: string;
  /** Modelo del nodo, cuando la URI lo nombra. */
  model?: string;
  /** Id del documento, solo para `kind === "document"`: sirve para enlazar. */
  doc?: string;
  /** Texto corto para mostrar. */
  label: string;
}
