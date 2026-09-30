/**
 * Vista Grafo de la maqueta (`SLDB_ caso Levira, de fuentes a respuesta.html`, función `om`), portada
 * a TSX con el DOM, las clases y el comportamiento de la maqueta: bases de conocimiento con sus
 * subgrupos anidados, plegado, aristas azules entre bases y creación de relaciones. Los datos y las
 * escrituras van al `sldb serve` real (lo que no depende de React está en `../grafo-logic.ts`).
 */
import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import {
  Background,
  Controls,
  Handle,
  MarkerType,
  Position,
  ReactFlow,
  type Connection,
  type Edge as FlowEdge,
  type FinalConnectionState,
  type Node as FlowNode,
  type NodeProps,
} from "@xyflow/react";
import { NO_GROUP, nextRelationName, relationPayloadBetween } from "../../core/atom-graph";
import { GROUP_MODEL, groupInfosFromDocuments, groupSlug, isAlreadyExists } from "../../core/atom-groups";
import { atomRelationTypes, inGroup, kindLabel } from "../../core/atoms";
import { groupTitle } from "../../core/caso";
import { toMockAtoms, toMockRelations, type MockAtom } from "../adapter";
import {
  cellTagOf,
  computeLayout,
  edgeSides,
  expandRelations,
  foldedBasePosition,
  foldedCellPosition,
  fuseEdges,
  groupNodeId,
  groupOf,
  isGroupNodeId,
  nodeCenter,
  planConnection,
  readingOrder,
  regionClass,
  relationsOfAtom,
  tagOfNodeId,
  typeLabel,
} from "../grafo-logic";
import type { ViewProps } from "../ViewProps";
import "./grafo.css";

const SIDES = [
  ["t", Position.Top],
  ["r", Position.Right],
  ["b", Position.Bottom],
  ["l", Position.Left],
] as const;

const handles = (
  <>
    {SIDES.map(([k, pos]) => (
      <Handle key={"s" + k} id={"s-" + k} type="source" position={pos} />
    ))}
    {SIDES.map(([k, pos]) => (
      <Handle key={"t" + k} id={"t-" + k} type="target" position={pos} />
    ))}
  </>
);

interface AtomData {
  atom: MockAtom;
  dimmed: boolean;
  selected: boolean;
  [k: string]: unknown;
}
interface RegionData {
  level: "kb" | "g";
  label: string;
  cls: string | null;
  onFold(): void;
  [k: string]: unknown;
}
interface FoldedData {
  level: "kb" | "g";
  label: string;
  cls: string | null;
  counts: Record<string, number>;
  internal: number;
  selected: boolean;
  onUnfold(): void;
  [k: string]: unknown;
}

function AtomNode({ data }: NodeProps<FlowNode<AtomData>>) {
  const t = data.atom;
  return (
    <div
      className={`w-[210px] rounded-md border border-line border-l-[3px] bl-t-${t.type} bg-panel px-2.5 py-2 text-left shadow-sm transition-opacity
      ${data.dimmed ? "opacity-25" : ""} ${data.selected ? "ring-2 ring-accent" : ""}`}
    >
      {handles}
      <div className={`text-[10.5px] font-semibold tx-t-${t.type}`}>{kindLabel(t.type)}</div>
      <div className="font-ui text-[12.5px] leading-snug text-ink line-clamp-2">{t.text}</div>
    </div>
  );
}

function RegionNode({ data }: NodeProps<FlowNode<RegionData>>) {
  const kb = data.level === "kb";
  return (
    <div
      className={`h-full w-full ${kb ? "rounded-2xl border border-line" : "rounded-lg border border-dashed border-ink2/30"}${kb && !data.cls ? " mq-graf-region-neutro" : ""}`}
      style={kb && data.cls ? { background: `var(--region-${data.cls})` } : {}}
    >
      {handles}
      <div className={`flex items-center justify-between font-ui ${kb ? "px-4 pt-2.5" : "px-2.5 pt-1.5"}`}>
        <span className={kb ? "text-[15px] font-semibold text-ink" : "text-[12px] font-semibold text-ink2"}>{data.label}</span>
        <button
          onClick={(e) => {
            e.stopPropagation();
            data.onFold();
          }}
          className="nodrag rounded px-1.5 text-[12px] text-ink2 hover:bg-panel hover:text-ink"
        >
          Plegar
        </button>
      </div>
    </div>
  );
}

