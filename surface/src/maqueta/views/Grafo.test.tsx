import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { act, cleanup, fireEvent, render, screen, within } from "@testing-library/react";
import fixture from "../../core/__fixtures__/atoms.json";
import { actasFromDocuments, atomsFromDocuments, relationTypesFromDocuments } from "../../core/atoms";
import type { Edge, GraphDocument, RelationTypeSpec } from "../../core/contract";
import type { AtomStore } from "../../views/atoms/useAtomStore";
import type { ViewProps } from "../ViewProps";

// jsdom no da geometría: React Flow se sustituye por un espía que guarda sus props (nodos, aristas
// y handlers) para inspeccionarlos y dispararlos; lo demás del módulo (Handle, Background…) es real.
const rf: { props: any } = { props: null };
vi.mock("@xyflow/react", async (orig) => ({
  ...(await orig<typeof import("@xyflow/react")>()),
  ReactFlow: (props: any) => {
    rf.props = props;
    return <div data-testid="rf" />;
  },
  Background: () => null,
  Controls: () => null,
}));

import Grafo from "./Grafo";

const docs = fixture.documents as unknown as GraphDocument[];
const spec = (name: string, src: string[], tgt: string[]): RelationTypeSpec => ({ id: name, name, source_types: src, target_types: tgt, cardinality: "", description: "" });
const relationTypes = [...relationTypesFromDocuments(docs), spec("afecta", ["AtomDoc", "GrupoDoc"], ["AtomDoc", "GrupoDoc"]), spec("plazo_de", ["AtomDoc"], ["AtomDoc", "GrupoDoc"])];
const edges: Edge[] = [
  { id: "e1", source: "AtomDoc:a5", target: "AtomDoc:a2", type: "motiva", origin: "relation_doc", relationDoc: "r1" },
  { id: "e3", source: "GrupoDoc:infra-ingesta", target: "AtomDoc:a4", type: "afecta", origin: "relation_doc", relationDoc: "r2" },
];
const documents: GraphDocument[] = [
  ...docs,
  { id: "infra-ingesta", model_name: "GrupoDoc", path: "docs/g.md", version: "v", semantic_tags: [], payload: { title: "Ingesta de datos", tag: "infra.ingesta" } } as unknown as GraphDocument,
];

function setup(over: Partial<ViewProps> = {}, storeOver: Partial<AtomStore> = {}) {
  const createDocument = vi.fn(async (..._a: unknown[]) => ({ ok: true, id: "x", version: "v" }));
  const store = {
    status: "ok",
    error: null,
    atoms: atomsFromDocuments(documents),
    actas: actasFromDocuments(documents),
    informes: [],
    relationTypes,
    edges,
    documents,
    reload: vi.fn(),
    saveField: vi.fn(),
    createAtom: vi.fn(),
    createDocument,
    ...storeOver,
  } as unknown as AtomStore;
  const props: ViewProps = { store, acta: store.actas[0]!, focusId: null, setFocusId: vi.fn(), go: vi.fn(), ...over };
  const view = render(<Grafo {...props} />);
  return { props, createDocument, ...view };
}

const nodeIds = () => (rf.props.nodes as { id: string }[]).map((n) => n.id);

beforeEach(() => {
  rf.props = null;
});
afterEach(cleanup);

