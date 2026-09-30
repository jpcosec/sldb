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
  { id: "e4", source: "AtomDoc:a1", target: "AtomDoc:a3", type: "motiva", origin: "relation_doc", relationDoc: "r3" },
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
  const acta = store.actas[0]!;
  const props: ViewProps = { store, acta, fuentes: [{ ...acta, tipo: "acta", base: "", descripcion: "" }], informe: undefined, respuesta: undefined, caso: null, focusId: null, setFocusId: vi.fn(), go: vi.fn(), ...over };
  const view = render(<Grafo {...props} />);
  return { props, createDocument, ...view };
}

const nodeIds = () => (rf.props.nodes as { id: string }[]).map((n) => n.id);

beforeEach(() => {
  rf.props = null;
});
afterEach(cleanup);

describe("Grafo (maqueta)", () => {
  it("nodos: bases con sus subgrupos anidados y átomos (parentId/extent); aristas directas y heredadas", () => {
    setup();
    expect(nodeIds().sort()).toEqual(["a1", "a2", "a3", "a4", "a5", "g:infra", "g:infra.ingesta", "g:infra.proveedores", "g:reuniones"]);
    const base = rf.props.nodes.find((n: any) => n.id === "g:infra");
    expect(base).toMatchObject({ type: "region", selectable: false });
    expect(base.data).toMatchObject({ level: "kb", label: "Base: Infra", cls: "infra" });
    const sub = rf.props.nodes.find((n: any) => n.id === "g:infra.ingesta");
    expect(sub).toMatchObject({ type: "region", parentId: "g:infra", extent: "parent", style: { width: 250 } });
    expect(sub.data).toMatchObject({ level: "g", label: "Ingesta de datos" }); // título del GrupoDoc
    expect(rf.props.nodes.find((n: any) => n.id === "a2")).toMatchObject({ type: "atom", parentId: "g:infra.ingesta", extent: "parent" });
    expect(rf.props.nodes.find((n: any) => n.id === "a5")).toMatchObject({ parentId: "g:infra" }); // tag `infra`: directo a la base
    const ed = rf.props.edges as any[];
    const direct = ed.find((e) => e.id === "a5->a2");
    expect(direct.style).toMatchObject({ stroke: "var(--ink-2)" });
    expect(direct.style.strokeDasharray).toBeUndefined();
    const inh = ed.filter((e) => e.id.endsWith(":inh"));
    expect(inh.map((e) => `${e.source}>${e.target}`).sort()).toEqual(["a2>a4", "a3>a4"]);
    expect(inh[0].label).toBe("afecta (heredada)");
    expect(inh[0].style.strokeDasharray).toBe("5 4");
  });

  it("las aristas que cruzan de una base a otra salen azules", () => {
    setup();
    const cross = (rf.props.edges as any[]).find((e) => e.id === "a1->a3");
    expect(cross.style.stroke).toBe("var(--accent)");
    expect(cross.markerEnd.color).toBe("var(--accent)");
  });

  it("barra 'Bases de conocimiento': árbol base ▸ subgrupos con conteos, ayuda; los tipos salen del store", () => {
    setup();
    const aside = screen.getByLabelText("Bases y tags");
    expect(within(aside).getByText("Bases de conocimiento")).toBeInTheDocument();
    expect(within(aside).getByText("Infra")).toBeInTheDocument();
    expect(within(aside).getByText("Ingesta de datos")).toBeInTheDocument(); // título del GrupoDoc
    expect(within(aside).getByText("Proveedores")).toBeInTheDocument();
    expect(within(aside).getByText("Reuniones")).toBeInTheDocument();
    expect(within(aside).getByText("4")).toBeInTheDocument(); // a2..a5 en Infra
    expect(within(aside).getByText(/Las aristas azules cruzan de una base a otra\. Plegar una base o un tag lo reduce a un nodo y fusiona sus aristas\./)).toBeInTheDocument();
    const chips = screen.getAllByRole("button", { pressed: true }).map((b) => b.textContent);
    expect(chips).toEqual(["motiva", "afecta", "plazo de"]); // sin `_`
    expect(screen.getByLabelText("Nueva relación")).toHaveValue("motiva"); // 'activa' no existe en este store: el primero
    expect(screen.getByText(/Arrastra desde el borde de un nodo a otro para relacionarlos\. Si sueltas sobre un grupo o base, la relación la heredan todos sus átomos \(línea punteada\)\./)).toBeInTheDocument();
  });

  it("el tipo por defecto es 'activa' si el store lo tiene", () => {
    const withActiva = [...relationTypes, spec("activa", ["AtomDoc"], ["AtomDoc"])];
    setup({}, { relationTypes: withActiva } as any);
    expect(screen.getByLabelText("Nueva relación")).toHaveValue("activa");
  });

  it("un chip oculta un tipo y lo muestra de nuevo", () => {
    setup();
    fireEvent.click(screen.getByRole("button", { name: "motiva" }));
    expect((rf.props.edges as any[]).some((e) => e.id === "a5->a2")).toBe(false);
    expect(screen.getByRole("button", { name: "motiva" })).toHaveAttribute("aria-pressed", "false");
    fireEvent.click(screen.getByRole("button", { name: "motiva" }));
    expect((rf.props.edges as any[]).some((e) => e.id === "a5->a2")).toBe(true);
  });

  it("clic en una base o subgrupo atenúa los átomos ajenos; otro clic lo quita", () => {
    setup();
    const dim = () => (rf.props.nodes as any[]).filter((n) => n.type === "atom" && n.data.dimmed).map((n) => n.id);
    const aside = () => within(screen.getByLabelText("Bases y tags"));
    fireEvent.click(aside().getByRole("button", { name: "Ingesta de datos" }));
    expect(dim().sort()).toEqual(["a1", "a4", "a5"]);
    fireEvent.click(aside().getByRole("button", { name: "Ingesta de datos" }));
    expect(dim()).toEqual([]);
    fireEvent.click(aside().getByRole("button", { name: "Infra" }));
    expect(dim()).toEqual(["a1"]);
  });

  it("el triángulo de una base la pliega en un nodo y fusiona sus aristas; desplegar lo restaura", () => {
    setup();
    fireEvent.click(screen.getAllByTitle("Plegar")[1]!); // orden de lectura: reuniones, infra
    expect(nodeIds().sort()).toEqual(["a1", "g:infra", "g:reuniones"]);
    const folded = rf.props.nodes.find((n: any) => n.id === "g:infra");
    expect(folded.type).toBe("folded");
    expect(folded.data).toMatchObject({ level: "kb", label: "Base: Infra", counts: { decision: 1, hecho: 1, riesgo: 1, pendiente: 1 }, internal: 1 });
    // las heredadas a2>a4 y a3>a4 quedan dentro del nodo plegado; solo sale la que va a a1
    expect((rf.props.edges as any[]).map((e) => `${e.source}>${e.target}`)).toEqual(["a1>g:infra"]);
    act(() => folded.data.onUnfold());
    expect(nodeIds()).toContain("a2");
  });

  it("plegar un subgrupo lo reduce a un nodo dentro de su base", () => {
    setup();
    const region = rf.props.nodes.find((n: any) => n.id === "g:infra.ingesta");
    act(() => region.data.onFold());
    const folded = rf.props.nodes.find((n: any) => n.id === "g:infra.ingesta");
    expect(folded).toMatchObject({ type: "folded", parentId: "g:infra", extent: "parent" });
    expect(folded.data).toMatchObject({ level: "g", label: "Ingesta de datos", counts: { decision: 1, hecho: 1 } });
    expect(nodeIds()).not.toContain("a2");
    expect((rf.props.edges as any[]).map((e) => e.id)).toContain("g:infra.ingesta->a4:inh");
  });

  it("el botón Plegar de la base pliega esa base", () => {
    setup();
    const region = rf.props.nodes.find((n: any) => n.id === "g:reuniones");
    act(() => region.data.onFold());
    expect(rf.props.nodes.find((n: any) => n.id === "g:reuniones").type).toBe("folded");
  });

  it("focusId abre el inspector: tipo, texto, base/tag/fuente, relaciones →/←, ancla y dirección AtomDoc:<id>", () => {
    const { props } = setup({ focusId: "a2" });
    const insp = screen.getByLabelText("Inspector");
    expect(within(insp).getByText("Decisión")).toBeInTheDocument();
    expect(within(insp).getByText("Reemplazar el lote por una cola")).toBeInTheDocument();
    expect(within(insp).getByText(/Base Infra, tag Ingesta de datos\. Fuente:/)).toBeInTheDocument();
    expect(within(insp).getByText("← motiva")).toBeInTheDocument(); // a5 motiva a2
    expect(within(insp).getByText("→ afecta (heredada del grupo)")).toBeInTheDocument(); // grupo ingesta afecta a4
    expect(within(insp).getByText("Definir esquema de eventos")).toBeInTheDocument();
    expect(within(insp).getByText("Proveedor no soporta el volumen")).toBeInTheDocument();
    expect(within(insp).getByText("“Decidimos reemplazar el lote nocturno por una cola de eventos”")).toBeInTheDocument();
    expect(within(insp).getByText("AtomDoc:a2")).toBeInTheDocument();
    fireEvent.click(within(insp).getByRole("button", { name: "Ver en el texto" }));
    expect(props.go).toHaveBeenCalledWith("extraccion", "a2");
    fireEvent.click(within(insp).getByRole("button", { name: "Cerrar inspector" }));
    expect(props.setFocusId).toHaveBeenCalledWith(null);
  });

  it("un átomo sin relaciones lo dice", () => {
    setup({ focusId: "a5" });
    expect(within(screen.getByLabelText("Inspector")).getByText(/motiva/)).toBeInTheDocument();
    cleanup();
    setup({ focusId: "a4" }, { edges: [] } as any);
    expect(within(screen.getByLabelText("Inspector")).getByText("Sin relaciones todavía.")).toBeInTheDocument();
  });

  it("focusId despliega la base y el subgrupo plegados que contienen al átomo", () => {
    const { props, rerender } = setup();
    act(() => rf.props.nodes.find((n: any) => n.id === "g:infra.ingesta").data.onFold());
    act(() => rf.props.nodes.find((n: any) => n.id === "g:reuniones").data.onFold());
    expect(nodeIds()).not.toContain("a2");
    rerender(<Grafo {...props} focusId="a2" />);
    expect(nodeIds()).toContain("a2");
    expect(rf.props.nodes.find((n: any) => n.id === "g:reuniones").type).toBe("folded"); // el resto sigue plegado
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

  it("un subgrupo plegado seleccionado abre el inspector con sus átomos; clic en uno lo despliega", () => {
    const { props } = setup();
    act(() => rf.props.nodes.find((n: any) => n.id === "g:infra.ingesta").data.onFold());
    act(() => rf.props.onNodeClick({}, { id: "g:infra.ingesta", type: "folded" }));
    const insp = screen.getByLabelText("Inspector");
    expect(within(insp).getByText("grupo Ingesta de datos")).toBeInTheDocument();
    fireEvent.click(within(insp).getByRole("button", { name: "Tomás responsable de la ingesta" }));
    expect(props.setFocusId).toHaveBeenLastCalledWith("a3");
    expect(nodeIds()).toContain("a3"); // se desplegó
  });

  describe("crear relación", () => {
    it("átomo → átomo válido: crea el RelationDoc con rel-<n>", async () => {
      const { createDocument } = setup();
      fireEvent.change(screen.getByLabelText("Nueva relación"), { target: { value: "motiva" } });
      await act(async () => rf.props.onConnect({ source: "a1", target: "a4" }));
      expect(createDocument).toHaveBeenCalledTimes(1);
      expect(createDocument).toHaveBeenCalledWith("RelationDoc", "rel-1", expect.objectContaining({ source_id: "AtomDoc:a1", target_id: "AtomDoc:a4", relation_type: "motiva" }));
      expect(screen.getByText(/Relación rel-1 creada/)).toBeInTheDocument();
    });

    it("usa el tipo elegido en 'Nueva relación' (con su nombre real, no el de pantalla)", async () => {
      const { createDocument } = setup();
      fireEvent.change(screen.getByLabelText("Nueva relación"), { target: { value: "plazo_de" } });
      await act(async () => rf.props.onConnect({ source: "a1", target: "a4" }));
      expect(createDocument).toHaveBeenCalledWith("RelationDoc", expect.any(String), expect.objectContaining({ relation_type: "plazo_de" }));
    });

    it("duplicada: aviso visible y no crea nada", async () => {
      const { createDocument } = setup();
      fireEvent.change(screen.getByLabelText("Nueva relación"), { target: { value: "motiva" } });
      await act(async () => rf.props.onConnect({ source: "a5", target: "a2" }));
      expect(createDocument).not.toHaveBeenCalled();
      expect(screen.getByRole("alert")).toHaveTextContent(/Ya existe «motiva»/);
    });

    it("tipo que no admite grupo (plazo_de) soltado sobre un subgrupo: aviso claro, nada creado", async () => {
      const { createDocument } = setup();
      fireEvent.change(screen.getByLabelText("Nueva relación"), { target: { value: "plazo_de" } });
      await act(async () => rf.props.onConnect({ source: "g:infra.proveedores", target: "a3" }));
      expect(createDocument).not.toHaveBeenCalled();
      expect(screen.getByRole("alert")).toHaveTextContent(/«plazo de» no admite un grupo o una base como extremo/);
    });

    it("sobre un subgrupo sin GrupoDoc: crea el GrupoDoc (slug con guiones, título de display) y luego el RelationDoc con GrupoDoc:<slug>", async () => {
      const { createDocument } = setup();
      fireEvent.change(screen.getByLabelText("Nueva relación"), { target: { value: "afecta" } });
      await act(async () => rf.props.onConnect({ source: "a3", target: "g:infra.proveedores" }));
      expect(createDocument.mock.calls.map((c: any[]) => [c[0], c[1]])).toEqual([
        ["GrupoDoc", "infra-proveedores"],
        ["RelationDoc", "rel-1"],
      ]);
      expect((createDocument.mock.calls[0] as unknown[])[2]).toEqual({ title: "Proveedores", tag: "infra.proveedores", description: "" });
      expect((createDocument.mock.calls[1] as unknown[])[2]).toMatchObject({ source_id: "AtomDoc:a3", target_id: "GrupoDoc:infra-proveedores" });
    });

    it("sobre una base sin GrupoDoc: GrupoDoc con el slug de la base y la relación", async () => {
      const { createDocument } = setup();
      fireEvent.change(screen.getByLabelText("Nueva relación"), { target: { value: "afecta" } });
      await act(async () => rf.props.onConnect({ source: "a3", target: "g:reuniones" }));
      expect(createDocument.mock.calls.map((c: any[]) => [c[0], c[1]])).toEqual([
        ["GrupoDoc", "reuniones"],
        ["RelationDoc", "rel-1"],
      ]);
      expect((createDocument.mock.calls[1] as unknown[])[2]).toMatchObject({ target_id: "GrupoDoc:reuniones" });
    });

    it("sobre un subgrupo que ya tiene GrupoDoc: solo crea la relación", async () => {
      const { createDocument } = setup();
      fireEvent.change(screen.getByLabelText("Nueva relación"), { target: { value: "afecta" } });
      await act(async () => rf.props.onConnect({ source: "a1", target: "g:infra.ingesta" }));
      expect(createDocument.mock.calls.map((c: any[]) => c[0])).toEqual(["RelationDoc"]);
    });

    it("soltar sobre el cuerpo de una región (sin asa) crea la relación con el grupo; 409 del grupo se tolera", async () => {
      const createDocument = vi.fn(async (model: string) => {
        if (model === "GrupoDoc") throw Object.assign(new Error("existe"), { status: 409 });
        return { ok: true, id: "x", version: "v" };
      });
      setup({}, { createDocument } as any);
      fireEvent.change(screen.getByLabelText("Nueva relación"), { target: { value: "afecta" } });
      const el = document.createElement("div");
      el.className = "react-flow__node";
      el.setAttribute("data-id", "g:reuniones");
      document.body.appendChild(el);
      (document as any).elementFromPoint = vi.fn(() => el);
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
      fireEvent.click(screen.getAllByTitle("Plegar")[1]!);
      fireEvent.change(screen.getByLabelText("Nueva relación"), { target: { value: "afecta" } });
      await act(async () => rf.props.onConnect({ source: "a1", target: "g:infra" }));
      expect(screen.getByRole("alert")).toHaveTextContent(/No se creó la relación: payload inválido/);
      expect(rf.props.nodes.find((n: any) => n.id === "g:infra").type).toBe("folded");
    });
  });
});
