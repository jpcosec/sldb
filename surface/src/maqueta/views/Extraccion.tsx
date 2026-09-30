/**
 * Extracción de la maqueta (`SLDB_ extracción, grafo y compositor.html`), portada 1:1: mismo DOM,
 * clases, textos y comportamiento; el texto se pinta con ProseMirror de solo lectura + decoraciones.
 * Difiere en los datos: párrafos = `acta.body.split("\n\n")`, átomos reales, escrituras por `store`.
 */
import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { Plugin, PluginKey, EditorState } from "prosemirror-state";
import { EditorView, Decoration, DecorationSet } from "prosemirror-view";
import { Schema } from "prosemirror-model";
import { paragraphsOf } from "../../core/atom-text";
import { nextAtomName, repairAnchor, selectionToAtomPayload } from "../../core/atoms";
import { SaveConflictError } from "../../core/client";
import type { AtomKind } from "../../core/contract";
import { toMockAtoms, type MockAtom } from "../adapter";
import { anchorKinds, highlightRanges, orderAtoms, selectionToBodyRange, type AnchorKind, type HighlightRange } from "../extraccion-logic";
import type { ViewProps } from "../ViewProps";
import "./extraccion.css";

/** Etiquetas de tipo (`gn` en la maqueta). */
const KINDS: Record<AtomKind, string> = { entidad: "Entidad", hecho: "Hecho", decision: "Decisión", pendiente: "Pendiente", riesgo: "Riesgo" };

const schema = new Schema({
  nodes: { doc: { content: "paragraph+" }, paragraph: { content: "text*", toDOM: () => ["p", 0] }, text: {} },
});
const anchorsKey = new PluginKey<{ ranges: HighlightRange[]; focus: string[] }>("anchors");

function decorationsFor(doc: Parameters<typeof DecorationSet.create>[0], ranges: HighlightRange[], focus: string[]) {
  const sorted = [...ranges].sort((o, i) => i.to - i.from - (o.to - o.from));
  return DecorationSet.create(
    doc,
    sorted.map((o) =>
      Decoration.inline(o.from, o.to, {
        class: `anc t-${o.type}${o.draft ? " is-draft" : ""}${focus.includes(o.id) ? " is-focus" : ""}`,
        style: `--layer:${o.layer}`,
        "data-atom": o.id,
      }),
    ),
  );
}

function Confidence({ v }: { v: number }) {
  const low = v < 0.7;
  return (
    <span className="flex items-center gap-1.5" title={`Confianza del extractor: ${Math.round(v * 100)} %`}>
      <span className="relative h-1 w-10 rounded-full bg-line overflow-hidden">
        <span className={`absolute inset-y-0 left-0 ${low ? "bg-t-pendiente" : "bg-ink2"}`} style={{ width: `${v * 100}%` }} />
      </span>
      <span className={`text-[11px] tabular-nums ${low ? "tx-t-pendiente font-semibold" : "text-ink2"}`}>{Math.round(v * 100)}</span>
    </span>
  );
}

interface WriteError {
  message: string;
  conflict: boolean;
}

interface CardProps {
  atom: MockAtom;
  anchor: AnchorKind;
  active: boolean;
  busy: boolean;
  error: WriteError | undefined;
  onHover(id: string | null): void;
  onFocus(id: string): void;
  onUpdate(id: string, patch: { type?: AtomKind; status?: "confirmado" }): void;
  onDiscard(id: string): void;
  onRepair(id: string): void;
  onReload(id: string): void;
}