describe("Grafo (maqueta)", () => {
  it("nodos: regiones por grupo y átomos no descartados; aristas directas y heredadas", () => {
    setup();
    expect(nodeIds().sort()).toEqual(["a1", "a2", "a3", "a4", "a5", "g:infra", "g:reuniones"]);
    const region = rf.props.nodes.find((n: any) => n.id === "g:infra");
    expect(region.type).toBe("region");
    expect(region.selectable).toBe(false);
    const atom = rf.props.nodes.find((n: any) => n.id === "a2");
    expect(atom).toMatchObject({ type: "atom", parentId: "g:infra", extent: "parent" });
    const ed = rf.props.edges as any[];
    expect(ed.find((e) => e.id === "a5->a2").style.strokeDasharray).toBeUndefined();
    const inh = ed.filter((e) => e.id.endsWith(":inh"));
    expect(inh.map((e) => `${e.source}>${e.target}`).sort()).toEqual(["a2>a4", "a3>a4"]);
    expect(inh[0].label).toBe("afecta (heredada)");
    expect(inh[0].style.strokeDasharray).toBe("5 4");
  });

  it("barra Tags: etiqueta del GrupoDoc, conteos y texto de ayuda; los tipos salen del store", () => {
    setup();
    const aside = screen.getByLabelText("Árbol de tags");
    expect(within(aside).getByText("Infra")).toBeInTheDocument();
    expect(within(aside).getByText("Ingesta de datos")).toBeInTheDocument(); // título del GrupoDoc
    expect(within(aside).getByText("Reuniones")).toBeInTheDocument();
    expect(within(aside).getByText(/Clic en un tag resalta sus átomos/)).toBeInTheDocument();
    const chips = screen.getAllByRole("button", { pressed: true }).map((b) => b.textContent);
    expect(chips).toEqual(["motiva", "afecta", "plazo_de"]);
    expect(screen.getByLabelText("Nueva relación")).toHaveValue("afecta"); // el tipo por defecto de la maqueta
    expect(screen.getByText(/Arrastra desde el borde de un nodo a otro/)).toBeInTheDocument();
  });

  it("un chip oculta un tipo y lo muestra de nuevo", () => {
    setup();
    fireEvent.click(screen.getByRole("button", { name: "motiva" }));
    expect((rf.props.edges as any[]).some((e) => e.id === "a5->a2")).toBe(false);
    expect(screen.getByRole("button", { name: "motiva" })).toHaveAttribute("aria-pressed", "false");
    fireEvent.click(screen.getByRole("button", { name: "motiva" }));
    expect((rf.props.edges as any[]).some((e) => e.id === "a5->a2")).toBe(true);
  });

  it("clic en un tag atenúa los átomos que no son del grupo; otro clic lo quita", () => {
    setup();
    const dim = () => (rf.props.nodes as any[]).filter((n) => n.type === "atom" && n.data.dimmed).map((n) => n.id);
    fireEvent.click(within(screen.getByLabelText("Árbol de tags")).getByRole("button", { name: "Ingesta de datos" }));
    expect(dim().sort()).toEqual(["a1", "a4", "a5"]);
    fireEvent.click(within(screen.getByLabelText("Árbol de tags")).getByRole("button", { name: "Ingesta de datos" }));
    expect(dim()).toEqual([]);
  });

  it("el triángulo pliega el grupo en un nodo y fusiona sus aristas; desplegar lo restaura", () => {
    setup();
    fireEvent.click(screen.getAllByTitle("Plegar")[0]!);
    expect(nodeIds().sort()).toEqual(["a1", "g:infra", "g:reuniones"]);
    const folded = rf.props.nodes.find((n: any) => n.id === "g:infra");
    expect(folded.type).toBe("folded");
    expect(folded.data.counts).toEqual({ decision: 1, hecho: 1, riesgo: 1, pendiente: 1 });
    expect(folded.data.internal).toBe(1);
    // las heredadas a2>a4 y a3>a4 quedan dentro del grupo plegado: ninguna arista sale de él
    expect(rf.props.edges).toEqual([]);
    act(() => folded.data.onUnfold());
    expect(nodeIds()).toContain("a2");
  });

  it("el botón Plegar de la región pliega ese grupo", () => {
    setup();
    const region = rf.props.nodes.find((n: any) => n.id === "g:reuniones");
    act(() => region.data.onFold());
    expect(rf.props.nodes.find((n: any) => n.id === "g:reuniones").type).toBe("folded");
  });

  it("focusId abre el inspector de ese átomo: tipo, texto, tags, relaciones →/←, ancla y dirección real", () => {
    const { props } = setup({ focusId: "a2" });
    const insp = screen.getByLabelText("Inspector");
    expect(within(insp).getByText("Decisión")).toBeInTheDocument();
    expect(within(insp).getByText("Reemplazar el lote por una cola")).toBeInTheDocument();
    expect(within(insp).getByText("infra.ingesta")).toBeInTheDocument();
    expect(within(insp).getByText("← motiva")).toBeInTheDocument(); // a5 motiva a2
    expect(within(insp).getByText("→ afecta (heredada)")).toBeInTheDocument(); // grupo ingesta afecta a4
    expect(within(insp).getByText("Definir esquema de eventos")).toBeInTheDocument();
    expect(within(insp).getByText("Proveedor no soporta el volumen")).toBeInTheDocument();
    expect(within(insp).getByText("“Decidimos reemplazar el lote nocturno por una cola de eventos”")).toBeInTheDocument();
    expect(within(insp).getByText("AtomDoc:a2")).toBeInTheDocument();
    fireEvent.click(within(insp).getByRole("button", { name: "Ver en el texto" }));
    expect(props.go).toHaveBeenCalledWith("extraccion", "a2");
    fireEvent.click(within(insp).getByRole("button", { name: "Cerrar inspector" }));
    expect(props.setFocusId).toHaveBeenCalledWith(null);
  });

  it("clic en un nodo enfoca el átomo; clic en el lienzo lo suelta; la región no se selecciona", () => {
    const { props } = setup();
    act(() => rf.props.onNodeClick({}, { id: "a3", type: "atom" }));
    expect(props.setFocusId).toHaveBeenLastCalledWith("a3");
    act(() => rf.props.onNodeClick({}, { id: "g:infra", type: "region" }));
    expect(props.setFocusId).toHaveBeenCalledTimes(1);
    act(() => rf.props.onPaneClick());
    expect(props.setFocusId).toHaveBeenLastCalledWith(null);
  });

  it("un grupo plegado seleccionado abre el inspector con sus átomos", () => {
    const { props } = setup();
    fireEvent.click(screen.getAllByTitle("Plegar")[0]!);
    act(() => rf.props.onNodeClick({}, { id: "g:infra", type: "folded" }));
    const insp = screen.getByLabelText("Inspector");
    expect(within(insp).getByText("Infra")).toBeInTheDocument();
    fireEvent.click(within(insp).getByRole("button", { name: "Definir esquema de eventos" }));
    expect(props.setFocusId).toHaveBeenLastCalledWith("a5");
    expect(nodeIds()).toContain("a5"); // se desplegó
  });

  describe("crear relación", () => {
    it("átomo → átomo válido: crea el RelationDoc con rel-<n>", async () => {
      const { createDocument } = setup();
      fireEvent.change(screen.getByLabelText("Nueva relación"), { target: { value: "motiva" } });
      await act(async () => rf.props.onConnect({ source: "a1", target: "a3" }));
      expect(createDocument).toHaveBeenCalledTimes(1);
      expect(createDocument).toHaveBeenCalledWith("RelationDoc", "rel-1", expect.objectContaining({ source_id: "AtomDoc:a1", target_id: "AtomDoc:a3", relation_type: "motiva" }));
      expect(screen.getByText(/Relación rel-1 creada/)).toBeInTheDocument();
    });

    it("usa el tipo elegido en 'Nueva relación'", async () => {
      const { createDocument } = setup();
      fireEvent.change(screen.getByLabelText("Nueva relación"), { target: { value: "plazo_de" } });
      await act(async () => rf.props.onConnect({ source: "a1", target: "a3" }));
      expect(createDocument).toHaveBeenCalledWith("RelationDoc", expect.any(String), expect.objectContaining({ relation_type: "plazo_de" }));
    });

    it("duplicada: aviso visible y no crea nada", async () => {
      const { createDocument } = setup();
      fireEvent.change(screen.getByLabelText("Nueva relación"), { target: { value: "motiva" } });
      await act(async () => rf.props.onConnect({ source: "a5", target: "a2" }));
      expect(createDocument).not.toHaveBeenCalled();
      expect(screen.getByRole("alert")).toHaveTextContent(/Ya existe «motiva»/);
    });

    it("tipo no válido entre extremos (grupo → átomo con plazo_de): aviso, nada creado", async () => {
      const { createDocument } = setup();
      fireEvent.change(screen.getByLabelText("Nueva relación"), { target: { value: "plazo_de" } });
      await act(async () => rf.props.onConnect({ source: "g:reuniones", target: "a3" }));
      expect(createDocument).not.toHaveBeenCalled();
      expect(screen.getByRole("alert")).toHaveTextContent(/«plazo_de» no es válido/);
    });

    it("sobre un grupo sin GrupoDoc: crea el GrupoDoc y luego el RelationDoc con GrupoDoc:<slug>", async () => {
      const { createDocument } = setup();
      await act(async () => rf.props.onConnect({ source: "a3", target: "g:reuniones" }));
      expect(createDocument.mock.calls.map((c: any[]) => [c[0], c[1]])).toEqual([
        ["GrupoDoc", "reuniones"],
        ["RelationDoc", "rel-1"],
      ]);
      expect((createDocument.mock.calls[1] as unknown[])[2]).toMatchObject({ source_id: "AtomDoc:a3", target_id: "GrupoDoc:reuniones" });
    });

    it("soltar sobre el cuerpo de una región (sin asa) crea la relación con el grupo; 409 del grupo se tolera", async () => {
      const createDocument = vi.fn(async (model: string) => {
        if (model === "GrupoDoc") throw Object.assign(new Error("existe"), { status: 409 });
        return { ok: true, id: "x", version: "v" };
      });
      setup({}, { createDocument } as any);
      const el = document.createElement("div");
      el.className = "react-flow__node";
      el.setAttribute("data-id", "g:reuniones");
      document.body.appendChild(el);
      const spy = vi.fn(() => el);
      (document as any).elementFromPoint = spy;
      await act(async () => rf.props.onConnectEnd({ clientX: 1, clientY: 1 }, { isValid: false, fromNode: { id: "a3" } }));
      delete (document as any).elementFromPoint;
      el.remove();
      expect(createDocument.mock.calls.map((c: any[]) => c[0])).toEqual(["GrupoDoc", "RelationDoc"]);
      expect(screen.getByText(/Relación rel-1 creada/)).toBeInTheDocument();
    });

    it("error del servidor (422): aviso sin perder el plegado", async () => {
      const createDocument = vi.fn(async () => {
        throw Object.assign(new Error("payload inválido"), { status: 422 });
      });
      setup({}, { createDocument } as any);
      fireEvent.click(screen.getAllByTitle("Plegar")[0]!);
      await act(async () => rf.props.onConnect({ source: "a1", target: "g:infra" }));
      expect(screen.getByRole("alert")).toHaveTextContent(/No se creó la relación: payload inválido/);
      expect(rf.props.nodes.find((n: any) => n.id === "g:infra").type).toBe("folded");
    });
  });
});
