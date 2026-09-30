/**
 * DESTILACIÓN · anchors → regularidad → modelo (§16.1).
 *
 * Es SOLO PROPUESTA. Lee los anchors del store, agrupa por referente y propone campos.
 * NO escribe: no genera archivos ni hace `POST`. SLDB no tiene endpoint de escritura de
 * modelos y no se inventa uno; el modelo lo revisa y lo escribe una persona.
 *
 * El tipo de un anchor no vive en un campo `kind` (este store no lo declara): está
 * dentro de `ref`, que es una s-expression tipada. Ver `core/distill.ts`.
 */
import { useEffect, useMemo, useState } from "react";
import { findAnchorModel } from "../core/anchors";
import { collectAnchors, distill, type ModelDraft, type ProposedField } from "../core/distill";
import { useDocuments, useSchema } from "../react/context";
import { hrefFor } from "./router";

const ROLE_LABEL: Record<ProposedField["role"], string> = {
  field: "campo",
  reference: "referencia",
  predicate: "predicado",
};

export function DistillView() {
  const [documents, reload] = useDocuments();
  const schema = useSchema();
  const [selected, setSelected] = useState<string | null>(null);
  const [copied, setCopied] = useState(false);

  const models = schema.status === "ready" ? schema.data.models : null;
  const anchorModel = useMemo(() => (models ? findAnchorModel(models) : null), [models]);
  const docs = documents.status === "ready" ? documents.data : null;
  const anchors = useMemo(() => (docs ? collectAnchors(docs, anchorModel?.id ?? null) : []), [docs, anchorModel]);
  const result = useMemo(() => distill(anchors), [anchors]);

  const current: ModelDraft | null = result.models.find((model) => model.model === selected) ?? result.models[0] ?? null;

  useEffect(() => setCopied(false), [current?.model]);

  const loading = documents.status === "loading" || schema.status === "loading";
  const error = documents.status === "error" ? documents.error : schema.status === "error" ? schema.error : null;

  const copyTemplate = async () => {
    if (!current?.template) return;
    try {
      await navigator.clipboard?.writeText(current.template);
      setCopied(true);
    } catch {
      setCopied(false);
    }
  };

  return (
    <div className="distill-view">
      <header className="doc-header">
        <div className="doc-header__id">
          <span className="doc-header__model">Destilación</span>
          <span className="doc-header__path">Anchors que se repiten → campos propuestos</span>
        </div>
        {docs && (
          <span className="save-status">
            {anchors.length} {anchors.length === 1 ? "anchor" : "anchors"}
          </span>
        )}
      </header>
      <div className="doc-body">
        <main className="page">
          {loading && <p className="sidebar__note">Leyendo anchors del store…</p>}
          {error && (
            <div className="banner banner--error" role="alert">
              No se pudo leer el store: {error}.{" "}
              <button type="button" className="link-btn" onClick={reload}>
                Reintentar
              </button>
            </div>
          )}

          {docs && anchors.length === 0 && (
            <section className="distill-empty">
              <h2 className="panel-title">Todavía no hay anchors que destilar</h2>
              <p>
                Esta vista lee los documentos <code>AnchorDoc</code>, los agrupa por el referente de su <code>ref</code> y propone los campos de un
                modelo. Un anchor declara un símbolo, un <code>ref</code> tipado y un <code>motive</code>; cuando varios apuntan al mismo referente, eso
                es regularidad.
              </p>
              <p>
                El store tiene {docs.length} documentos y ninguno es un anchor. El camino para poblarlo es la vista{" "}
                <a href={hrefFor({ view: "lector" })}>Lector</a>: pegá un texto crudo, seleccioná un tramo y guardá un anchor.
              </p>
              <p className="inspector__note">
                Recordá: la destilación <strong>no escribe nada</strong>. Propone; el modelo lo escribe una persona.
              </p>
            </section>
          )}

          {docs && anchors.length > 0 && result.models.length === 0 && (
            <section className="distill-empty">
              <h2 className="panel-title">Ningún anchor propone un campo</h2>
              <p>
                Hay {anchors.length} {anchors.length === 1 ? "anchor" : "anchors"}, pero ninguno nombra un campo, una relación o un predicado
                reconocible.
              </p>
              {result.unbacked.length > 0 && (
                <p className="inspector__note">
                  {result.unbacked.length} sin <code>motive</code>: un campo sin razón escrita no se propone, porque no es auditable.
                </p>
              )}
              {result.unparsed.length > 0 && (
                <p className="inspector__note">{result.unparsed.length} con un <code>ref</code> que no se pudo tipar.</p>
              )}
            </section>
          )}

          {docs && result.models.length > 0 && (
            <>
              <section aria-label="Modelos candidatos">
                <h2 className="panel-title">
                  Modelos candidatos <span className="sidebar__count">{result.models.length}</span>
                </h2>
                <p className="health-help">
                  Agrupados por el modelo objetivo del <code>ref</code>. Los <code>(field M f)</code> son campos de <code>M</code>; los{" "}
                  <code>(relation R)</code> son candidatos a <code>__references__</code>; los <code>(where M …)</code> son predicados, no campos.
                </p>
                <ul className="distill-candidates">
                  {result.models.map((model) => (
                    <li key={model.model}>
                      <button
                        type="button"
                        className={`distill-candidate${model.model === current?.model ? " is-active" : ""}`}
                        aria-pressed={model.model === current?.model}
                        onClick={() => setSelected(model.model)}
                      >
                        <span className="distill-candidate__name">{model.model}</span>
                        <span className="distill-candidate__meta">
                          {model.fields.length} {model.fields.length === 1 ? "campo" : "campos"}
                          {model.references.length > 0 && ` · ${model.references.length} ref`}
                          {model.predicates.length > 0 && ` · ${model.predicates.length} pred`}
                        </span>
                      </button>
                    </li>
                  ))}
                </ul>
              </section>

              {current && (
                <section className="distill-draft" aria-label={`Borrador ${current.model}`}>
                  <h2 className="panel-title">
                    Borrador · {current.model}
                  </h2>
                  <ProposalList title="Campos" role="field" proposals={current.fields} empty="Ningún anchor nombra un campo de este modelo." />
                  <ProposalList title="Referencias" role="reference" proposals={current.references} empty="Ningún anchor nombra una relación de este modelo." />
                  <ProposalList title="Predicados (no son campos)" role="predicate" proposals={current.predicates} empty="Sin predicados." />

                  <h3 className="panel-subtitle">__template__ sugerido</h3>
                  {current.template ? (
                    <>
                      <pre className="reader-preview distill-template">{current.template}</pre>
                      <button type="button" className="btn" onClick={() => void copyTemplate()}>
                        {copied ? "Copiado" : "Copiar borrador"}
                      </button>
                      <p className="inspector__note">
                        Es el frontmatter: las posiciones de los campos. El cuerpo no se propone. Un anchor no guarda posición, así que
                        "posición estable" no es observable desde acá; el proxy es que el modelo tenga dos o más campos.
                      </p>
                    </>
                  ) : (
                    <p className="inspector__note">
                      Sin template: hace falta más de un campo propuesto para que haya posiciones que declarar.
                    </p>
                  )}
                </section>
              )}
            </>
          )}
        </main>
        <aside className="inspector">
          <p className="inspector__note">
            <strong>Solo propuesta.</strong> Esta vista no escribe: no crea archivos ni hace <code>POST</code>. El modelo lo revisa una persona y lo
            escribe ella.
          </p>
          <p className="inspector__note">
            El <strong>motive</strong> de cada anchor viaja con el campo que justifica. Es lo que hace auditable la destilación (§16.1): no es
            inferencia estadística, es una razón escrita. Un campo sin motivo no se propone.
          </p>
          <p className="inspector__note">
            El <strong>tipo</strong> de un anchor no es un campo: vive dentro de <code>ref</code>, que es una s-expression tipada. El primer átomo
            (<code>field</code>, <code>relation</code>, <code>where</code>, …) es el tipo. También se leen los refs viejos en string.
          </p>
          {docs && result.models.length > 0 && (
            <p className="inspector__note">
              Leídos: {anchors.length} anchors · {result.models.length} modelos candidatos
              {result.unbacked.length > 0 && ` · ${result.unbacked.length} sin motive`}
              {result.unparsed.length > 0 && ` · ${result.unparsed.length} sin tipar`}.
            </p>
          )}
        </aside>
      </div>
    </div>
  );
}

function ProposalList({
  title,
  role,
  proposals,
  empty,
}: {
  title: string;
  role: ProposedField["role"];
  proposals: ProposedField[];
  empty: string;
}) {
  return (
    <section className="distill-proposals" aria-label={title}>
      <h3 className="panel-subtitle">
        {title} {proposals.length > 0 && <span className="sidebar__count">{proposals.length}</span>}
      </h3>
      {proposals.length === 0 ? (
        <p className="inspector__note">{empty}</p>
      ) : (
        <ul className="distill-fields">
          {proposals.map((proposal) => (
            <li key={proposal.name} className="distill-field">
              <div className="distill-field__head">
                <span className="distill-field__name">{proposal.name}</span>
                <span className={`distill-role distill-role--${role}`}>{ROLE_LABEL[role]}</span>
                <span className="distill-field__symbol">símbolo: {proposal.symbol || "—"}</span>
              </div>
              <p className="distill-field__motive">{proposal.motive}</p>
              <span className="distill-field__refs">
                {proposal.sources.map((source) => (
                  <a key={source.doc} className="distill-source" href={hrefFor({ view: "doc", id: source.doc, mode: "document" })}>
                    {source.doc}
                  </a>
                ))}
              </span>
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}