function AtomCard({ atom: e, anchor, active, busy, error, onHover, onFocus, onUpdate, onDiscard, onRepair, onReload }: CardProps) {
  const [open, setOpen] = useState(false);
  const low = e.conf < 0.7;
  return (
    <article
      onMouseEnter={() => onHover(e.id)}
      onMouseLeave={() => onHover(null)}
      onClick={() => onFocus(e.id)}
      aria-busy={busy || undefined}
      className={`group relative rounded-md border-l-[3px] bl-t-${e.type} bg-panel border border-line px-3 pt-2.5 pb-2 cursor-pointer transition-shadow
        ${active ? "shadow-[0_6px_20px_-8px_rgba(20,30,40,.35)] ring-1 ring-accent/40" : ""} ${low ? "bg-fresh/40" : ""}`}
    >
      <div className="flex items-center justify-between gap-2 mb-1">
        <div className="relative">
          <button
            disabled={busy}
            onClick={(u) => {
              u.stopPropagation();
              setOpen(!open);
            }}
            className={`text-[12px] font-semibold tx-t-${e.type} hover:underline`}
            aria-haspopup="menu"
          >
            {KINDS[e.type]} ▾
          </button>
          {open && (
            <div role="menu" className="absolute z-20 mt-1 w-36 rounded-md border border-line bg-panel shadow-lg py-1">
              {(Object.entries(KINDS) as [AtomKind, string][]).map(([u, c]) => (
                <button
                  key={u}
                  role="menuitem"
                  onClick={(d) => {
                    d.stopPropagation();
                    setOpen(false);
                    if (u !== e.type) onUpdate(e.id, { type: u });
                  }}
                  className="flex w-full items-center gap-2 px-3 py-1.5 text-[13px] hover:bg-panel2"
                >
                  <span className={`tdot bg-t-${u}`} />
                  {c}
                </button>
              ))}
            </div>
          )}
        </div>
        <Confidence v={e.conf} />
      </div>
      <p className="text-[14.5px] leading-snug text-ink">{e.text}</p>
      <div className="mt-2 flex flex-wrap gap-1">
        {e.tags.map((u) => (
          <span key={u} className="rounded bg-panel2 border border-line px-1.5 py-px text-[11.5px] text-ink2">
            {u}
          </span>
        ))}
      </div>
      <p className="mt-2 rounded bg-panel2 px-2 py-1 font-doc text-[12.5px] italic text-ink2 line-clamp-1">
        “{e.anchor[1]}”
      </p>
      {anchor === "drifted" && (
        <div className="ext-note">
          <strong>Ancla movida</strong>
          <span>el texto se desplazó</span>
          <button
            disabled={busy}
            onClick={(u) => {
              u.stopPropagation();
              onRepair(e.id);
            }}
          >
            Reparar
          </button>
        </div>
      )}
      {anchor === "orphan" && (
        <div className="ext-note is-orphan">
          <strong>El texto cambió</strong>
          <span>la cita ya no está en el acta</span>
        </div>
      )}
      {error && (
        <div className="ext-err" role="alert">
          <span>{error.message}</span>
          {error.conflict && (
            <button
              onClick={(u) => {
                u.stopPropagation();
                onReload(e.id);
              }}
            >
              Recargar
            </button>
          )}
        </div>
      )}
      <div className="mt-2 flex items-center gap-3 text-[12px]">
        {e.status === "confirmado" ? (
          <span className="text-ink2">Confirmado</span>
        ) : (
          <button
            disabled={busy}
            onClick={(u) => {
              u.stopPropagation();
              onUpdate(e.id, { status: "confirmado" });
            }}
            className="font-semibold text-accent hover:underline"
          >
            Confirmar
          </button>
        )}
        <button
          disabled={busy}
          onClick={(u) => {
            u.stopPropagation();
            onDiscard(e.id);
          }}
          className="text-ink2 hover:text-ink hover:underline"
        >
          Descartar
        </button>
        <span className="ml-auto text-ink2 opacity-0 group-hover:opacity-100">Arrastra sobre otra para fusionar</span>
      </div>
    </article>
  );
}

interface Selection {
  from: number;
  to: number;
  text: string;
  top: number;
  left: number;
}

