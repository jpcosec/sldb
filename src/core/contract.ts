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
