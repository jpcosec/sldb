/**
 * BANDEJA · lo anotado sin ubicar (§6.4).
 *
 * La propuesta pide sugerir destino por similitud y vecindad. `Corpus.rank()` no
 * está servido por HTTP (§5) y `/graph/neighborhood` devuelve solo el nodo
 * consultado en este store: la bandeja LISTA pero no SUGIERE, y lo dice. No se
 * simula un ranking con una heurística inventada.
 */
import { useMemo, useState } from "react";
import { collectTray, groupByModel, type TrayEntry, type TrayReason } from "../core/tray";
import { useDocuments, useSchema } from "../react/context";
import { hrefFor } from "./router";

const REASON_LABEL: Record<TrayReason, string> = {
  "sin-procedencia": "sin procedencia",
  "marcado-borrador": "marcado borrador",
};

export function TrayView() {
  const [documents, reload] = useDocuments();
  const schema = useSchema();
  const [only, setOnly] = useState<TrayReason | "todas">("todas");

  const docs = documents.status === "ready" ? documents.data : null;
  const schemaIndex = schema.status === "ready" ? schema.data : null;

  const entries = useMemo(() => (docs ? collectTray(docs, schemaIndex) : []), [docs, schemaIndex]);
  const filtered = useMemo(() => (only === "todas" ? entries : entries.filter((e) => e.reasons.includes(only))), [entries, only]);
  const groups = useMemo(() => groupByModel(filtered), [filtered]);

  const loading = documents.status === "loading" || schema.status === "loading";
  const error = documents.status === "error" ? documents.error : null;

  return (
    <div className="tray-view">
      <header className="doc-header">
        <div className="doc-header__id">
          <span className="doc-header__model">Bandeja</span>
          <span className="doc-header__path">Documentos anotados que todavía no tienen lugar</span>
        </div>
        {docs && (
          <span className="save-status">
            {entries.length} {entries.length === 1 ? "sin ubicar" : "sin ubicar"}
          </span>
        )}
      </header>
      <div className="doc-body">
        <main className="page">
          {loading && <p className="sidebar__note">Leyendo el store…</p>}
          {error && (
            <div className="banner banner--error" role="alert">
              No se pudo leer el store: {error}.{" "}
              <button type="button" className="link-btn" onClick={reload}>
                Reintentar
              </button>
            </div>
          )}
          {docs && (
            <>
              <div className="tray-filters" role="group" aria-label="Filtrar por motivo">
                {(["todas", "sin-procedencia", "marcado-borrador"] as const).map((key) => (
                  <button
                    key={key}
                    type="button"
                    className={`tray-filter${only === key ? " is-active" : ""}`}
                    aria-pressed={only === key}
                    onClick={() => setOnly(key)}
                  >
                    {key === "todas" ? "Todas" : REASON_LABEL[key]}
                    <span className="sidebar__count">
                      {key === "todas" ? entries.length : entries.filter((e) => e.reasons.includes(key)).length}
                    </span>
                  </button>
                ))}
              </div>

              {filtered.length === 0 ? (
                <p className="inspector__note">
                  {entries.length === 0
                    ? "Nada sin ubicar: todos los documentos que declaran procedencia la tienen."
                    : "Ningún documento cae en este motivo."}
                </p>
              ) : (
                groups.map((group) => (
                  <section key={group.model} className="tray-group" aria-label={group.model}>
                    <h2 className="panel-title">
                      {group.model} <span className="sidebar__count">{group.entries.length}</span>
                    </h2>
                    <ul className="tray-list">
                      {group.entries.map((entry) => (
                        <TrayCard key={entry.doc} entry={entry} />
                      ))}
                    </ul>
                  </section>
                ))
              )}
            </>
          )}
        </main>
        <aside className="inspector">
          <p className="inspector__note">
            Un documento entra a la bandeja si su modelo declara <code>provenance</code> y lo tiene vacío, o si está tageado como borrador. Si el
            modelo no declara procedencia, el documento no aparece: la regla no le aplica.
          </p>
          <p className="inspector__note">
            <strong>Todavía no sugiere destino.</strong> Eso necesita ranking por similitud (<code>Corpus.rank()</code>), que no está servido por
            HTTP, y vecindad de grafo, que en este store devuelve solo el nodo consultado.
          </p>
        </aside>
      </div>
    </div>
  );
}

function TrayCard({ entry }: { entry: TrayEntry }) {
  return (
    <li className="tray-card">
      <div className="tray-card__head">
        <a className="tray-card__title" href={hrefFor({ view: "doc", id: entry.doc, mode: "document" })} title={entry.path}>
          {entry.title}
        </a>
        <span className="tray-card__reasons">
          {entry.reasons.map((reason) => (
            <span key={reason} className={`tray-tag tray-tag--${reason}`}>
              {REASON_LABEL[reason]}
            </span>
          ))}
        </span>
      </div>
      {entry.excerpt && <p className="tray-card__excerpt">{entry.excerpt}</p>}
      <span className="tray-card__path">{entry.path}</span>
    </li>
  );
}
