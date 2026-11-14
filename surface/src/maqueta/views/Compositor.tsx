/**
 * Compositor de la maqueta (`SLDB_ extracción, grafo y compositor.html`, función `Kp`): mismo DOM,
 * clases y textos; los datos son el `InformeAvanceDoc` real y las acciones se persisten con `saveField`.
 * Diferencias conscientes (ver el reporte): prosa unida sin modelo, "Agregar sección" deshabilitado,
 * "Agregar filtro" abre un desplegable, aviso de errores de guardado.
 */
import { Fragment, useMemo, useState, type ReactNode } from "react";
import { acceptAtom, excludeAtom, kindLabel, pinAtom, SLOT_MODES, unexcludeAtom, unpinAtom } from "../../core/atoms";
import {
  nextVersion,
  publicationName,
  publicationPayload,
  buildPreview,
  publicationsOf,
  PUBLICATION_MODEL,
  publishState,
  removeQueryToken,
  reviewGate,
  slotChanges,
  slotField,
  snapshotAtoms,
} from "../../core/atom-report";
import { SaveConflictError } from "../../core/client";
import type { Atom, InformeSlot, SlotMode } from "../../core/contract";
import { useSldb } from "../../react/context";
import {
  addQueryFilter,
  filterChips,
  filterOptions,
  FILTER_KINDS,
  isIncluded,
  newBySlot,
  OLD_SLOT_ROTULOS,
  queryOptions,
  slotItems,
  STATE_LABELS,
  type CardState,
  type FilterKind,
} from "../compositor-logic";
import type { ViewProps } from "../ViewProps";
import "./compositor.css";

const MODE_LABEL: Record<SlotMode, string> = { viñetas: "viñetas", prosa: "prosa", tabla: "tabla" };

const sentence = (text: string) => {
  const t = text.trim();
  return /[.!?…]$/.test(t) ? t : `${t}.`;
};

/** Frase clicable del documento final (`x` en la maqueta). */
function Piece({ ids, selected, onOpen, children }: { ids: string[]; selected: string[] | null; onOpen(ids: string[]): void; children: ReactNode }) {
  return (
    <span
      role="button"
      tabIndex={0}
      onClick={() => onOpen(ids)}
      onKeyDown={(e) => e.key === "Enter" && onOpen(ids)}
      className={`cursor-pointer rounded-sm decoration-[var(--accent)] underline-offset-4 hover:underline ${selected && ids.some((v) => selected.includes(v)) ? "underline" : ""}`}
    >
      {children}
    </span>
  );
}

