/**
 * Vista Respuesta de la maqueta (`SLDB_ caso Levira, de fuentes a respuesta.html`, función `lp`): mismo
 * DOM, clases y textos; los datos son el `RespuestaDoc`, el informe y los átomos reales.
 * Diferencias conscientes: la nota "Redactada por…" dice lo que el dato `generadaPor` dice; las
 * verificaciones de reglas solo existen para p5 y p7 (el resto: "sin verificación automática"); "Enviar"
 * marca `estado: enviada` en el store (no hay canal de entrega).
 */
import { Fragment, useMemo, useState } from "react";
import { kindLabel } from "../../core/atoms";
import { atomsByBase, reglasDelPrompt, respuestaProvenance } from "../../core/caso";
import { reviewGate } from "../../core/atom-report";
import { SaveConflictError, SldbHttpError } from "../../core/client";
import {
  estadoLabel,
  frasesConEstado,
  includedIds,
  messageParagraphs,
  nuevosPorSlot,
  orderBases,
  pendientes,
  ruleResults,
  slotAtomIds,
  slotByName,
} from "../respuesta-logic";
import type { ViewProps } from "../ViewProps";
import "./respuesta.css";

function saveMessage(e: unknown): string {
  if (e instanceof SaveConflictError) return "El documento cambió en SLDB mientras tanto: se recargó, revisa y vuelve a intentar.";
  if (e instanceof SldbHttpError) return `No se pudo guardar (HTTP ${e.status}): ${e.message}`;
  return `No se pudo guardar: ${e instanceof Error ? e.message : String(e)}`;
}