function FoldedNode({ data }: NodeProps<FlowNode<FoldedData>>) {
  const total = Object.values(data.counts).reduce((a, b) => a + b, 0);
  return (
    <div
      onDoubleClick={data.onUnfold}
      className={`w-[210px] rounded-xl bg-panel px-3 py-2.5 font-ui shadow-md ${data.level === "kb" ? "border-2 border-ink/70" : "border border-ink/40"} ${data.selected ? "ring-2 ring-accent" : ""}${data.cls ? "" : " mq-graf-folded-neutro"}`}
      style={data.cls ? { backgroundImage: `linear-gradient(var(--region-${data.cls}),var(--region-${data.cls}))` } : {}}
    >
      {handles}
      <div className="flex items-baseline justify-between gap-2">
        <span className="text-[14px] font-semibold text-ink">{data.label}</span>
        <span className="text-[12px] text-ink2 tabular-nums">{total}</span>
      </div>
      <div className="mt-2 flex h-1.5 overflow-hidden rounded-full">
        {Object.entries(data.counts).map(([k, n]) => (
          <span key={k} className={`bg-t-${k}`} style={{ width: `${(n / total) * 100}%` }} />
        ))}
      </div>
      <div className="mt-1.5 text-[11px] text-ink2">{data.internal} relaciones internas. Doble clic para desplegar.</div>
    </div>
  );
}

const nodeTypes = { atom: AtomNode, region: RegionNode, folded: FoldedNode };

const countKinds = (list: MockAtom[]): Record<string, number> =>
  list.reduce<Record<string, number>>((acc, a) => ({ ...acc, [a.type]: (acc[a.type] || 0) + 1 }), {});

interface Notice {
  tone: "error" | "ok";
  text: string;
}