export default function Compositor({ store, informe, go }: ViewProps) {
  const { client } = useSldb();
  const { atoms, edges, documents, grupos, relationTypes, saveField, reload } = store;

  const [selName, setSel] = useState<string | null>(null);
  const [origin, setOrigin] = useState<string[] | null>(null);
  const [drafts, setDrafts] = useState<Record<string, string | undefined>>({});
  const [adding, setAdding] = useState<{ kind: FilterKind; value: string } | null>(null);
  const [busy, setBusy] = useState(false);
  const [publishing, setPublishing] = useState(false);
  const [failure, setFailure] = useState<string | null>(null);

  const byPath = useMemo(() => new Map(atoms.map((a) => [a.path, a])), [atoms]);
    const qopts = useMemo(() => queryOptions(atoms, grupos), [atoms, grupos]);
  const nuevosBySlot = useMemo(() => (informe ? newBySlot(informe, atoms, edges, qopts) : null), [informe, atoms, edges, qopts]);

  if (!informe || !nuevosBySlot || informe.slotList.length === 0) return <div className="mq-state">El store no tiene ningún informe con slots.</div>;
  const slotList = informe.slotList;
  const sel = slotList.some((s) => s.name === selName) ? selName! : slotList[0]!.name;
  const entry = slotList.find((s) => s.name === sel)!;
  const rotuloOf = (e: { name: string; rotulo: string }) => e.rotulo || OLD_SLOT_ROTULOS[e.name] || "";

  const title = typeof informe.payload.title === "string" && informe.payload.title ? informe.payload.title : `Informe ${informe.id}`;
  const slotOf = (name: string) => slotList.find((s) => s.name === name)!;
  const itemsOf = (name: string) => slotItems(slotOf(name), nuevosBySlot[name] ?? []);
  const includedOf = (name: string) => itemsOf(name).filter((i) => isIncluded(i.state)).flatMap((i) => (byPath.get(i.path) ? [byPath.get(i.path)!] : []));
  /** Tabla: encabezados y evidencia del núcleo, sobre lo que entra al documento. */
  const previews = buildPreview(
    slotList.map((s) => ({ ...s, atomos: includedOf(s.name).map((a) => a.path) })),
    atoms,
    edges,
  );
  const gate = reviewGate(nuevosBySlot);
  const h = gate.pending;
  const publications = publicationsOf(documents, informe.id);
  const publish = publishState({ gate, publications, atomCount: snapshotAtoms(slotList).length, publishing });

  const slot: InformeSlot = entry;
  const items = itemsOf(sel);
  const queryText = drafts[sel] ?? slot.query;
  const chips = filterChips(queryText, qopts);
  const openOrigin = (atom: Atom) => go("extraccion", atom.id);

  /** Ejecuta escrituras; si el servidor las rechaza se muestra el error y se relee. */
  async function run(work: () => Promise<void>): Promise<boolean> {
    setBusy(true);
    setFailure(null);
    try {
      await work();
      return true;
    } catch (error) {
      setFailure(error instanceof SaveConflictError ? "El informe cambió en SLDB desde que lo abriste; no se escribió nada." : (error as Error).message);
      await reload();
      return false;
    } finally {
      setBusy(false);
    }
  }

  async function write(field: string, value: unknown) {
    const result = await saveField(informe!.id, field, value);
    if (!result.ok) throw new Error(result.error ?? "El servidor rechazó el cambio.");
  }

  const change = (name: string, next: InformeSlot) =>
    run(async () => {
      for (const c of slotChanges(name, slotOf(name), next)) await write(c.field, c.value);
    });

  const decide = (path: string, fn: (s: InformeSlot, p: string) => InformeSlot) => void change(sel, fn(slot, path));

  async function saveQuery(name: string, text: string) {
    if (text === slotOf(name).query) {
      setDrafts((d) => ({ ...d, [name]: undefined }));
      return;
    }
    if (await run(() => write(slotField(name, "query"), text))) setDrafts((d) => ({ ...d, [name]: undefined }));
  }

  const setMode = (modo: SlotMode) => {
    if (modo !== slot.modo) void run(() => write(slotField(sel, "modo"), modo));
  };

  /** Foto inmutable: render real + versiones frescas; si otro publicó a la vez (409) relee y reintenta una vez. */
  async function publishNow() {
    setPublishing(true);
    setFailure(null);
    const attempt = async () => {
      const [docs, markdown] = await Promise.all([client.documents(), client.render(informe!.id)]);
      const version = nextVersion(publicationsOf(docs, informe!.id));
      return client.createDocument(PUBLICATION_MODEL, publicationName(informe!.id, version), publicationPayload({ informe: informe!, version, markdown }));
    };
    try {
      try {
        await attempt();
      } catch (error) {
        if (!(error instanceof SaveConflictError)) throw error;
        await attempt();
      }
    } catch (error) {
      setFailure(error instanceof SaveConflictError ? "Otra publicación ganó de mano dos veces; vuelve a intentarlo." : `No se pudo publicar: ${(error as Error).message}`);
    } finally {
      await reload();
      setPublishing(false);
    }
  }

  const choicesFor = (kind: FilterKind) => filterOptions(kind, { atoms, grupos, relationTypes });

  const renderSection = (name: string, mode: SlotMode) => {
    const list = includedOf(name);
    if (!list.length) return <p className="text-[14px] italic text-ink2">Este slot todavía no tiene átomos.</p>;
    const piece = (ids: string[], text: string) => (
      <Piece ids={ids} selected={origin} onOpen={setOrigin}>
        {text}
      </Piece>
    );
    if (mode === "prosa")
      return (
        <div className="border-l-2 pl-3" style={{ borderColor: "var(--gen)" }}>
          <p className="text-[15.5px] leading-relaxed">
            {list.map((a) => (
              <Fragment key={a.path}>
                {piece([a.path], sentence(a.text))}{" "}
              </Fragment>
            ))}
          </p>
          <p className="mt-1 text-[11.5px]" style={{ color: "var(--gen)" }}>
            Vista previa unida, no redactada por un modelo
          </p>
        </div>
      );
    if (mode === "tabla") {
      const pv = previews.find((x) => x.slot === name)!;
      return (
        <div className="overflow-x-auto">
          <table className="w-full text-left text-[14px]">
            <thead>
              <tr className="border-b border-line text-[12px] text-ink2">
                <th className="py-1 pr-3 font-semibold">{pv.headers[0]}</th>
                <th className="py-1 font-semibold">{pv.headers[1]}</th>
              </tr>
            </thead>
            <tbody>
              {list.map((a, i) => (
                <tr key={a.path} className="border-b border-line/60 align-top">
                  <td className="py-1.5 pr-3">{piece([a.path], a.text)}</td>
                  <td className="py-1.5 text-ink2">{pv.items[i]?.evidence}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      );
    }
    return (
      <ul className="list-disc space-y-1 pl-5 text-[15px] leading-relaxed marker:text-ink2">
        {list.map((a) => (
          <li key={a.path}>{piece([a.path], a.text)}</li>
        ))}
      </ul>
    );
  };

  const originAtoms = origin ? origin.flatMap((p) => (byPath.get(p) ? [byPath.get(p)!] : [])) : [];

  return (
    <div className="flex h-full flex-col">
      <div className="flex flex-wrap items-center gap-3 border-b border-line bg-panel px-4 py-2 text-[13px]">
        <span className="font-semibold">{title}</span>
        <span className="text-ink2">{publish.published}.</span>
        {h > 0 && (
          <span className="rounded px-2 py-0.5 text-ink" style={{ background: "var(--fresh)" }}>
            Desde entonces: {h} {h === 1 ? "átomo nuevo" : "átomos nuevos"} por revisar
          </span>
        )}
        <button
          className="ml-auto rounded-md bg-ink px-3 py-1 font-semibold text-bg disabled:opacity-40"
          disabled={!publish.enabled || busy}
          title={publish.reason}
          onClick={() => void publishNow()}
        >
          {publish.label}
        </button>
      </div>
      {failure && (
        <div className="cmp-notice" role="alert">
          <span>{failure}</span>
          <button onClick={() => setFailure(null)}>Cerrar</button>
        </div>
      )}
      <div className="flex min-h-0 flex-1 flex-col overflow-auto lg:flex-row lg:overflow-hidden">
        <nav className="shrink-0 border-b border-line bg-panel p-3 lg:w-56 lg:border-b-0 lg:border-r" aria-label="Esqueleto del documento">
          <h2 className="mb-2 text-[12px] font-semibold text-ink2">Esqueleto</h2>
          <ol className="flex gap-1 overflow-x-auto lg:block lg:space-y-0.5">
            {slotList.map((e, idx) => {
              const name = e.name;
              const count = includedOf(name).length;
              const hasNew = (nuevosBySlot[name] ?? []).length > 0;
              return (
                <li className="shrink-0" key={name}>
                  <button
                    onClick={() => setSel(name)}
                    aria-current={sel === name}
                    className={`flex w-full items-center gap-2 rounded px-2 py-1.5 text-left text-[13.5px] ${sel === name ? "bg-panel2 font-semibold" : "hover:bg-panel2"}`}
                  >
                    <span className="tabular-nums text-ink2">{idx + 1}.</span>
                    <span className="flex-1">{e.titulo}</span>
                    {hasNew && <span className="h-2 w-2 rounded-full bg-t-pregunta" title="Tiene átomos nuevos sin revisar" />}
                    <span className="text-[11.5px] tabular-nums text-ink2">{count}</span>
                  </button>
                </li>
              );
            })}
          </ol>
          <button
            className="mt-2 hidden w-full rounded border border-dashed border-line px-2 py-1.5 text-left text-[13px] text-ink2 hover:text-ink lg:block"
            disabled
            title="Las secciones las define el tipo de informe"
          >
            Agregar sección
          </button>
        </nav>
        <section className="lg:min-h-0 lg:overflow-auto border-b border-line bg-panel2 p-4 lg:basis-[42%] lg:border-b-0 lg:border-r" aria-label="Slot seleccionado">
          <h2 className="text-[12px] font-semibold text-ink2">{entry.titulo}</h2>
          <p className="text-[16px] font-semibold">{rotuloOf(entry)}</p>
          <label className="mt-3 block text-[12px] font-semibold text-ink2" htmlFor="q">
            Qué va en este slot
          </label>
          <input
            id="q"
            value={queryText}
            placeholder="base:paciente tag:asistente tipo:regla distancia:1 relacion:activa texto libre"
            onChange={(e) => setDrafts((d) => ({ ...d, [sel]: e.target.value }))}
            onBlur={(e) => void saveQuery(sel, e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && e.currentTarget.blur()}
            className="mt-1 w-full rounded-md border border-line bg-panel px-3 py-2 text-[14px]"
          />
          <div className="mt-2 flex flex-wrap gap-1.5 text-[12.5px]">
            {chips.map((c) => (
              <span
                key={`${c.index}-${c.label}`}
                className={`flex items-center gap-1 rounded border border-line bg-panel px-2 py-0.5${c.active ? "" : " opacity-60"}`}
                title={c.active ? undefined : "Este filtro no se aplica"}
              >
                <span className="text-ink2">{c.prefix}:</span> {c.value}
                <button
                  className="ml-0.5 text-ink2 hover:text-ink"
                  aria-label={`Quitar filtro ${c.prefix}`}
                  onClick={() => {
                    const next = removeQueryToken(queryText, c.index);
                    setDrafts((d) => ({ ...d, [sel]: next }));
                    void saveQuery(sel, next);
                  }}
                >
                  ✕
                </button>
              </span>
            ))}
            <button className="rounded border border-dashed border-line px-2 py-0.5 text-ink2 hover:text-ink" aria-expanded={!!adding} onClick={() => setAdding(adding ? null : { kind: "tipo", value: choicesFor("tipo")[0]?.value ?? "" })}>
              Agregar filtro
            </button>
            {adding && (
              <span className="cmp-pop" role="group" aria-label="Nuevo filtro">
                <select
                  aria-label="Filtrar por"
                  value={adding.kind}
                  onChange={(e) => {
                    const kind = e.target.value as FilterKind;
                    setAdding({ kind, value: choicesFor(kind)[0]?.value ?? "" });
                  }}
                >
                  {FILTER_KINDS.map((f) => (
                    <option key={f.kind} value={f.kind}>
                      {f.label}
                    </option>
                  ))}
                </select>
                <select aria-label="Valor del filtro" value={adding.value} onChange={(e) => setAdding({ ...adding, value: e.target.value })}>
                  {choicesFor(adding.kind).map((o) => (
                    <option key={o.value} value={o.value}>
                      {o.label}
                    </option>
                  ))}
                </select>
                <button
                  disabled={!adding.value}
                  onClick={() => {
                    const next = addQueryFilter(queryText, adding.kind, adding.value);
                    setDrafts((d) => ({ ...d, [sel]: next }));
                    setAdding(null);
                    void saveQuery(sel, next);
                  }}
                >
                  Agregar
                </button>
                <button aria-label="Cancelar filtro" onClick={() => setAdding(null)}>
                  ✕
                </button>
              </span>
            )}
          </div>
          <div className="mt-4 flex items-center gap-2 text-[12.5px]">
            <span className="text-ink2">Presentar como</span>
            <div className="flex overflow-hidden rounded-md border border-line" role="radiogroup">
              {SLOT_MODES.map((m) => (
                <button key={m} role="radio" aria-checked={slot.modo === m} disabled={busy} onClick={() => setMode(m)} className={`px-2.5 py-1 ${slot.modo === m ? "bg-ink text-bg" : "bg-panel hover:bg-panel2"}`}>
                  {MODE_LABEL[m]}
                </button>
              ))}
            </div>
          </div>
          <h3 className="mt-5 text-[12px] font-semibold text-ink2">Átomos ({items.length})</h3>
          <ul className="mt-2 space-y-2">
            {items.map(({ path, state }: { path: string; state: CardState }) => {
              const g = byPath.get(path);
              const v = origin?.includes(path);
              return (
                <li
                  key={path}
                  className={`rounded-md border border-l-[3px] ${g ? `bl-t-${g.kind}` : ""} px-3 py-2 ${state === "excluido" ? "border-line bg-panel opacity-60" : "border-line bg-panel"} ${v ? "ring-2 ring-accent" : ""}`}
                  style={state === "nuevo" ? { background: "var(--fresh)" } : {}}
                >
                  <div className="flex items-center justify-between gap-2 text-[11.5px]">
                    <span className={`font-semibold ${state === "nuevo" ? "text-ink" : "text-ink2"}`}>
                      {state === "pin" ? "\u{1F4CC} " : ""}
                      {STATE_LABELS[state]}
                    </span>
                    {g && <span className={`tx-t-${g.kind}`}>{kindLabel(g.kind)}</span>}
                  </div>
                  <p className={`mt-0.5 text-[14px] leading-snug ${state === "excluido" ? "line-through" : ""}`}>{g ? g.text : `Átomo no encontrado: ${path}`}</p>
                  <div className="mt-1.5 flex gap-3 text-[12.5px]">
                    {state === "nuevo" && (
                      <>
                        <button className="font-semibold text-accent hover:underline" disabled={busy} onClick={() => decide(path, acceptAtom)}>
                          Aceptar
                        </button>
                        <button className="text-ink2 hover:underline" disabled={busy} onClick={() => decide(path, excludeAtom)}>
                          Excluir
                        </button>
                      </>
                    )}
                    {state === "regla" && (
                      <>
                        {g && (
                          <button className="text-ink2 hover:underline" disabled={busy} onClick={() => decide(path, pinAtom)}>
                            Fijar
                          </button>
                        )}
                        <button className="text-ink2 hover:underline" disabled={busy} onClick={() => decide(path, excludeAtom)}>
                          Excluir
                        </button>
                      </>
                    )}
                    {state === "pin" && (
                      <button className="text-ink2 hover:underline" disabled={busy} onClick={() => decide(path, unpinAtom)}>
                        Soltar pin
                      </button>
                    )}
                    {state === "excluido" && (
                      <button className="text-ink2 hover:underline" disabled={busy} onClick={() => decide(path, unexcludeAtom)}>
                        Volver a incluir
                      </button>
                    )}
                    {g && (
                      <button className="ml-auto text-ink2 hover:underline" onClick={() => openOrigin(g)}>
                        Origen
                      </button>
                    )}
                  </div>
                </li>
              );
            })}
          </ul>
        </section>
        <article className="lg:min-h-0 flex-1 lg:overflow-auto bg-panel px-6 py-6" aria-label="Documento final">
          <div className="mx-auto max-w-[62ch] font-doc">
            <h1 className="text-[26px] font-semibold leading-tight">{title}</h1>
            {slotList.map((e) => e.name).map((name) => (
              <section key={name} onClick={() => setSel(name)} className={`mt-6 rounded-md transition-colors ${sel === name ? "outline outline-1 outline-offset-8 outline-line" : ""}`}>
                <h2 className="mb-2 text-[18px] font-semibold">{slotOf(name).titulo}</h2>
                {renderSection(name, slotOf(name).modo)}
                {(nuevosBySlot[name] ?? []).length > 0 && <p className="mt-2 font-ui text-[12px] text-ink2">Hay átomos nuevos que calzan con este slot. No entran hasta que los revises.</p>}
              </section>
            ))}
            <p className="mt-6 font-ui text-[12px] text-ink2">El documento guardado en disco siempre renderiza viñetas; prosa y tabla son solo vista previa.</p>
          </div>
          {origin && (
            <div className="sticky bottom-0 mx-auto mt-6 max-w-[62ch] rounded-md border border-line bg-panel2 p-3 font-ui text-[13px] shadow-lg">
              <div className="flex items-start justify-between gap-3">
                <div>
                  <p className="font-semibold">Viene de {origin.length === 1 ? "1 átomo" : `${origin.length} átomos`}</p>
                  {originAtoms.map((a) => (
                    <p className="mt-1 text-ink2" key={a.path}>
                      <span className="text-ink">{a.text}</span>. Ancla: <span className="font-doc italic">“{a.quote || "sin cita"}”</span>
                    </p>
                  ))}
                </div>
                <button onClick={() => setOrigin(null)} className="text-ink2 hover:text-ink" aria-label="Cerrar origen">
                  ✕
                </button>
              </div>
              {originAtoms[0] && (
                <button onClick={() => openOrigin(originAtoms[0]!)} className="mt-2 font-semibold text-accent hover:underline">
                  Abrir en Extracción
                </button>
              )}
            </div>
          )}
        </article>
      </div>
    </div>
  );
}