export default function Respuesta({ store, fuentes, informe, respuesta, go }: ViewProps) {
  const [hoverAtom, setHoverAtom] = useState<string | null>(null);
  const [hoverFrase, setHoverFrase] = useState<number | null>(null);
  const [sending, setSending] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const { atoms, grupos } = store;

  const slot = useMemo(() => (respuesta ? slotByName(informe, respuesta.slot) : undefined), [informe, respuesta]);
  const model = useMemo(() => {
    if (!respuesta) return null;
    const prov = respuestaProvenance(respuesta, atoms);
    const included = includedIds(slot, atoms);
    // Sin el slot no se puede saber si una frase sigue vigente: no se marca ninguna stale (y se avisa).
    const frases = frasesConEstado(prov, included).map((f) => (slot ? f : { ...f, stale: false }));
    const idsDelSlot = slotAtomIds(slot, atoms);
    const bases = orderBases(atomsByBase(respuesta, atoms, idsDelSlot, grupos), fuentes);
    const reglas = ruleResults(reglasDelPrompt(respuesta, atoms, fuentes), frases);
    const nuevos = reviewGate(nuevosPorSlot(informe, atoms)).pending;
    const stale = frases.filter((f) => f.stale).length;
    const pend = pendientes(nuevos, stale);
    if (!slot) {
      pend.avisos.push(`El informe no tiene el slot “${respuesta.slot}”: no se puede saber si las frases siguen vigentes`);
      pend.canSend = false;
    }
    const missing = frases.flatMap((f) => f.missing.map((ref) => ({ ref, n: f.n })));
    return { frases, included, bases, reglas, pend, missing };
  }, [respuesta, atoms, slot, grupos, fuentes, informe]);

  if (!respuesta || !model) return <div className="mq-state">Este store no tiene una respuesta del asistente (RespuestaDoc).</div>;

  const { frases, included, bases, reglas, pend, missing } = model;
  const enviada = respuesta.estado === "enviada";
  const mensaje = fuentes.find((f) => f.id === respuesta.mensaje);
  const activeFrase = hoverFrase === null ? undefined : frases[hoverFrase];
  const faded = hoverFrase !== null || hoverAtom !== null;

  const send = async () => {
    setError(null);
    setSending(true);
    try {
      await store.saveField(respuesta.id, "estado", "enviada");
    } catch (e) {
      setError(saveMessage(e));
      void store.reload();
    } finally {
      setSending(false);
    }
  };

  return (
    <div className="flex h-full flex-col lg:flex-row">
      <section className="flex min-h-0 flex-1 flex-col bg-panel2" aria-label="Conversación con el paciente">
        <div className="flex items-center gap-3 border-b border-line bg-panel px-4 py-2 text-[13px]">
          <span className="font-semibold">{respuesta.title}</span>
          <span className="text-ink2">{estadoLabel(respuesta.estado)}</span>
          <button onClick={() => go("compositor")} className="ml-auto rounded border border-line px-2.5 py-1 hover:bg-panel2">
            Editar en el Compositor
          </button>
        </div>
        {error && (
          <div className="rp-error" role="alert">
            {error}
          </div>
        )}
        <div className="flex-1 overflow-auto px-4 py-6">
          <div className="mx-auto flex max-w-[60ch] flex-col gap-4 font-ui">
            <div className="max-w-[85%] self-start">
              <div className="mb-1 text-[12px] text-ink2">Paciente</div>
              <div className="rounded-2xl rounded-tl-sm border border-line bg-panel px-4 py-3 text-[15px] leading-relaxed">
                {mensaje ? (
                  messageParagraphs(mensaje.body).map((p, i) => (
                    <p key={i} className="mb-2 last:mb-0">
                      {p}
                    </p>
                  ))
                ) : (
                  <p className="text-ink2">No se encontró el mensaje de la paciente (fuente “{respuesta.mensaje}”).</p>
                )}
              </div>
            </div>
            <div className="max-w-[88%] self-end">
              <div className="mb-1 text-right text-[12px] text-ink2">Asistente Levira Contigo</div>
              <div className="rounded-2xl rounded-tr-sm px-4 py-3 text-[15px] leading-relaxed text-ink" style={{ background: "var(--hl)" }}>
                {frases.map((f, i) => {
                  const on = hoverFrase === i || (hoverAtom !== null && f.ids.includes(hoverAtom));
                  const dim = faded && !on;
                  return (
                    <Fragment key={i}>
                      <span
                        onMouseEnter={() => setHoverFrase(i)}
                        onMouseLeave={() => setHoverFrase(null)}
                        onClick={() => setHoverFrase(hoverFrase === i ? null : i)}
                        className="cursor-default rounded-sm transition-colors"
                        title={f.stale ? "Depende de átomos que ya no están en el slot" : undefined}
                        style={{
                          opacity: dim ? 0.35 : 1,
                          background: f.stale ? "var(--fresh)" : on ? "var(--panel)" : "transparent",
                          boxShadow: on ? "0 0 0 2px var(--panel)" : "none",
                          textDecoration: f.stale ? "underline wavy var(--t-pregunta)" : "none",
                        }}
                      >
                        {f.texto}
                      </span>{" "}
                    </Fragment>
                  );
                })}
              </div>
              <p className="mt-1 text-right text-[11.5px]" style={{ color: "var(--gen)" }}>
                Redactada por {respuesta.generadaPor || "un origen no indicado"}
                {slot ? ` desde el slot “${slot.titulo}”` : respuesta.slot ? ` desde el slot “${respuesta.slot}”` : ""}. Pasa el cursor por una frase para ver sus átomos.
              </p>
            </div>
          </div>
        </div>
      </section>
      <aside className="shrink-0 overflow-auto border-t border-line bg-panel p-4 text-[13.5px] lg:w-80 lg:border-l lg:border-t-0" aria-label="Verificación antes de enviar">
        <h2 className="text-[12px] font-semibold text-ink2">Átomos de la respuesta</h2>
        {bases.map((b) => (
          <div key={b.base} className="mt-3">
            <h3 className="mb-1 text-[12.5px] font-semibold">
              Base {b.title || "sin base"} <span className="font-normal text-ink2">({b.atoms.length})</span>
            </h3>
            <ul className="space-y-0.5">
              {b.atoms.map(({ atom, frases: ns }) => {
                const on = hoverAtom === atom.id || (activeFrase !== undefined && activeFrase.ids.includes(atom.id));
                return (
                  <li
                    key={atom.id}
                    onMouseEnter={() => setHoverAtom(atom.id)}
                    onMouseLeave={() => setHoverAtom(null)}
                    className={`group flex items-start gap-2 rounded px-1.5 py-1 transition-opacity ${on ? "bg-panel2" : ""}`}
                    style={{ opacity: faded && !on ? 0.35 : 1 }}
                  >
                    <span className={`tdot mt-1.5 bg-t-${atom.kind}`} title={kindLabel(atom.kind)} />
                    <span className={`flex-1 leading-snug ${included.has(atom.id) ? "" : "text-ink2 line-through"}`}>{atom.text}</span>
                    <span className="shrink-0 text-[11.5px] tabular-nums text-ink2 group-hover:hidden">{ns.length ? `frase ${ns.join(", ")}` : "sin usar"}</span>
                    <button onClick={() => go("extraccion", atom.id)} className="hidden shrink-0 text-[12px] text-accent hover:underline group-hover:inline">
                      Origen
                    </button>
                  </li>
                );
              })}
            </ul>
          </div>
        ))}
        {missing.length > 0 && (
          <div className="mt-3">
            <h3 className="mb-1 text-[12.5px] font-semibold">Referencias sin átomo</h3>
            <ul className="space-y-0.5">
              {missing.map((m, i) => (
                <li key={`${m.ref}-${i}`} className="flex items-start gap-2 px-1.5 py-1">
                  <span className="flex-1 leading-snug rp-missing">
                    átomo no encontrado <span className="text-ink2">({m.ref})</span>
                  </span>
                  <span className="shrink-0 text-[11.5px] tabular-nums text-ink2">frase {m.n}</span>
                </li>
              ))}
            </ul>
          </div>
        )}
        <h2 className="mt-6 text-[12px] font-semibold text-ink2">Reglas del system prompt</h2>
        {reglas.length === 0 ? (
          <p className="mt-2 text-ink2">Este caso no tiene reglas de system prompt.</p>
        ) : (
          <ul className="mt-2 space-y-2.5">
            {reglas.map(({ atom, check }) => (
              <li key={atom.id} className="flex gap-2.5">
                {check ? (
                  <span
                    className={`mt-0.5 flex h-5 w-5 shrink-0 items-center justify-center rounded-full text-[12px] font-bold ${check.ok ? "text-white" : "text-ink"}`}
                    style={{ background: check.ok ? "var(--t-criterio)" : "var(--fresh)" }}
                  >
                    {check.ok ? "✓" : "!"}
                  </span>
                ) : (
                  <span className="rp-nocheck" aria-hidden="true" />
                )}
                <span className="leading-snug">
                  {check ? check.label : atom.text}
                  <br />
                  {check ? <span className="text-[12px] text-ink2">{atom.text}</span> : <span className="rp-tag">sin verificación automática</span>}
                </span>
              </li>
            ))}
          </ul>
        )}
        <h2 className="mt-6 text-[12px] font-semibold text-ink2">Antes de enviar</h2>
        {pend.avisos.length ? (
          <ul className="mt-2 space-y-1.5">
            {pend.avisos.map((a) => (
              <li key={a} className="rounded px-2 py-1.5" style={{ background: "var(--fresh)" }}>
                {a}
              </li>
            ))}
          </ul>
        ) : (
          <p className="mt-2 text-ink2">Nada pendiente.</p>
        )}
        <button
          disabled={!pend.canSend || enviada || sending}
          onClick={() => void send()}
          title={pend.canSend ? undefined : pend.avisos.join(" · ")}
          className="mt-4 w-full rounded-md bg-ink px-3 py-2 font-semibold text-bg disabled:opacity-40"
        >
          {enviada ? "Enviada" : sending ? "Enviando…" : "Enviar al paciente"}
        </button>
        {!pend.canSend && (
          <button onClick={() => go("compositor")} className="mt-2 w-full text-center text-accent hover:underline">
            Resolver en el Compositor
          </button>
        )}
      </aside>
    </div>
  );
}
