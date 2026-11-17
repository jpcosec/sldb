import React, { useEffect, useMemo, useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { resolveFieldAuthority } from "../core/authority";
import type {
  AuthorityKind,
  CompositionPiece,
  Edge,
  FieldSegment,
  GraphDocument,
  ModelCatalogEntry,
  ModelDescription,
  ResolvedNotationView,
  SegmentTableData,
} from "../core/contract";
import { layoutSegments, type InlinePiece, type LayoutUnit } from "../core/layout";
import { useSldb } from "../react/context";
import { useDocumentEditor } from "../react/useDocumentEditor";
import { NotationSvgCanvas } from "./NotationSvgCanvas";
import { TopologyMindmap } from "./TopologyMindmap";

export type WorkbenchLens = "lectura" | "fierros";

export interface ProsaWorkbenchViewProps {
  docId: string;
  lens: WorkbenchLens;
  documents: GraphDocument[];
  models: ModelCatalogEntry[];
  onSelectDoc(id: string): void;
  onInspectDiagram(specId: string, nodeDoc?: string): void;
  onOpenSource(sourceDocId: string): void;
  onOpenStudio(modelName: string): void;
  onDirtyChange?(dirty: boolean): void;
}

function parseDocRef(
  raw: unknown,
): { model: string | null; docId: string; field: string | null } | null {
  if (typeof raw !== "string") return null;
  const trimmed = raw.trim();
  const typed = /^([A-Z][A-Za-z0-9_]*Doc):([a-zA-Z0-9_.-]+)(?:#([a-zA-Z0-9_./-]+))?$/.exec(trimmed);
  if (typed) {
    return { model: typed[1]!, docId: typed[2]!, field: typed[3] ?? null };
  }
  const docsPath = /^docs\/(?:([A-Z][A-Za-z0-9_]*Doc)\/)?([a-zA-Z0-9_.-]+)(?:\/([a-zA-Z0-9_.-]+))?(?:\.md)?$/.exec(
    trimmed,
  );
  if (docsPath) {
    return { model: docsPath[1] ?? null, docId: docsPath[2]!, field: docsPath[3] ?? null };
  }
  return null;
}

export function ProsaWorkbenchView({
  docId,
  lens,
  documents,
  models,
  onSelectDoc,
  onInspectDiagram,
  onOpenSource,
  onOpenStudio,
}: ProsaWorkbenchViewProps) {
  const { client } = useSldb();
  const { data, loadError, save, commit } = useDocumentEditor(docId);
  const [hoveredRefDoc, setHoveredRefDoc] = useState<string | null>(null);
  const [modelDetail, setModelDetail] = useState<ModelDescription | null>(null);
  const [edges, setEdges] = useState<Edge[]>([]);

  useEffect(() => {
    if (!data?.model) return;
    let active = true;
    client
      .describeModel(data.model)
      .then((desc: ModelDescription) => {
        if (!active) return;
        setModelDetail(desc);
      })
      .catch(() => {
        if (!active) return;
        setModelDetail(null);
      });
    return () => {
      active = false;
    };
  }, [client, data?.model]);

  useEffect(() => {
    if (!data?.doc) return;
    let active = true;
    const gid = `${data.model}:${data.doc}`;
    client
      .getEdges(gid)
      .then((res: Edge[]) => {
        if (!active) return;
        setEdges(res ?? []);
      })
      .catch(() => {
        if (!active) return;
        setEdges([]);
      });
    return () => {
      active = false;
    };
  }, [client, data?.model, data?.doc]);

  const authority: AuthorityKind = modelDetail?.authority ?? "authored";
  /** `content_hash` del documento (`GET /documents`): el `expected` que compara `POST /save`. */
  const expectedVersion = useMemo(() => {
    if (!data) return null;
    const doc = documents.find((d) => d.id === data.doc || d.id === data.id);
    return typeof doc?.version === "string" && doc.version ? doc.version.slice(0, 7) : null;
  }, [documents, data]);
  const modelRef = useMemo(
    () => modelDetail?.model_ref ?? models.find((m) => m.name === data?.model)?.model_ref,
    [modelDetail, models, data?.model],
  );

  const units = useMemo(() => {
    if (!data?.segments) return [];
    return layoutSegments(data.segments);
  }, [data?.segments]);

  const connectedLabels = useMemo(() => {
    const names = new Set<string>();
    for (const e of edges) {
      const other = e.source.endsWith(`:${data?.doc}`) ? e.target : e.source;
      const clean = other.includes(":") ? other.split(":")[1]! : other;
      if (clean && clean !== data?.doc) {
        const doc = documents.find((d) => d.id === clean || d.id === other);
        names.add(String(doc?.payload?.title ?? clean));
      }
    }
    return Array.from(names).slice(0, 6);
  }, [edges, data?.doc, documents]);

  if (loadError) {
    return (
      <div className="wb-split-38-62" data-testid="prosa-workbench-view">
        <div style={{ padding: 32 }} className="wb-mono">
          Error al cargar {docId}: {loadError}
        </div>
      </div>
    );
  }

  if (!data) {
    return (
      <div className="wb-split-38-62" data-testid="prosa-workbench-view">
        <div style={{ padding: 32, color: "var(--wb-ink-muted)" }} className="wb-mono">
          Cargando documento {docId}...
        </div>
      </div>
    );
  }

  const docTitle = String(data.payload?.title ?? data.doc);
  const rawEstado = data.payload?.estado ?? data.payload?.status;
  const docEstado = typeof rawEstado === "string" && rawEstado.trim() ? rawEstado : null;
  const isFierros = lens === "fierros";
  const hasTitleField = Object.prototype.hasOwnProperty.call(data.payload ?? {}, "title");
  const titleCanEdit =
    hasTitleField && resolveFieldAuthority(data.model, data.doc, "title", authority, modelRef).allowed;
  const saveError =
    save.status === "error" || save.status === "conflict" ? save.message : null;

  return (
    <div className="wb-split-38-62" data-testid="prosa-workbench-view">
      {/* LEFT PANE (38%): 2D Spatial Mindmap + Bottom Schema Summary */}
      <TopologyMindmap
        data={data}
        documents={documents}
        edges={edges}
        modelDetail={modelDetail}
        hoveredRefDoc={hoveredRefDoc}
        onSelectDoc={onSelectDoc}
        onInspectDiagram={(specId) => onInspectDiagram(specId)}
        onOpenSource={onOpenSource}
        onOpenStudio={onOpenStudio}
      />

      {/* RIGHT PANE (62%): Editorial Prose Sheet with Marginal Gutter */}
      <section className="wb-pane-right-62">
        <div className={isFierros ? "wb-editorial-sheet" : "wb-editorial-sheet--lectura"}>
          {/* Document Editorial Header */}
          <header style={{ marginBottom: 36 }}>
            <h1
              className="wb-serif"
              style={{
                fontSize: 30,
                fontWeight: 500,
                letterSpacing: "-0.015em",
                lineHeight: 1.25,
                color: "var(--wb-ink)",
                margin: "0 0 6px 0",
              }}
            >
              <InlineEditableProse
                value={docTitle}
                canEdit={titleCanEdit}
                onCommit={(next) => void commit({ doc: data.id, model: data.model }, "title", next)}
              />
            </h1>
            <p
              className="wb-mono"
              style={{
                fontSize: 11.5,
                color: "var(--wb-ink-muted)",
                margin: 0,
              }}
            >
              {data.model} · {docEstado ? `${docEstado} · ` : ""}
              <span style={{ color: "var(--wb-ink-tertiary)" }}>
                path: {data.path || `${data.doc}.md`}
              </span>
              {save.status === "saving" && " · guardando..."}
              {save.status === "saved" && " · ✓ sincronizado"}
            </p>
            {saveError && (
              <div
                role="alert"
                className="wb-mono"
                data-testid="prosa-save-error"
                style={{
                  marginTop: 10,
                  padding: "6px 10px",
                  fontSize: 11.5,
                  border: "1px solid var(--wb-ink)",
                  color: "var(--wb-ink)",
                  borderRadius: "var(--wb-radius)",
                }}
              >
                {save.status === "conflict" ? "✗ Conflicto al guardar" : "✗ Error al guardar"}: {saveError}
              </div>
            )}
          </header>

          {/* Document Body Segments via layoutSegments */}
          <div>
            {units.map((unit, idx) => (
              <RenderedLayoutUnit
                key={idx}
                unit={unit}
                docId={data.doc}
                modelName={data.model}
                authority={authority}
                modelRef={modelRef}
                lens={lens}
                expectedVersion={expectedVersion}
                onCommitField={(path, nextVal) =>
                  void commit({ doc: data.id, model: data.model }, path, nextVal)
                }
                onSelectDoc={onSelectDoc}
                onInspectDiagram={onInspectDiagram}
                onOpenSource={onOpenSource}
                onHoverRef={setHoveredRefDoc}
              />
            ))}
          </div>

          {/* Editorial Footer: Conectado con */}
          {connectedLabels.length > 0 && (
            <footer
              style={{
                marginTop: 56,
                paddingTop: 20,
                borderTop: "1px solid var(--wb-hairline)",
              }}
            >
              <span
                className="wb-mono"
                style={{
                  fontSize: 10.5,
                  textTransform: "uppercase",
                  letterSpacing: "0.06em",
                  color: "var(--wb-ink-muted)",
                  display: "block",
                  marginBottom: 8,
                }}
              >
                Conectado con
              </span>
              <div
                style={{
                  display: "flex",
                  flexWrap: "wrap",
                  gap: "6px 12px",
                  fontSize: 12,
                  color: "var(--wb-ink-body)",
                }}
              >
                {connectedLabels.map((label, i) => (
                  <React.Fragment key={label}>
                    {i > 0 && <span style={{ color: "var(--wb-border)" }}>·</span>}
                    <span>{label}</span>
                  </React.Fragment>
                ))}
              </div>
            </footer>
          )}
        </div>
      </section>
    </div>
  );
}

interface RenderedLayoutUnitProps {
  unit: LayoutUnit;
  docId: string;
  modelName: string;
  authority: AuthorityKind;
  modelRef?: string;
  lens: WorkbenchLens;
  expectedVersion: string | null;
  onCommitField: (path: string, value: unknown) => void;
  onSelectDoc: (id: string) => void;
  onInspectDiagram: (specId: string, nodeDoc?: string) => void;
  onOpenSource: (sourceDocId: string) => void;
  onHoverRef: (docId: string | null) => void;
}

const RenderedLayoutUnit: React.FC<RenderedLayoutUnitProps> = ({
  unit,
  docId,
  modelName,
  authority,
  modelRef,
  lens,
  expectedVersion,
  onCommitField,
  onSelectDoc,
  onInspectDiagram,
  onOpenSource,
  onHoverRef,
}) => {
  const isFierros = lens === "fierros";
  const saveSub = (editable: boolean) =>
    editable && expectedVersion ? (
      <div className="wb-marginal-gutter__sub">POST /save · expected {expectedVersion}</div>
    ) : null;

  if (unit.unit === "frontmatter") {
    return null;
  }

  if (unit.unit === "piece") {
    return (
      <CompositionTransclusionBlock
        piece={unit.segment}
        lens={lens}
        onSelectDoc={onSelectDoc}
        onOpenSource={onOpenSource}
        onHoverRef={onHoverRef}
      />
    );
  }

  if (unit.unit === "block") {
    const seg = unit.segment;
    // If the block has composition children, render each composition piece
    const compChildren = seg.children.filter(
      (c): c is CompositionPiece => c.type === "composition",
    );
    if (compChildren.length > 0) {
      return (
        <>
          {compChildren.map((piece, idx) => (
            <CompositionTransclusionBlock
              key={`${piece.path}-${idx}`}
              piece={piece}
              lens={lens}
              onSelectDoc={onSelectDoc}
              onOpenSource={onOpenSource}
              onHoverRef={onHoverRef}
            />
          ))}
        </>
      );
    }

    // Spec2Viz embedded projection block
    if (seg.projection) {
      return (
        <EmbeddedSpec2VizBlock
          segment={seg}
          projection={seg.projection}
          lens={lens}
          onInspectDiagram={onInspectDiagram}
        />
      );
    }

    // Structured table block
    if (seg.table_data) {
      return (
        <StructuredTableBlock
          segment={seg}
          tableData={seg.table_data}
          lens={lens}
          onSelectDoc={onSelectDoc}
        />
      );
    }

    // Editable or read-only prose field block
    const perm = resolveFieldAuthority(modelName, docId, seg.path, authority, modelRef);
    const canEdit = seg.editable && perm.allowed;
    return (
      <div
        className={
          isFierros
            ? `wb-block-with-gutter ${canEdit ? "wb-block-with-gutter--editable" : ""}`
            : "wb-block-with-gutter--lectura"
        }
      >
        {isFierros && (
          <div className="wb-marginal-gutter">
            field: {seg.path}
            {saveSub(canEdit)}
          </div>
        )}
        <InlineEditableProse
          value={String(seg.value ?? seg.text)}
          canEdit={canEdit}
          onCommit={(val) => onCommitField(seg.path, val)}
        />
      </div>
    );
  }

  if (unit.unit === "list") {
    return (
      <ul
        style={{
          margin: "0 0 24px 0",
          paddingLeft: 20,
          lineHeight: 1.65,
          color: "var(--wb-ink-body)",
        }}
      >
        {unit.items.map((itemPieces, idx) => (
          <li key={idx} style={{ marginBottom: 6 }}>
            <InlinePiecesRow
              pieces={itemPieces}
              docId={docId}
              modelName={modelName}
              authority={authority}
              modelRef={modelRef}
              onCommitField={onCommitField}
              onSelectDoc={onSelectDoc}
            />
          </li>
        ))}
      </ul>
    );
  }

  // unit.unit === "line"
  const { kind, pieces } = unit;
  const fieldInLine = pieces.find((p): p is { kind: "field"; segment: FieldSegment } => p.kind === "field");

  // Skip duplicating main H1 title if it matches the header
  if (kind.type === "heading" && kind.level === 1) {
    return null;
  }

  if (kind.type === "heading") {
    return (
      <h2
        className="wb-serif"
        style={{
          fontSize: kind.level === 2 ? 20 : 17,
          fontWeight: 500,
          color: "var(--wb-ink)",
          margin: "32px 0 12px 0",
          letterSpacing: "-0.01em",
        }}
      >
        <InlinePiecesRow
          pieces={pieces}
          docId={docId}
          modelName={modelName}
          authority={authority}
          modelRef={modelRef}
          onCommitField={onCommitField}
          onSelectDoc={onSelectDoc}
        />
      </h2>
    );
  }

  const hasEditableField = Boolean(
    fieldInLine?.segment.editable &&
      resolveFieldAuthority(modelName, docId, fieldInLine.segment.path, authority, modelRef).allowed,
  );

  return (
    <div
      className={
        isFierros
          ? `wb-block-with-gutter ${hasEditableField ? "wb-block-with-gutter--editable" : ""}`
          : "wb-block-with-gutter--lectura"
      }
      style={{
        borderLeftColor:
          isFierros && !fieldInLine ? "transparent" : undefined,
      }}
    >
      {isFierros && fieldInLine && (
        <div className="wb-marginal-gutter">
          field: {fieldInLine.segment.path}
          {saveSub(hasEditableField)}
        </div>
      )}
      <div
        style={{
          fontSize: 16,
          lineHeight: 1.68,
          color: "var(--wb-ink-body)",
        }}
      >
        <InlinePiecesRow
          pieces={pieces}
          docId={docId}
          modelName={modelName}
          authority={authority}
          modelRef={modelRef}
          onCommitField={onCommitField}
          onSelectDoc={onSelectDoc}
        />
      </div>
    </div>
  );
};

const InlinePiecesRow: React.FC<{
  pieces: InlinePiece[];
  docId: string;
  modelName: string;
  authority: AuthorityKind;
  modelRef?: string;
  onCommitField: (path: string, value: unknown) => void;
  onSelectDoc: (id: string) => void;
}> = ({ pieces, docId, modelName, authority, modelRef, onCommitField, onSelectDoc }) => {
  return (
    <>
      {pieces.map((piece, i) => {
        if (piece.kind === "text") {
          return <span key={i}>{piece.text}</span>;
        }
        const seg = piece.segment;
        const parsedRef = parseDocRef(seg.value ?? seg.text);
        if (parsedRef) {
          return (
            <button
              key={i}
              type="button"
              className="wb-chip"
              style={{ cursor: "pointer", margin: "0 2px" }}
              onClick={() => onSelectDoc(parsedRef.docId)}
            >
              {parsedRef.field ? `${parsedRef.docId}#${parsedRef.field}` : parsedRef.docId}
            </button>
          );
        }
        const perm = resolveFieldAuthority(modelName, docId, seg.path, authority, modelRef);
        const canEdit = seg.editable && perm.allowed;
        return (
          <InlineEditableProse
            key={i}
            value={String(seg.value ?? seg.text)}
            canEdit={canEdit}
            onCommit={(val) => onCommitField(seg.path, val)}
          />
        );
      })}
    </>
  );
};

const CompositionTransclusionBlock: React.FC<{
  piece: CompositionPiece;
  lens: WorkbenchLens;
  onSelectDoc: (id: string) => void;
  onOpenSource: (sourceDocId: string) => void;
  onHoverRef: (docId: string | null) => void;
}> = ({ piece, lens, onSelectDoc, onOpenSource, onHoverRef }) => {
  const { client } = useSldb();
  const parsedRef = parseDocRef(piece.ref);
  const childDocId = piece.source.doc
    ? piece.source.doc.includes(":")
      ? piece.source.doc.split(":")[1]!
      : piece.source.doc
    : parsedRef?.docId ?? "";
  const { data: childData, commit: commitChild } = useDocumentEditor(childDocId);
  // Sin describeModel resuelto no hay autoridad confirmada: la pieza queda de solo lectura.
  const [childContract, setChildContract] = useState<{
    model: string;
    authority: AuthorityKind;
    modelRef?: string;
  } | null>(null);

  useEffect(() => {
    if (!childData?.model) return;
    let active = true;
    const model = childData.model;
    client
      .describeModel(model)
      .then((desc: ModelDescription) => {
        if (!active) return;
        setChildContract({ model, authority: desc.authority ?? "authored", modelRef: desc.model_ref });
      })
      .catch(() => {
        /* ignore */
      });
    return () => {
      active = false;
    };
  }, [client, childData?.model]);

  // Resolve target field in order: explicit ref field -> body -> text -> cuerpo -> answer -> texto
  const targetField = useMemo(() => {
    const payload = childData?.payload ?? {};
    const candidates = [
      parsedRef?.field,
      piece.source.path,
      "body",
      "text",
      "cuerpo",
      "answer",
      "texto",
    ].filter((c): c is string => Boolean(c && c.trim()));
    for (const c of candidates) {
      if (typeof payload[c] === "string" && String(payload[c]).trim().length > 0) {
        return c;
      }
    }
    return candidates[0] ?? "body";
  }, [childData?.payload, parsedRef?.field, piece.source.path]);

  const quoteValue = useMemo(() => {
    const payload = childData?.payload ?? {};
    const v = payload[targetField];
    if (typeof v === "string" && v.trim()) return v;
    return piece.text.trim();
  }, [childData?.payload, targetField, piece.text]);

  const perm = useMemo(() => {
    if (!childData || !childContract || childContract.model !== childData.model) {
      return {
        allowed: false,
        authority: "authored" as AuthorityKind,
        owner: "local" as const,
        reason: "Autoridad del modelo sin confirmar (describeModel pendiente).",
      };
    }
    return resolveFieldAuthority(
      childData.model,
      childData.doc,
      targetField,
      childContract.authority,
      childContract.modelRef,
    );
  }, [childData, targetField, childContract]);

  const isFierros = lens === "fierros";
  const sourceRef = parseDocRef(
    childData?.payload?.source ?? childData?.payload?.fuente_ref,
  );

  return (
    <div
      className={isFierros ? "wb-block-with-gutter" : "wb-block-with-gutter--lectura"}
      onMouseEnter={() => onHoverRef(childDocId)}
      onMouseLeave={() => onHoverRef(null)}
    >
      {isFierros && (
        <div className="wb-marginal-gutter">
          transclude: {childDocId}#{targetField}
        </div>
      )}
      <div className="wb-transclusion-card">
        {isFierros && (
          <div className="wb-transclusion-card__header">
            <span>
              {childDocId}.md → #{targetField} ({childData?.model ?? piece.source.model ?? "AtomDoc"} ·{" "}
              {perm.allowed ? "editable in-place" : "read-only"})
            </span>
            <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
              {sourceRef && (
                <button
                  type="button"
                  className="wb-mono"
                  style={{
                    border: "none",
                    background: "transparent",
                    fontSize: 10,
                    color: "var(--wb-ink-muted)",
                    cursor: "pointer",
                  }}
                  onClick={() => onOpenSource(sourceRef.docId)}
                  title={`Ir a fuente ${sourceRef.docId}`}
                >
                  [{sourceRef.docId}]
                </button>
              )}
              <button
                type="button"
                className="wb-mono"
                style={{
                  border: "none",
                  background: "transparent",
                  fontSize: 11,
                  color: "var(--wb-ink-muted)",
                  cursor: "pointer",
                }}
                onClick={() => onSelectDoc(childDocId)}
                title={`Abrir ${childDocId}`}
              >
                ↗
              </button>
            </div>
          </div>
        )}
        <div className="wb-transclusion-card__quote">
          “
          <InlineEditableProse
            value={quoteValue}
            canEdit={perm.allowed}
            onCommit={(nextVal) => {
              if (childData) void commitChild({ doc: childData.id, model: childData.model }, targetField, nextVal);
            }}
          />
          ”
        </div>
      </div>
    </div>
  );
};

const EmbeddedSpec2VizBlock: React.FC<{
  segment: FieldSegment;
  projection: ResolvedNotationView;
  lens: WorkbenchLens;
  onInspectDiagram: (specId: string, nodeDoc?: string) => void;
}> = ({ segment, projection, lens, onInspectDiagram }) => {
  const { client } = useSldb();
  const [showRaw, setShowRaw] = useState(false);
  const [rawSource, setRawSource] = useState<
    { status: "loading" } | { status: "ready"; markdown: string } | { status: "error"; message: string } | null
  >(null);
  const isFierros = lens === "fierros";
  const specClean = projection.spec.includes(":")
    ? projection.spec.split(":")[1]!
    : projection.spec;

  useEffect(() => {
    if (!showRaw) return;
    let active = true;
    setRawSource({ status: "loading" });
    client
      .render(specClean)
      .then((markdown: string) => {
        if (active) setRawSource({ status: "ready", markdown });
      })
      .catch((err: unknown) => {
        if (active) setRawSource({ status: "error", message: err instanceof Error ? err.message : String(err) });
      });
    return () => {
      active = false;
    };
  }, [client, showRaw, specClean]);

  return (
    <div className={isFierros ? "wb-block-with-gutter" : "wb-block-with-gutter--lectura"}>
      {isFierros && (
        <div className="wb-marginal-gutter">
          spec2viz: {projection.diagram_type || projection.notation || segment.path}
        </div>
      )}
      <div
        style={{
          border: "1px solid var(--wb-hairline)",
          borderRadius: "var(--wb-radius)",
          backgroundColor: "var(--wb-stone)",
          padding: 16,
        }}
      >
        <div
          style={{
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            paddingBottom: 10,
            marginBottom: 12,
            borderBottom: "1px solid var(--wb-hairline)",
          }}
        >
          <div className="wb-mono" style={{ display: "flex", alignItems: "center", gap: 6 }}>
            <span
              style={{
                fontSize: 10,
                fontWeight: 500,
                textTransform: "uppercase",
                letterSpacing: "0.05em",
                color: "var(--wb-ink)",
              }}
            >
              {projection.title || specClean}
            </span>
            <span style={{ fontSize: 9, color: "var(--wb-ink-muted)" }}>· spec2viz-block</span>
          </div>
          <div className="wb-mono" style={{ fontSize: 10, display: "flex", alignItems: "center", gap: 8 }}>
            <button
              type="button"
              style={{
                border: "none",
                background: "transparent",
                fontFamily: "inherit",
                fontSize: 10,
                fontWeight: !showRaw ? 600 : 400,
                color: !showRaw ? "var(--wb-ink)" : "var(--wb-ink-muted)",
                cursor: "pointer",
              }}
              onClick={() => setShowRaw(false)}
            >
              [ Vista ]
            </button>
            <span style={{ color: "var(--wb-border)" }}>|</span>
            <button
              type="button"
              style={{
                border: "none",
                background: "transparent",
                fontFamily: "inherit",
                fontSize: 10,
                fontWeight: showRaw ? 600 : 400,
                color: showRaw ? "var(--wb-ink)" : "var(--wb-ink-muted)",
                cursor: "pointer",
              }}
              onClick={() => setShowRaw(true)}
            >
              Fuente YAML/MD
            </button>
            <span style={{ color: "var(--wb-border)" }}>|</span>
            <button
              type="button"
              style={{
                border: "none",
                background: "transparent",
                fontFamily: "inherit",
                fontSize: 10,
                color: "var(--wb-ink)",
                cursor: "pointer",
              }}
              onClick={() => onInspectDiagram(specClean)}
            >
              Inspeccionar ↗
            </button>
          </div>
        </div>

        <div
          style={{
            backgroundColor: "var(--wb-paper)",
            border: "1px solid var(--wb-hairline)",
            borderRadius: "var(--wb-radius)",
            padding: 12,
          }}
        >
          {showRaw ? (
            rawSource?.status === "ready" ? (
              <pre
                className="wb-mono"
                data-testid="spec2viz-raw-source"
                style={{ fontSize: 11, margin: 0, overflowX: "auto", whiteSpace: "pre-wrap" }}
              >
                {rawSource.markdown}
              </pre>
            ) : rawSource?.status === "error" ? (
              <div className="wb-mono" role="alert" style={{ fontSize: 11 }}>
                No se pudo leer el SpecDoc ({specClean}): {rawSource.message}
              </div>
            ) : (
              <div className="wb-mono" style={{ fontSize: 11, color: "var(--wb-ink-muted)" }}>
                Leyendo {specClean} desde SLDB…
              </div>
            )
          ) : (
            <NotationSvgCanvas
              view={projection}
              compact
              onSelectNode={(n) => onInspectDiagram(specClean, n.doc)}
            />
          )}
        </div>
      </div>
    </div>
  );
};

const StructuredTableBlock: React.FC<{
  segment: FieldSegment;
  tableData: SegmentTableData;
  lens: WorkbenchLens;
  onSelectDoc: (docId: string) => void;
}> = ({ segment, tableData, lens, onSelectDoc }) => {
  const isFierros = lens === "fierros";
  return (
    <div className={isFierros ? "wb-block-with-gutter" : "wb-block-with-gutter--lectura"}>
      {isFierros && <div className="wb-marginal-gutter">field: {segment.path}</div>}
      <div
        style={{
          border: "1px solid var(--wb-hairline)",
          borderRadius: "var(--wb-radius)",
          overflow: "hidden",
        }}
      >
        <div
          style={{
            backgroundColor: "var(--wb-stone)",
            padding: "8px 12px",
            borderBottom: "1px solid var(--wb-hairline)",
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
          }}
        >
          <span
            className="wb-mono"
            style={{
              fontSize: 10,
              textTransform: "uppercase",
              letterSpacing: "0.05em",
              color: "var(--wb-ink-muted)",
              fontWeight: 500,
            }}
          >
            {segment.path.replace(/_/g, " ")}
          </span>
          <span className="wb-mono" style={{ fontSize: 9, color: "var(--wb-ink-tertiary)" }}>
            {[segment.kind, segment.marker].filter(Boolean).join(" · ")}
          </span>
        </div>
        <table className="wb-table">
          <thead>
            <tr>
              {tableData.columns.map((col) => (
                <th key={col}>{col}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {tableData.rows.map((row, rIdx) => (
              <tr key={rIdx}>
                {tableData.columns.map((col) => {
                  const cellVal = String(row[col] ?? "");
                  const parsedRef = parseDocRef(cellVal);
                  return (
                    <td key={col}>
                      {parsedRef ? (
                        <span
                          className="wb-chip"
                          style={{ cursor: "pointer" }}
                          onClick={() => onSelectDoc(parsedRef.docId)}
                        >
                          {parsedRef.field
                            ? `${parsedRef.docId}#${parsedRef.field}`
                            : parsedRef.docId}
                        </span>
                      ) : (
                        cellVal
                      )}
                    </td>
                  );
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

const InlineEditableProse: React.FC<{
  value: string;
  canEdit: boolean;
  onCommit: (next: string) => void;
}> = ({ value, canEdit, onCommit }) => {
  const [editing, setEditing] = useState(false);
  const [draft, setDraft] = useState(value);

  useEffect(() => {
    setDraft(value);
  }, [value]);

  const confirm = () => {
    setEditing(false);
    const trimmed = draft.trim();
    if (trimmed && trimmed !== value) {
      onCommit(trimmed);
    } else {
      setDraft(value);
    }
  };

  // Un valor de varias líneas es Markdown del store (párrafos, listas, tablas GFM): se lee como tal.
  const multiline = value.includes("\n");
  const shown = multiline ? (
    <div className="wb-prose-md">
      <ReactMarkdown remarkPlugins={[remarkGfm]}>{value}</ReactMarkdown>
    </div>
  ) : (
    value
  );

  if (!canEdit) {
    return multiline ? shown : <span>{value}</span>;
  }

  if (!editing) {
    const Tag = multiline ? "div" : "span";
    return (
      <Tag
        role="button"
        tabIndex={0}
        onClick={() => setEditing(true)}
        onKeyDown={(e: React.KeyboardEvent) => {
          if (e.key === "Enter") setEditing(true);
        }}
        style={{ cursor: "text" }}
        title="Haz clic para editar in-situ (POST /save)"
      >
        {shown}
      </Tag>
    );
  }

  return (
    <textarea
      autoFocus
      rows={Math.max(2, draft.split("\n").length, Math.ceil(draft.length / 72))}
      className="wb-textarea"
      style={{
        fontFamily: "inherit",
        fontSize: "inherit",
        lineHeight: "inherit",
        backgroundColor: "var(--wb-card)",
        borderColor: "var(--wb-ink)",
      }}
      value={draft}
      onChange={(e) => setDraft(e.target.value)}
      onBlur={confirm}
      onKeyDown={(e) => {
        if (e.key === "Escape") {
          setDraft(value);
          setEditing(false);
        }
        if (e.key === "Enter" && (e.metaKey || e.ctrlKey)) {
          e.preventDefault();
          confirm();
        }
      }}
    />
  );
};
