/**
 * Cliente HTTP de `sldb serve`. Framework-agnóstico: solo usa `fetch`.
 * Toda escritura va por `/save` en modo batch con `expected` (control optimista).
 */
import type {
  CreateDocumentResult,
  DocumentSegments,
  Edge,
  ExtractionSegments,
  GraphDocument,
  LintReport,
  Payload,
  SaveChange,
  SaveResult,
  SchemaResponse,
  StoredDocument,
} from "./contract";

export class SldbHttpError extends Error {
  constructor(
    message: string,
    readonly status: number,
    readonly body: unknown,
  ) {
    super(message);
    this.name = "SldbHttpError";
  }
}

/** El documento cambió en SLDB desde que se leyó: la escritura se rechazó sin tocar nada. */
export class SaveConflictError extends SldbHttpError {
  constructor(message: string, body: unknown) {
    super(message, 409, body);
    this.name = "SaveConflictError";
  }
}

export interface SldbClient {
  schema(): Promise<SchemaResponse>;
  documents(): Promise<GraphDocument[]>;
  document(id: string): Promise<StoredDocument>;
  segments(id: string): Promise<DocumentSegments>;
  extract(model: string, markdown: string): Promise<ExtractionSegments>;
  save(changes: SaveChange[]): Promise<SaveResult>;
  /** Aristas del grafo; con `id` (`Model:name`) solo las que tocan ese documento. */
  getEdges(id?: string): Promise<Edge[]>;
  /** Crea un documento nuevo (`POST /docs`). Errores 400/404/409/422 lanzan `SldbHttpError`. */
  createDocument(model: string, name: string, payload: Payload): Promise<CreateDocumentResult>;
  /** Análisis que SLDB ya sirve; no se deriva nada de esto en el cliente. */
  lint(): Promise<LintReport>;
  isolated(): Promise<string[]>;
  cycles(limit?: number): Promise<string[][]>;
}

type FetchLike = (input: string, init?: RequestInit) => Promise<Response>;

function errorMessage(body: unknown, status: number): string {
  if (body && typeof body === "object" && "error" in body && typeof body.error === "string") {
    return body.error;
  }
  return `SLDB respondió ${status}`;
}

export function createHttpClient(baseUrl: string, fetchImpl: FetchLike = (i, init) => fetch(i, init)): SldbClient {
  const root = baseUrl.replace(/\/$/, "");

  async function request<T>(path: string, init?: RequestInit): Promise<T> {
    const response = await fetchImpl(`${root}${path}`, init);
    const body: unknown = await response.json().catch(() => null);
    if (response.status === 409) throw new SaveConflictError(errorMessage(body, 409), body);
    if (!response.ok) throw new SldbHttpError(errorMessage(body, response.status), response.status, body);
    return body as T;
  }

  const post = <T>(path: string, body: unknown) =>
    request<T>(path, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) });

  return {
    schema: () => request<SchemaResponse>("/schema"),
    documents: async () => (await request<{ documents: GraphDocument[] }>("/graph")).documents,
    document: (id) => request<StoredDocument>(`/document?id=${encodeURIComponent(id)}`),
    segments: (id) => request<DocumentSegments>(`/document/segments?id=${encodeURIComponent(id)}`),
    extract: (model, markdown) => post<ExtractionSegments>("/extract/segments", { model, markdown }),
    save: (changes) => post<SaveResult>("/save", { changes }),
    getEdges: async (id) => (await request<{ edges: Edge[] }>(id ? `/edges?id=${encodeURIComponent(id)}` : "/edges")).edges,
    createDocument: (model, name, payload) => post<CreateDocumentResult>("/docs", { model, name, payload }),
    lint: () => request<LintReport>("/lint"),
    isolated: async () => (await request<{ isolated: string[] }>("/graph/isolated")).isolated,
    cycles: async (limit = 20) => (await request<{ cycles: string[][] }>(`/graph/cycles?limit=${limit}`)).cycles,
  };
}