export default function Extraccion({ store, acta, focusId: o, setFocusId }: ViewProps) {
  const body = acta.body;
  const host = useRef<HTMLDivElement>(null);
  const view = useRef<EditorView | null>(null);
  const [a, setHover] = useState<string | null>(null);
  const [c, setSel] = useState<Selection | null>(null);
  const [selMsg, setSelMsg] = useState<string | null>(null);
  const [f, setLowFirst] = useState(false);
  const [h, setFilter] = useState<AtomKind | null>(null);
  const [busy, setBusy] = useState<Set<string>>(new Set());
  const [errors, setErrors] = useState<Record<string, WriteError>>({});

  const setFocusRef = useRef(setFocusId);
  setFocusRef.current = setFocusId;

  const all = useMemo(() => toMockAtoms(store.atoms, acta), [store.atoms, acta]);
  const e = useMemo(() => all.filter((x) => x.status !== "descartado"), [all]);
  const n = useMemo(() => all.filter((x) => x.status === "descartado"), [all]);
  const w = useMemo(() => highlightRanges(body, e), [body, e]);
  const anchors = useMemo(() => anchorKinds(body, e), [body, e]);
  const m = a ? [a] : o ? [o] : [];

  // Editor de solo lectura: se recrea sólo si cambia el texto del acta.
  useEffect(() => {
    const paras = paragraphsOf(body);
    if (!host.current || paras.length === 0) return;
    const doc = schema.node("doc", null, paras.map((p) => schema.node("paragraph", null, [schema.text(p.text)])));
    const plugin = new Plugin({
      key: anchorsKey,
      state: { init: () => ({ ranges: [], focus: [] }), apply: (tr, prev) => tr.getMeta(anchorsKey) || prev },
      props: {
        decorations: (s) => decorationsFor(s.doc, anchorsKey.getState(s)!.ranges, anchorsKey.getState(s)!.focus),
        handleDOMEvents: {
          mouseover: (_v, ev) => {
            const t = (ev.target as HTMLElement).closest?.("[data-atom]") as HTMLElement | null;
            setHover(t ? t.dataset.atom ?? null : null);
            return false;
          },
          mouseleave: () => {
            setHover(null);
            return false;
          },
          click: (_v, ev) => {
            const t = (ev.target as HTMLElement).closest?.("[data-atom]") as HTMLElement | null;
            if (t) setFocusRef.current(t.dataset.atom ?? null);
            return false;
          },
        },
      },
      filterTransaction: (tr) => !tr.docChanged,
    });
    const b: EditorView = new EditorView(host.current, {
      state: EditorState.create({ doc, plugins: [plugin] }),
      attributes: { spellcheck: "false" },
      dispatchTransaction(tr) {
        b.updateState(b.state.apply(tr));
        if (tr.selectionSet) setSelMsg(null);
        const { from, to, empty } = b.state.selection;
        if (empty) setSel(null);
        else {
          let bottom = 0;
          let left = 0;
          try {
            const L = b.coordsAtPos(to);
            bottom = L.bottom;
            left = L.left;
          } catch {
            /* sin geometría (jsdom) */
          }
          const T = host.current!.getBoundingClientRect();
          setSel({ from, to, text: b.state.doc.textBetween(from, to), top: bottom - T.top + 6, left: Math.min(left - T.left, T.width - 190) });
        }
      },
    });
    view.current = b;
    return () => {
      b.destroy();
      view.current = null;
    };
  }, [body]);

  useEffect(() => {
    const k = view.current;
    if (!k) return;
    const E = w.filter((b) => !h || e.find((S) => S.id === b.id)!.type === h);
    k.dispatch(k.state.tr.setMeta(anchorsKey, { ranges: E, focus: m }));
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [w, a, o, h, body]);

  useEffect(() => {
    if (!o || !view.current) return;
    const k = w.find((b) => b.id === o);
    if (!k) return;
    const E = view.current.domAtPos(k.from).node;
    ((E.nodeType === 3 ? E.parentElement : E) as HTMLElement | null)?.scrollIntoView?.({ block: "center", behavior: "smooth" });
    document.getElementById(`card-${o}`)?.scrollIntoView?.({ block: "nearest", behavior: "smooth" });
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [o, body]);

  /** Escribe campos de un átomo: deshabilita su tarjeta mientras guarda y muestra el fallo si lo hay. */
  const write = useCallback(
    async (id: string, fn: () => Promise<unknown>) => {
      setBusy((s) => new Set(s).add(id));
      setErrors((x) => {
        const { [id]: _drop, ...rest } = x;
        return rest;
      });
      try {
        await fn();
      } catch (err) {
        const conflict = err instanceof SaveConflictError;
        setErrors((x) => ({
          ...x,
          [id]: { conflict, message: conflict ? "El átomo cambió en el servidor; recarga para ver la versión actual." : `No se pudo guardar: ${(err as Error).message}` },
        }));
      } finally {
        setBusy((s) => {
          const next = new Set(s);
          next.delete(id);
          return next;
        });
      }
    },
    [],
  );

  const y = async () => {
    if (!c) return;
    const sel = selectionToBodyRange(body, c.from, c.to);
    if (!sel.ok) {
      setSelMsg(sel.reason);
      return;
    }
    setSelMsg(null);
    const name = nextAtomName(store.atoms.map((x) => x.id));
    try {
      const res = await store.createAtom(name, selectionToAtomPayload(body, sel.from, sel.to, "hecho", acta.gid));
      setSel(null);
      setFocusId(res?.id ?? name);
    } catch (err) {
      setSelMsg(`No se pudo crear el átomo: ${(err as Error).message}`);
    }
  };

  const g = orderAtoms(e, w, h, f);
  const v = e.filter((k) => k.status !== "confirmado").length;

  return (
    <div className="flex h-full flex-col">
      <div className="flex flex-wrap items-center gap-x-4 gap-y-2 border-b border-line bg-panel px-4 py-2 text-[13px]">
        <span className="text-ink2">
          {e.length} átomos, {v} sin confirmar
        </span>
        <div className="flex flex-wrap gap-1" role="group" aria-label="Filtrar por tipo">
          {(Object.entries(KINDS) as [AtomKind, string][]).map(([k, E]) => (
            <button
              key={k}
              onClick={() => setFilter(h === k ? null : k)}
              aria-pressed={h === k}
              className={`flex items-center gap-1.5 rounded px-2 py-0.5 border ${h === k ? "border-ink bg-panel2" : "border-transparent hover:bg-panel2"}`}
            >
              <span className={`tdot bg-t-${k}`} />
              {E}
            </button>
          ))}
        </div>
        <label className="flex items-center gap-1.5 text-ink2">
          <input type="checkbox" checked={f} onChange={(k) => setLowFirst(k.target.checked)} className="accent-[var(--accent)]" />
          Baja confianza primero
        </label>
        <button
          disabled
          className="ext-disabled ml-auto rounded border border-line px-2.5 py-1 hover:bg-panel2"
          title="Falta el extractor: aún no hay un modelo de extracción conectado al servidor"
        >
          Re-extraer lo no confirmado
        </button>
      </div>
      <div className="flex min-h-0 flex-1 flex-col overflow-auto lg:flex-row lg:overflow-hidden">
        <section className={`relative lg:min-h-0 lg:overflow-auto px-5 py-6 sm:px-10 lg:basis-2/3 ${m.length ? "dim" : ""}`} aria-label="Texto fuente">
          <div ref={host} className="relative">
            {c && !selMsg && (
              <button
                onMouseDown={(k) => k.preventDefault()}
                onClick={() => void y()}
                style={{ top: c.top, left: Math.max(0, c.left) }}
                className="absolute z-10 rounded-md bg-ink px-3 py-1.5 text-[13px] font-semibold text-bg shadow-lg"
              >
                Crear átomo desde la selección
              </button>
            )}
            {c && selMsg && (
              <div className="ext-msg" role="alert" style={{ top: c.top, left: Math.max(0, c.left) }}>
                {selMsg}
              </div>
            )}
          </div>
          <p className="mt-4 max-w-[68ch] text-[12.5px] text-ink2">
            Línea continua: confirmado. Línea punteada: propuesto por el modelo. Varias líneas bajo un tramo: varios átomos anclados ahí.
          </p>
        </section>
        <aside className="lg:min-h-0 lg:overflow-auto border-t border-line bg-panel2 p-3 lg:basis-1/3 lg:border-l lg:border-t-0" aria-label="Átomos">
          <div className="flex flex-col gap-2.5">
            {g.map((k) => (
              <div key={k.id} id={`card-${k.id}`}>
                <AtomCard
                  atom={k}
                  anchor={anchors.get(k.id) ?? "intact"}
                  active={m.includes(k.id)}
                  busy={busy.has(k.id)}
                  error={errors[k.id]}
                  onHover={setHover}
                  onFocus={(id) => setFocusId(id === o ? null : id)}
                  onUpdate={(id, patch) =>
                    void write(id, () => (patch.type ? store.saveField(id, "kind", patch.type) : store.saveField(id, "status", patch.status)))
                  }
                  onDiscard={(id) => void write(id, () => store.saveField(id, "status", "descartado"))}
                  onRepair={(id) =>
                    void write(id, async () => {
                      const fixed = repairAnchor(body, k.atom);
                      if (!fixed) return;
                      // Se escribe primero el extremo que mantiene start <= end en el paso intermedio.
                      const forward = fixed.start > k.atom.start;
                      if (forward) {
                        await store.saveField(id, "end", fixed.end);
                        await store.saveField(id, "start", fixed.start);
                      } else {
                        await store.saveField(id, "start", fixed.start);
                        await store.saveField(id, "end", fixed.end);
                      }
                    })
                  }
                  onReload={(id) => {
                    setErrors((x) => {
                      const { [id]: _drop, ...rest } = x;
                      return rest;
                    });
                    void store.reload();
                  }}
                />
              </div>
            ))}
          </div>
          {n.length > 0 && (
            <details className="mt-4 rounded-md border border-dashed border-line p-3 text-[13px]">
              <summary className="cursor-pointer text-ink2">Descartados ({n.length})</summary>
              {n.map((k) => (
                <div key={k.id} id={`card-${k.id}`} className={`mt-2 flex items-center justify-between gap-2 ${busy.has(k.id) ? "ext-busy" : ""}`}>
                  <span className="text-ink2 line-through">{k.text}</span>
                  {errors[k.id] && (
                    <span className="ext-err" role="alert">
                      {errors[k.id]!.message}
                      {errors[k.id]!.conflict && <button onClick={() => void store.reload()}>Recargar</button>}
                    </span>
                  )}
                  <button
                    disabled={busy.has(k.id)}
                    className="text-accent hover:underline"
                    onClick={() => void write(k.id, () => store.saveField(k.id, "status", "propuesto"))}
                  >
                    Restaurar
                  </button>
                </div>
              ))}
            </details>
          )}
        </aside>
      </div>
    </div>
  );
}