export default function Grafo(props: ViewProps) {
  const { store, fuentes, focusId, setFocusId, go } = props;

  const atoms = useMemo(
    () => readingOrder(toMockAtoms(store.atoms.filter((a) => a.status !== "descartado"), fuentes), fuentes),
    [store.atoms, fuentes],
  );
  const relations = useMemo(() => toMockRelations(store.edges, store.atoms), [store.edges, store.atoms]);
  const types = useMemo(() => atomRelationTypes(store.relationTypes).map((t) => t.name), [store.relationTypes]);
  const grupos = useMemo(() => groupInfosFromDocuments(store.documents), [store.documents]);

  const [folded, setFolded] = useState<Record<string, boolean>>({});
  const [hidden, setHidden] = useState<string[]>([]);
  const [tag, setTag] = useState<string | null>(null);
  const [selGroup, setSelGroup] = useState<string | null>(null);
  const [hoverEdge, setHoverEdge] = useState<string | null>(null);
  const [chosen, setChosen] = useState("activa");
  const [notice, setNotice] = useState<Notice | null>(null);
  const busy = useRef(false);
  const dragFrom = useRef<string | null>(null);

  const newType = types.includes(chosen) ? chosen : (types[0] ?? chosen);
  const foldedSet = useMemo(() => new Set(Object.keys(folded).filter((k) => folded[k])), [folded]);
  const toggle = (id: string, to?: boolean) => setFolded((m) => ({ ...m, [id]: to ?? !m[id] }));

  const layout = useMemo(() => computeLayout(atoms), [atoms]);
  const byId = useMemo(() => new Map(atoms.map((a) => [a.id, a])), [atoms]);

  /** Título de display de una base o subgrupo (el `GrupoDoc` si existe). */
  const groupLabel = useCallback((t: string): string => (t === NO_GROUP ? "Sin grupo" : groupTitle(t, grupos)), [grupos]);

  // El átomo enfocado despliega la base y el subgrupo plegados que lo contienen.
  useEffect(() => {
    const a = focusId ? byId.get(focusId) : undefined;
    if (!a) return;
    const base = groupOf(a);
    const cell = cellTagOf(a);
    setFolded((m) => (m[base] || (cell && m[cell]) ? { ...m, [base]: false, ...(cell ? { [cell]: false } : {}) } : m));
  }, [focusId, byId]);

  const flat = useMemo(() => expandRelations(relations, atoms), [relations, atoms]);
  const internalOf = (ids: Set<string>) => flat.filter((f) => ids.has(f.source) && ids.has(f.target) && !f.inherited).length;

  const nodes = useMemo(() => {
    const out: FlowNode[] = [];
    layout.bases.forEach((base, bi) => {
      const g = base.tag;
      const cls = regionClass(g, bi);
      const inBase = atoms.filter((a) => groupOf(a) === g);
      const label = g === NO_GROUP ? "Sin grupo" : `Base: ${groupLabel(g)}`;
      if (folded[g]) {
        out.push({
          id: groupNodeId(g),
          type: "folded",
          position: foldedBasePosition(base),
          data: { level: "kb", label, cls, counts: countKinds(inBase), internal: internalOf(new Set(inBase.map((a) => a.id))), selected: selGroup === g, onUnfold: () => toggle(g, false) } satisfies FoldedData,
        });
        return;
      }
      out.push({
        id: groupNodeId(g),
        type: "region",
        position: { x: base.x, y: base.y },
        style: { width: base.w, height: base.h },
        selectable: false,
        data: { level: "kb", label, cls, onFold: () => toggle(g, true) } satisfies RegionData,
      });
      const atomNode = (a: MockAtom): FlowNode => {
        const p = layout.atoms[a.id]!;
        const dimmed = tag !== null && !(tag === NO_GROUP ? a.tags.length === 0 : inGroup(a, tag));
        return { id: a.id, type: "atom", parentId: p.parent, extent: "parent", position: { x: p.x, y: p.y }, data: { atom: a, dimmed, selected: focusId === a.id } satisfies AtomData };
      };
      for (const cell of base.cells) {
        if (cell.tag === null) {
          cell.atomIds.forEach((id) => out.push(atomNode(byId.get(id)!)));
          continue;
        }
        const ct = cell.tag;
        const inCell = cell.atomIds.map((id) => byId.get(id)!);
        if (folded[ct]) {
          out.push({
            id: groupNodeId(ct),
            type: "folded",
            parentId: groupNodeId(g),
            extent: "parent",
            position: foldedCellPosition(cell),
            data: { level: "g", label: groupLabel(ct), cls: null, counts: countKinds(inCell), internal: internalOf(new Set(cell.atomIds)), selected: selGroup === ct, onUnfold: () => toggle(ct, false) } satisfies FoldedData,
          });
          continue;
        }
        out.push({
          id: groupNodeId(ct),
          type: "region",
          parentId: groupNodeId(g),
          extent: "parent",
          position: { x: cell.x, y: cell.y },
          style: { width: 250, height: cell.h },
          selectable: false,
          data: { level: "g", label: groupLabel(ct), cls: null, onFold: () => toggle(ct, true) } satisfies RegionData,
        });
        inCell.forEach((a) => out.push(atomNode(a)));
      }
    });
    return out;
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [atoms, layout, folded, tag, focusId, selGroup, flat, groupLabel, byId]);

  const edges = useMemo(() => {
    return fuseEdges(flat, atoms, foldedSet, hidden).flatMap((f): FlowEdge[] => {
      const a = nodeCenter(f.source, layout, foldedSet);
      const b = nodeCenter(f.target, layout, foldedSet);
      if (!a || !b) return [];
      const [sa, sb] = edgeSides(a, b);
      const n = f.list.length;
      const first = f.list[0]!;
      const color = f.crossBase ? "var(--accent)" : "var(--ink-2)";
      const showLabel = hoverEdge === f.key || n > 1 || f.inherited;
      return [
        {
          id: f.key,
          source: f.source,
          target: f.target,
          sourceHandle: "s-" + sa,
          targetHandle: "t-" + sb,
          zIndex: 5,
          label: showLabel ? (n > 1 ? `${n} relaciones` : typeLabel(first.type) + (f.inherited ? " (heredada)" : "")) : undefined,
          style: { strokeWidth: 1.3 + (n - 1) * 1.4, stroke: color, strokeDasharray: f.inherited ? "5 4" : undefined, opacity: tag ? 0.35 : 0.9 },
          markerEnd: { type: MarkerType.ArrowClosed, width: 14, height: 14, color },
        },
      ];
    });
  }, [flat, atoms, foldedSet, hidden, hoverEdge, tag, layout]);

  // ------------------------------------------------------------ crear relaciones
  const say = useCallback((n: Notice | null) => setNotice(n), []);
  useEffect(() => {
    if (!notice) return;
    const t = setTimeout(() => setNotice(null), notice.tone === "ok" ? 4000 : 9000);
    return () => clearTimeout(t);
  }, [notice]);

  const connect = useCallback(
    async (sourceId: string, targetId: string) => {
      if (busy.current) return;
      const plan = planConnection({ sourceId, targetId, typeName: newType, atoms, types: store.relationTypes, edges: store.edges, groupLabel });
      if (!plan.ok) return say({ tone: "error", text: plan.message });
      busy.current = true;
      say(null);
      try {
        // Un grupo es un documento: se crea la primera vez que recibe una relación (409 = ya existe).
        for (const end of [plan.source, plan.target]) {
          if (!end.tag || store.documents.some((d) => d.model_name === GROUP_MODEL && `${GROUP_MODEL}:${d.id}` === end.gid)) continue;
          try {
            const g = await store.createDocument(GROUP_MODEL, groupSlug(end.tag), { title: groupLabel(end.tag), tag: end.tag, description: "" });
            if (g && g.ok === false) throw new Error(`El servidor rechazó el grupo ${end.tag}.`);
          } catch (err) {
            if (!isAlreadyExists(err)) throw err;
          }
        }
        const name = nextRelationName(store.documents);
        const res = await store.createDocument("RelationDoc", name, relationPayloadBetween(plan.source, plan.target, plan.type));
        if (res && res.ok === false) throw new Error("El servidor rechazó la relación.");
        say({ tone: "ok", text: `Relación ${name} creada: ${typeLabel(plan.type.name)}.` });
      } catch (err) {
        say({ tone: "error", text: `No se creó la relación: ${(err as Error).message}` });
      } finally {
        busy.current = false;
      }
    },
    [newType, atoms, store, groupLabel, say],
  );

  const onConnect = useCallback(
    (c: Connection) => {
      if (c.source && c.target) void connect(c.source, c.target);
    },
    [connect],
  );

  /** Soltar sobre el cuerpo de un nodo (no sobre un asa): el nodo bajo el puntero es el destino. */
  const onConnectEnd = useCallback(
    (event: MouseEvent | TouchEvent, state: FinalConnectionState) => {
      if (state.isValid) return;
      const from = state.fromNode?.id ?? dragFrom.current;
      const pt = "changedTouches" in event ? event.changedTouches[0] : (event as MouseEvent);
      if (!from || !pt) return;
      const el = document.elementFromPoint(pt.clientX, pt.clientY)?.closest?.(".react-flow__node");
      const to = el?.getAttribute("data-id");
      if (to && to !== from) void connect(from, to);
    },
    [connect],
  );

  // ------------------------------------------------------------ inspector
  const v = focusId ? byId.get(focusId) : undefined;
  const k = v ? relationsOfAtom(v, relations) : [];
  const P = selGroup;
  const D = (end: string) => {
    if (!isGroupNodeId(end)) return byId.get(end)?.text;
    const t = tagOfNodeId(end);
    return `${t.includes(".") ? "grupo" : "base"} ${groupLabel(t)}`;
  };
  const inspected = P ? atoms.filter((a) => (P.includes(".") ? inGroup(a, P) : groupOf(a) === P)) : [];
  const close = () => {
    setSelGroup(null);
    setFocusId(null);
  };

  const rows = layout.bases.map((box) => ({
    id: box.tag,
    label: box.tag === NO_GROUP ? "Sin grupo" : groupLabel(box.tag),
    count: atoms.filter((a) => groupOf(a) === box.tag).length,
    subs: box.cells.flatMap((c) => (c.tag === null ? [] : [{ tag: c.tag, title: groupLabel(c.tag) }])),
  }));

  const Toggle = ({ id }: { id: string }) => (
    <button onClick={() => toggle(id)} aria-expanded={!folded[id]} className="w-5 text-ink2 hover:text-ink" title={folded[id] ? "Desplegar" : "Plegar"}>
      {folded[id] ? "▸" : "▾"}
    </button>
  );
  const Name = ({ id, strong, children }: { id: string; strong?: boolean; children: string }) => (
    <button
      onClick={() => setTag(tag === id ? null : id)}
      className={`rounded px-1 ${strong ? "font-semibold" : "text-ink2 hover:text-ink"}`}
      style={tag === id ? { background: "var(--hl)", color: "var(--ink)" } : {}}
    >
      {children}
    </button>
  );

  return (
    <div className="flex h-full flex-col lg:flex-row">
      <aside className="shrink-0 overflow-auto border-b border-line bg-panel p-3 text-[13px] lg:w-60 lg:border-b-0 lg:border-r" aria-label="Bases y tags">
        <h2 className="mb-2 text-[12px] font-semibold text-ink2">Bases de conocimiento</h2>
        <ul className="flex flex-wrap gap-x-6 gap-y-2 lg:block">
          {rows.map((S) => (
            <li key={S.id} className="lg:mb-3">
              <div className="flex items-center gap-1">
                <Toggle id={S.id} />
                <Name id={S.id} strong>
                  {S.label}
                </Name>
                <span className="ml-auto pl-2 text-[11.5px] tabular-nums text-ink2">{S.count}</span>
              </div>
              {!folded[S.id] && S.subs.length > 0 && (
                <ul className="ml-5 mt-0.5 flex flex-wrap gap-x-2 lg:block">
                  {S.subs.map((O) => (
                    <li key={O.tag} className="flex items-center gap-0.5">
                      <Toggle id={O.tag} />
                      <Name id={O.tag}>{O.title}</Name>
                    </li>
                  ))}
                </ul>
              )}
            </li>
          ))}
        </ul>
        <p className="mt-4 hidden text-[12px] leading-relaxed text-ink2 lg:block">
          Las aristas azules cruzan de una base a otra. Plegar una base o un tag lo reduce a un nodo y fusiona sus aristas.
        </p>
      </aside>
      <section className="relative flex min-h-[460px] flex-1 flex-col" aria-label="Grafo">
        <div className="flex flex-wrap items-center gap-2 border-b border-line bg-panel px-3 py-2 text-[12.5px]">
          <span className="text-ink2">Relaciones:</span>
          {types.map((S) => (
            <button
              key={S}
              aria-pressed={!hidden.includes(S)}
              onClick={() => setHidden(hidden.includes(S) ? hidden.filter((C) => C !== S) : [...hidden, S])}
              className={`rounded-full border px-2 py-0.5 ${hidden.includes(S) ? "border-line text-faint line-through" : "border-ink2/40 text-ink"}`}
            >
              {typeLabel(S)}
            </button>
          ))}
          <label className="ml-auto flex items-center gap-1.5 text-ink2">
            Nueva relación
            <select value={newType} onChange={(e) => setChosen(e.target.value)} className="rounded border border-line bg-panel px-1 py-0.5 text-ink">
              {types.map((S) => (
                <option key={S} value={S}>
                  {typeLabel(S)}
                </option>
              ))}
            </select>
          </label>
        </div>
        <div className="min-h-0 flex-1">
          <ReactFlow
            nodes={nodes}
            edges={edges}
            nodeTypes={nodeTypes}
            fitView
            fitViewOptions={{ padding: 0.08 }}
            minZoom={0.25}
            onConnect={onConnect}
            onConnectStart={(_, p) => {
              dragFrom.current = p.nodeId;
            }}
            onConnectEnd={onConnectEnd}
            onNodeClick={(_, n) => {
              if (n.type === "region") return;
              if (n.type === "folded") {
                setSelGroup(tagOfNodeId(n.id));
                setFocusId(null);
              } else {
                setSelGroup(null);
                setFocusId(n.id);
              }
            }}
            onPaneClick={close}
            onEdgeMouseEnter={(_, e) => setHoverEdge(e.id)}
            onEdgeMouseLeave={() => setHoverEdge(null)}
            nodesConnectable
            zoomOnDoubleClick={false}
            proOptions={{ hideAttribution: true }}
          >
            <Background gap={24} size={1} color="var(--line)" />
            <Controls showInteractive={false} />
          </ReactFlow>
        </div>
        {notice && (
          <div className={`mq-graf-aviso${notice.tone === "ok" ? " is-ok" : ""}`} role={notice.tone === "error" ? "alert" : "status"}>
            <span>{notice.text}</span>
            <button onClick={() => setNotice(null)} aria-label="Cerrar aviso">
              ✕
            </button>
          </div>
        )}
        <p className="border-t border-line bg-panel px-3 py-1.5 text-[12px] text-ink2">
          Arrastra desde el borde de un nodo a otro para relacionarlos. Si sueltas sobre un grupo o base, la relación la heredan todos sus átomos (línea punteada).
        </p>
      </section>
      {(v || P) && (
        <aside className="shrink-0 overflow-auto border-t border-line bg-panel p-4 text-[13.5px] lg:w-72 lg:border-l lg:border-t-0" aria-label="Inspector">
          <div className="flex items-start justify-between">
            <h2 className="text-[12px] font-semibold text-ink2">Inspector</h2>
            <button onClick={close} className="text-ink2 hover:text-ink" aria-label="Cerrar inspector">
              ✕
            </button>
          </div>
          {v ? (
            <>
              <div className={`mt-2 text-[12px] font-semibold tx-t-${v.type}`}>{kindLabel(v.type)}</div>
              <p className="mt-0.5 text-[15px] leading-snug">{v.text}</p>
              <p className="mt-2 text-[12.5px] text-ink2">
                {v.tags.length ? `Base ${groupLabel(groupOf(v))}${cellTagOf(v) ? `, tag ${groupLabel(cellTagOf(v)!)}` : ""}. ` : "Sin grupo. "}
                Fuente: {fuentes.find((f) => f.gid === v.atom.source)?.title ?? v.sourceId}.
              </p>
              <h3 className="mt-4 text-[12px] font-semibold text-ink2">Relaciones</h3>
              <ul className="mt-1 space-y-1.5">
                {k.map((S) => {
                  const C = S.source === v.id || (isGroupNodeId(S.source) && inGroup(v, tagOfNodeId(S.source)));
                  return (
                    <li key={S.id} className="leading-snug">
                      <span className="text-ink2">
                        {C ? "→" : "←"} {typeLabel(S.type)}
                        {S.inherited ? " (heredada del grupo)" : ""}
                      </span>
                      <br />
                      <span>{D(C ? S.target : S.source)}</span>
                    </li>
                  );
                })}
                {!k.length && <li className="text-ink2">Sin relaciones todavía.</li>}
              </ul>
              <h3 className="mt-4 text-[12px] font-semibold text-ink2">Ancla en el texto</h3>
              <p className="mt-1 rounded bg-panel2 px-2 py-1.5 font-doc text-[13px] italic text-ink2">“{v.anchor[1]}”</p>
              <button onClick={() => go("extraccion", v.id)} className="mt-3 rounded-md border border-line px-3 py-1.5 font-semibold text-accent hover:bg-panel2">
                Ver en el texto
              </button>
              <h3 className="mt-4 text-[12px] font-semibold text-ink2">Dirección</h3>
              <code className="mt-1 block break-all text-[11.5px] text-ink2">{v.atom.gid}</code>
            </>
          ) : (
            <>
              <p className="mt-2 text-[15px] font-semibold">{P ? D(groupNodeId(P)) : null}</p>
              <ul className="mt-2 space-y-1">
                {inspected.map((S) => (
                  <li key={S.id} className="flex gap-2">
                    <span className={`tdot mt-1.5 bg-t-${S.type}`} />
                    <button
                      className="text-left hover:underline"
                      onClick={() => {
                        setFolded((m) => ({ ...m, [groupOf(S)]: false, ...(cellTagOf(S) ? { [cellTagOf(S)!]: false } : {}) }));
                        setSelGroup(null);
                        setFocusId(S.id);
                      }}
                    >
                      {S.text}
                    </button>
                  </li>
                ))}
              </ul>
            </>
          )}
        </aside>
      )}
    </div>
  );
}
