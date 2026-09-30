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
  version?: string;
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

/**
 * Átomos, relaciones e informes (OPERACIONALIZACION-VISTAS). Un átomo es un documento
 * `AtomDoc`; sus relaciones son `RelationDoc`; los verbos permitidos, `RelationTypeDoc`.
 */
export type AtomKind = "entidad" | "hecho" | "decision" | "pendiente" | "riesgo";
export type AtomStatus = "propuesto" | "confirmado" | "descartado";

/** Estado del ancla de un átomo respecto del texto actual del acta: se calcula, no se guarda. */
export type AnchorState = "intact" | "drifted" | "orphan";

export interface Atom {
  /** Id del documento (el de `/graph`, `/document` y `/save`): `a3`. */
  id: string;
  /** Id de grafo `AtomDoc:a3`, el que usan `source`/`target` de las aristas. */
  gid: string;
  /** Ruta del archivo (`docs/atoms/a3.md`): es lo que las listas de un informe referencian. */
  path: string;
  version?: string;
  kind: AtomKind;
  status: AtomStatus;
  /** `ActaDoc:<name>`. */
  source: string;
  source_field: string;
  start: number;
  end: number;
  /** Tags con puntos: `infra.ingesta` es el grupo `infra` ⊃ `ingesta`. */
  tags: string[];
  text: string;
  quote: string;
  conf: number;
}

export interface Acta {
  id: string;
  /** `ActaDoc:<id>`, como la nombra `Atom.source`. */
  gid: string;
  path: string;
  version?: string;
  title: string;
  body: string;
}

export interface RelationTypeSpec {
  /** Id del documento `RelationTypeDoc`. */
  id: string;
  name: string;
  source_types: string[];
  target_types: string[];
  cardinality: string;
  description: string;
}

/** Arista tal como la sirve `GET /edges`. `source`/`target` son `Model:name`. */
export interface Edge {
  id: string;
  source: string;
  target: string;
  type: string;
  origin: string;
  /** Id del `RelationDoc` que la respalda; `null` si es estructural (referencias, tags). */
  relationDoc: string | null;
}

export type SlotName = "resumen" | "decisiones" | "riesgos" | "pendientes";
export type SlotMode = "viñetas" | "prosa" | "tabla";

/** Estado de un slot de informe. `atomos`, `pins` y `excluidos` son RUTAS de átomos. */
export interface InformeSlot {
  atomos: string[];
  query: string;
  pins: string[];
  excluidos: string[];
  modo: SlotMode;
}

export interface Informe {
  id: string;
  path: string;
  version?: string;
  slots: Record<SlotName, InformeSlot>;
  payload: Payload;
}

export interface CreateDocumentResult {
  ok: boolean;
  id: string;
  version: string;
}

// ---------------------------------------------------------------- similitud (`/corpus/rank`, `/similar`)

/** Documento parecido a una consulta: `Hit` de `sldb.api.corpus`, tal cual. */
export interface RankHit {
  id: string;
  model: string;
  name: string;
  score: number;
  payload: Payload;
  tags: string[];
}

/** Campo parecido a una consulta (`fields=1`): `FieldHit` de `sldb.api.corpus`. `id` es `docs/<Model>/<doc>/<field>`. */
export interface FieldRankHit {
  id: string;
  document_id: string;
  field: string;
  model: string;
  name: string;
  score: number;
  text: string;
  payload: Payload;
  tags: string[];
}

/**
 * Resultado de pedir similitud. Los tres estados NO se mezclan: `ok` con `hits: []` significa
 * "no hay parecidos"; `not_indexed` que el corpus nunca se indexó (hay que pedir `refresh`);
 * `unavailable` que el servidor no respondió o no tiene la ruta. Una vista nunca muestra
 * `not_indexed` ni `unavailable` como si fueran una lista vacía, ni inventa una heurística.
 */
export type SimilarityResult<T> =
  | { status: "ok"; hits: T[] }
  | { status: "not_indexed" }
  | { status: "unavailable"; reason: string };

export interface RankParams {
  /** Texto a comparar contra el corpus. */
  q: string;
  k?: number;
  /** Puntaje mínimo (0 a 1). */
  threshold?: number;
  /** Restringe a estos ids; con `fields`, nombrar un documento admite todos sus campos. */
  among?: string[];
  /** Rankea campos (`FieldRankHit`) en vez de documentos. */
  fields?: boolean;
  /** `true` construye/actualiza el índice (puede ser lento); `false` solo lee lo indexado. */
  refresh?: boolean;
}

/** Vecino por grafo: `[node_id, cuántos destinos comparte]`, más compartidos primero. */
export type SimilarNode = [string, number];
