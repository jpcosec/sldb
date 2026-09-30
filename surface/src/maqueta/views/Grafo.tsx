/**
 * Vista Grafo de la maqueta (`SLDB_ extracción, grafo y compositor.html`, función `Xp`), portada a
 * TSX con el DOM, las clases y el comportamiento de la maqueta; los datos y las escrituras van al
 * `sldb serve` real (ver `../grafo-logic.ts` para lo que no depende de React).
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
import { NO_GROUP } from "../../core/atom-graph";
import { GROUP_MODEL, groupPayload, groupSlug, isAlreadyExists } from "../../core/atom-groups";
import { atomRelationTypes, groupTree, inGroup, type GroupNode } from "../../core/atoms";
import { nextRelationName, relationPayloadBetween } from "../../core/atom-graph";
import { toMockAtoms, toMockRelations, type MockAtom } from "../adapter";
import {
  KIND_LABEL,
  capitalize,
  computeLayout,
  edgeSides,
  expandRelations,
  foldedPosition,
  fuseEdges,
  groupNodeId,
  groupOf,
  isGroupNodeId,
  nodeCenter,
  planConnection,
  regionClass,
  relationsOfAtom,
  tagOfNodeId,
} from "../grafo-logic";
import type { ViewProps } from "../ViewProps";
import "../grafo.css";

const handles = (
  <>
    {(
      [
        ["t", Position.Top],
        ["r", Position.Right],
        ["b", Position.Bottom],
        ["l", Position.Left],
      ] as const
    ).map(([k, pos]) => (
      <Handle key={"s" + k} id={"s-" + k} type="source" position={pos} />
    ))}
    {(
      [
        ["t", Position.Top],
        ["r", Position.Right],
        ["b", Position.Bottom],
        ["l", Position.Left],
      ] as const
    ).map(([k, pos]) => (
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
  label: string;
  cls: string | null;
  onFold(): void;
  [k: string]: unknown;
}
interface FoldedData {
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
      <div className={`text-[10.5px] font-semibold tx-t-${t.type}`}>{KIND_LABEL[t.type]}</div>
      <div className="font-ui text-[12.5px] leading-snug text-ink line-clamp-2">{t.text}</div>
    </div>
  );
}

function RegionNode({ data }: NodeProps<FlowNode<RegionData>>) {
  return (
    <div
      className={`h-full w-full rounded-xl border border-line${data.cls ? "" : " mq-graf-region-neutro"}`}
      style={data.cls ? { background: `var(--region-${data.cls})` } : undefined}
    >
      {handles}
      <div className="flex items-center justify-between px-3 pt-2 font-ui">
        <span className="text-[13px] font-semibold text-ink">{data.label}</span>
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
  const counts = data.counts;
  const total = Object.values(counts).reduce((a, b) => a + b, 0);
  return (
    <div
      onDoubleClick={data.onUnfold}
      className={`w-[200px] rounded-xl border-2 border-ink/70 bg-panel px-3 py-2.5 font-ui shadow-md ${data.selected ? "ring-2 ring-accent" : ""}${data.cls ? "" : " mq-graf-folded-neutro"}`}
      style={data.cls ? { backgroundImage: `linear-gradient(var(--region-${data.cls}),var(--region-${data.cls}))` } : undefined}
    >
      {handles}
      <div className="flex items-baseline justify-between">
        <span className="text-[14px] font-semibold text-ink">{data.label}</span>
        <span className="text-[12px] text-ink2 tabular-nums">{total} átomos</span>
      </div>
      <div className="mt-2 flex h-1.5 overflow-hidden rounded-full">
        {Object.entries(counts).map(([k, n]) => (
          <span key={k} className={`bg-t-${k}`} style={{ width: `${(n / total) * 100}%` }} />
        ))}
      </div>
      <div className="mt-1.5 text-[11px] text-ink2">{data.internal} relaciones internas. Doble clic para desplegar.</div>
    </div>
  );
}

const nodeTypes = { atom: AtomNode, region: RegionNode, folded: FoldedNode };

interface Notice {
  tone: "error" | "ok";
  text: string;
}

export default function Grafo(props: ViewProps) {
  const { store, acta, focusId, setFocusId, go } = props;

  const atoms = useMemo(() => toMockAtoms(store.atoms.filter((a) => a.status !== "descartado"), acta), [store.atoms, acta]);
  const relations = useMemo(() => toMockRelations(store.edges, store.atoms), [store.edges, store.atoms]);
  const types = useMemo(() => relationTypeNamesOf(store.relationTypes), [store.relationTypes]);

  const [folded, setFolded] = useState<Record<string, boolean>>({});
  const [hidden, setHidden] = useState<string[]>([]);
  const [tag, setTag] = useState<string | null>(null);
  const [selGroup, setSelGroup] = useState<string | null>(null);
  const [hoverEdge, setHoverEdge] = useState<string | null>(null);
  const [chosen, setChosen] = useState("afecta");
  const [notice, setNotice] = useState<Notice | null>(null);
  const busy = useRef(false);
  const dragFrom = useRef<string | null>(null);

  const newType = types.includes(chosen) ? chosen : (types[0] ?? chosen);
  const foldedSet = useMemo(() => new Set(Object.keys(folded).filter((k) => folded[k])), [folded]);

  const layout = useMemo(() => computeLayout(atoms), [atoms]);
  const tree = useMemo(() => groupTree(atoms.map((a) => a.atom)), [atoms]);
  const untagged = atoms.filter((a) => groupOf(a) === NO_GROUP).length;

  const groupLabel = useCallback(
    (t: string): string => {
      const doc = store.documents.find(
        (d) => d.model_name === GROUP_MODEL && (d.payload.tag === t || d.id === groupSlug(t)),
      );
      const title = typeof doc?.payload.title === "string" ? doc.payload.title.trim() : "";
      if (title && title !== t) return title;
      return capitalize(t.split(".").filter(Boolean).pop() ?? t);
    },
    [store.documents],
  );
  const labelOfRegion = (t: string) => (t === NO_GROUP ? "Sin grupo" : groupLabel(t));

  const nodes = useMemo(() => {
    const out: FlowNode[] = [];
    for (const region of layout.regions) {
      const g = region.tag;
      const cls = regionClass(g);
      const inRegion = atoms.filter((a) => groupOf(a) === g);
      const label = labelOfRegion(g);
      if (folded[g]) {
        const counts: Record<string, number> = {};
        inRegion.forEach((a) => {
          counts[a.type] = (counts[a.type] || 0) + 1;
        });
        const ids = new Set(inRegion.map((a) => a.id));
        const internal = expandRelations(relations, atoms).filter((f) => ids.has(f.source) && ids.has(f.target) && !f.inherited).length;
        out.push({
          id: groupNodeId(g),
          type: "folded",
          position: foldedPosition(region),
          data: { label, cls, counts, internal, selected: selGroup === g, onUnfold: () => setFolded({ ...folded, [g]: false }) } satisfies FoldedData,
        });
        continue;
      }
      out.push({
        id: groupNodeId(g),
        type: "region",
        position: { x: region.x, y: region.y },
        style: { width: region.w, height: region.h },
        selectable: false,
        data: { label, cls, onFold: () => setFolded({ ...folded, [g]: true }) } satisfies RegionData,
      });
      for (const a of inRegion) {
        const p = layout.atoms[a.id]!;
        const dimmed = tag !== null && !(tag === NO_GROUP ? a.tags.length === 0 : inGroup(a, tag));
        out.push({
          id: a.id,
          type: "atom",
          parentId: groupNodeId(g),
          extent: "parent",
          position: { x: p.x, y: p.y },
          data: { atom: a, dimmed, selected: focusId === a.id } satisfies AtomData,
        });
      }
    }
    return out;
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [atoms, layout, folded, tag, focusId, selGroup, relations, groupLabel]);

  const flat = useMemo(() => expandRelations(relations, atoms), [relations, atoms]);
  const edges = useMemo(() => {
    return fuseEdges(flat, atoms, foldedSet, hidden).flatMap((f): FlowEdge[] => {
      const a = nodeCenter(f.source, layout, foldedSet);
      const b = nodeCenter(f.target, layout, foldedSet);
      if (!a || !b) return [];
      const [sa, sb] = edgeSides(a, b);
      const n = f.list.length;
      const first = f.list[0]!;
      const showLabel = hoverEdge === f.key || n > 1 || f.inherited;
      return [
        {
          id: f.key,
          source: f.source,
          target: f.target,
          sourceHandle: "s-" + sa,
          targetHandle: "t-" + sb,
          type: "default",
          label: showLabel ? (n > 1 ? `${n} relaciones` : first.type + (f.inherited ? " (heredada)" : "")) : undefined,
          style: { strokeWidth: 1.2 + (n - 1) * 1.6, stroke: "var(--ink-2)", strokeDasharray: f.inherited ? "5 4" : undefined, opacity: tag ? 0.35 : 0.9 },
          markerEnd: { type: MarkerType.ArrowClosed, width: 14, height: 14, color: "var(--ink-2)" },
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
            const g = await store.createDocument(GROUP_MODEL, groupSlug(end.tag), groupPayload(end.tag));
            if (g && g.ok === false) throw new Error(`El servidor rechazó el grupo ${end.tag}.`);
          } catch (err) {
            if (!isAlreadyExists(err)) throw err;
          }
        }
        const name = nextRelationName(store.documents);
        const res = await store.createDocument("RelationDoc", name, relationPayloadBetween(plan.source, plan.target, plan.type));
        if (res && res.ok === false) throw new Error("El servidor rechazó la relación.");
        say({ tone: "ok", text: `Relación ${name} creada: ${plan.type.name}.` });
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
  const v = atoms.find((a) => a.id === focusId);
  const k = v ? relationsOfAtom(v, relations) : [];
  const b = selGroup;
  const E = (end: string) => (isGroupNodeId(end) ? `grupo ${groupLabel(tagOfNodeId(end))}` : atoms.find((a) => a.id === end)?.text);

  const toggleFold = (g: string) => setFolded({ ...folded, [g]: !folded[g] });
  const roots: GroupNode[] = tree;

  const renderChildren = (list: GroupNode[]) =>
    list.map((c) => (
      <li key={c.id}>
        <button
          onClick={() => setTag(tag === c.id ? null : c.id)}
          className="rounded px-1 text-ink2 hover:text-ink"
          style={tag === c.id ? { background: "var(--hl)", color: "var(--ink)" } : {}}
        >
          {groupLabel(c.id)}
        </button>
        {c.children.length > 0 && <ul className="ml-6 mt-0.5">{renderChildren(c.children)}</ul>}
      </li>
    ));

  const rows: { id: string; label: string; count: number; children: GroupNode[]; region: boolean }[] = [
    ...[...roots]
      .sort((a, b) => regionOrder(layout, a.id) - regionOrder(layout, b.id))
      .map((r) => ({
      id: r.id,
      label: groupLabel(r.id),
      count: atoms.filter((a) => groupOf(a) === r.id).length,
      children: r.children,
      region: layout.regions.some((x) => x.tag === r.id),
    })),
    ...(untagged ? [{ id: NO_GROUP, label: "Sin grupo", count: untagged, children: [], region: true }] : []),
  ];

  return (
    <div className="flex h-full flex-col lg:flex-row">
      <aside className="shrink-0 border-b border-line bg-panel p-3 text-[13px] lg:w-56 lg:border-b-0 lg:border-r" aria-label="Árbol de tags">
        <h2 className="mb-2 text-[12px] font-semibold text-ink2">Tags</h2>
        <ul className="flex flex-wrap gap-x-4 gap-y-1 lg:block">
          {rows.map((S) => (
            <li key={S.id} className="lg:mb-1.5">
              <div className="flex items-center gap-1">
                {S.region ? (
                  <button
                    onClick={() => toggleFold(S.id)}
                    aria-expanded={!folded[S.id]}
                    className="w-5 text-ink2 hover:text-ink"
                    title={folded[S.id] ? "Desplegar" : "Plegar"}
                  >
                    {folded[S.id] ? "▸" : "▾"}
                  </button>
                ) : (
                  <span className="w-5" />
                )}
                <button
                  onClick={() => setTag(tag === S.id ? null : S.id)}
                  className={`rounded px-1 ${tag === S.id ? "bg-hl font-semibold" : "hover:bg-panel2"}`}
                  style={tag === S.id ? { background: "var(--hl)" } : {}}
                >
                  {S.label}
                </button>
                <span className="ml-auto text-[11.5px] tabular-nums text-ink2">{S.count}</span>
              </div>
              {!folded[S.id] && S.children.length > 0 && <ul className="ml-6 mt-0.5 hidden lg:block">{renderChildren(S.children)}</ul>}
            </li>
          ))}
        </ul>
        <p className="mt-4 hidden text-[12px] leading-relaxed text-ink2 lg:block">
          Clic en un tag resalta sus átomos. El triángulo pliega el grupo en un solo nodo y fusiona sus aristas.
        </p>
      </aside>
      <section className="relative flex min-h-[420px] flex-1 flex-col" aria-label="Grafo">
        <div className="flex flex-wrap items-center gap-2 border-b border-line bg-panel px-3 py-2 text-[12.5px]">
          <span className="text-ink2">Relaciones:</span>
          {types.map((S) => (
            <button
              key={S}
              aria-pressed={!hidden.includes(S)}
              onClick={() => setHidden(hidden.includes(S) ? hidden.filter((C) => C !== S) : [...hidden, S])}
              className={`rounded-full border px-2 py-0.5 ${hidden.includes(S) ? "border-line text-faint line-through" : "border-ink2/40 text-ink"}`}
            >
              {S}
            </button>
          ))}
          <label className="ml-auto flex items-center gap-1.5 text-ink2">
            Nueva relación
            <select value={newType} onChange={(e) => setChosen(e.target.value)} className="rounded border border-line bg-panel px-1 py-0.5 text-ink">
              {types.map((S) => (
                <option key={S}>{S}</option>
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
            fitViewOptions={{ padding: 0.12 }}
            minZoom={0.3}
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
            onPaneClick={() => {
              setSelGroup(null);
              setFocusId(null);
            }}
            onEdgeMouseEnter={(_, e) => setHoverEdge(e.id)}
            onEdgeMouseLeave={() => setHoverEdge(null)}
            nodesConnectable
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
          Arrastra desde el borde de un nodo a otro para relacionarlos. Si sueltas sobre un grupo, la relación la heredan todos sus átomos (línea punteada).
        </p>
      </section>
      {(v || b) && (
        <aside className="shrink-0 overflow-auto border-t border-line bg-panel p-4 text-[13.5px] lg:w-72 lg:border-l lg:border-t-0" aria-label="Inspector">
          <div className="flex items-start justify-between">
            <h2 className="text-[12px] font-semibold text-ink2">Inspector</h2>
            <button
              onClick={() => {
                setSelGroup(null);
                setFocusId(null);
              }}
              className="text-ink2 hover:text-ink"
              aria-label="Cerrar inspector"
            >
              ✕
            </button>
          </div>
          {v ? (
            <>
              <div className={`mt-2 text-[12px] font-semibold tx-t-${v.type}`}>{KIND_LABEL[v.type]}</div>
              <p className="mt-0.5 text-[15px] leading-snug">{v.text}</p>
              <div className="mt-2 flex flex-wrap gap-1">
                {v.tags.map((S) => (
                  <span key={S} className="rounded border border-line bg-panel2 px-1.5 text-[11.5px] text-ink2">
                    {S}
                  </span>
                ))}
              </div>
              <h3 className="mt-4 text-[12px] font-semibold text-ink2">Relaciones</h3>
              <ul className="mt-1 space-y-1.5">
                {k.map((S) => {
                  const C = S.source === v.id || (isGroupNodeId(S.source) && inGroup(v, tagOfNodeId(S.source)));
                  return (
                    <li key={S.id} className="leading-snug">
                      <span className="text-ink2">
                        {C ? "→" : "←"} {S.type}
                        {S.inherited ? " (heredada)" : ""}
                      </span>
                      <br />
                      <span>{E(C ? S.target : S.source)}</span>
                    </li>
                  );
                })}
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
              <p className="mt-2 text-[15px] font-semibold">{b ? labelOfRegion(b) : null}</p>
              <ul className="mt-2 space-y-1">
                {atoms
                  .filter((S) => groupOf(S) === b)
                  .map((S) => (
                    <li key={S.id} className="flex gap-2">
                      <span className={`tdot mt-1.5 bg-t-${S.type}`} />
                      <button
                        className="text-left hover:underline"
                        onClick={() => {
                          setFolded({ ...folded, [b as string]: false });
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

/** Posición de la región del grupo en el layout (las regiones van de mayor a menor); sin región, al final. */
const regionOrder = (layout: ReturnType<typeof computeLayout>, tag: string): number => {
  const i = layout.regions.findIndex((r) => r.tag === tag);
  return i < 0 ? layout.regions.length : i;
};

const relationTypeNamesOf = (specs: ViewProps["store"]["relationTypes"]): string[] => atomRelationTypes(specs).map((t) => t.name);
