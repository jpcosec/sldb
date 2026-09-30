import { beforeEach, describe, expect, it, vi } from "vitest";
import { fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import type { SldbClient } from "../../core/client";
import type { Edge, GraphDocument } from "../../core/contract";
import fixture from "../../core/__fixtures__/atoms.json";
import { SldbProvider } from "../../react/context";
import AtomosGrafoView from "./AtomosGrafoView";

const docs = fixture.documents as unknown as GraphDocument[];
const edges = fixture.edges as Edge[];

function mount(opts: { documents?: () => Promise<GraphDocument[]>; getEdges?: () => Promise<Edge[]>; createDocument?: ReturnType<typeof vi.fn> } = {}) {
  const createDocument = opts.createDocument ?? vi.fn(async () => ({ ok: true, id: "rel-1", version: "v" }));
  const client = {
    documents: opts.documents ?? (async () => docs),
    getEdges: opts.getEdges ?? (async () => edges),
    createDocument,
  } as unknown as SldbClient;
  render(
    <SldbProvider client={client}>
      <AtomosGrafoView />
    </SldbProvider>,
  );
  return { createDocument };
}

const node = (id: string) => document.querySelector(`[data-node-key="AtomDoc:${id}"]`) as SVGGElement;

/** Arrastra del átomo `from` al átomo `to` con pointer events. */
function connect(from: string, to: string) {
  fireEvent.pointerDown(node(from), { clientX: 10, clientY: 10, button: 0 });
  fireEvent.pointerMove(screen.getByRole("group", { name: "Grafo de átomos" }), { clientX: 60, clientY: 60 });
  fireEvent.pointerUp(node(to), { clientX: 80, clientY: 80 });
}

beforeEach(() => {
  window.location.hash = "";
});

describe("AtomosGrafoView", () => {
  it("muestra cargando y luego nodos (sin descartados) y aristas", async () => {
    mount();
    expect(screen.getByText(/Leyendo el grafo/)).toBeInTheDocument();
    await screen.findByRole("group", { name: "Grafo de átomos" });
    for (const id of ["a1", "a2", "a3", "a4", "a5"]) expect(node(id)).toBeTruthy();
    expect(node("a6")).toBeNull(); // descartado
    expect(screen.getByText(/5 átomos · 1 relación/)).toBeInTheDocument();
    // 1 directa + 2 heredadas del grupo infra; la referencia hacia el acta no se dibuja
    const aristas = screen.getAllByRole("button", { name: /^Relación motiva/ });
    expect(aristas).toHaveLength(3);
    expect(aristas.filter((a) => /heredada/.test(a.getAttribute("aria-label")!))).toHaveLength(2);
    expect(screen.getByRole("button", { name: /Decisión: Reemplazar el lote por una cola.*arquitectura/ })).toBeInTheDocument();
  });

  it("estado vacío", async () => {
    mount({ documents: async () => [], getEdges: async () => [] });
    expect(await screen.findByText("Sin átomos todavía")).toBeInTheDocument();
  });

  it("error de red con reintentar", async () => {
    let fail = true;
    mount({
      documents: async () => {
        if (fail) throw new Error("sin red");
        return docs;
      },
    });
    expect(await screen.findByText(/No se pudo leer el grafo: sin red/)).toBeInTheDocument();
    fail = false;
    fireEvent.click(screen.getByRole("button", { name: "Reintentar" }));
    await screen.findByRole("group", { name: "Grafo de átomos" });
    expect(node("a2")).toBeTruthy();
  });

  it("plegar un grupo deja un solo nodo y fusiona; desplegar lo restaura", async () => {
    mount();
    await screen.findByRole("group", { name: "Grafo de átomos" });
    fireEvent.click(screen.getByRole("button", { name: "Plegar grupo infra" }));
    expect(node("a2")).toBeNull();
    expect(document.querySelector('[data-node-key="group:infra"]')).toBeTruthy();
    expect(screen.queryAllByRole("button", { name: /^Relación motiva/ })).toHaveLength(0); // todas internas a infra
    fireEvent.click(screen.getByRole("button", { name: "Desplegar grupo infra" }));
    expect(node("a2")).toBeTruthy();
    expect(screen.getAllByRole("button", { name: /^Relación motiva/ })).toHaveLength(3);
  });

  it("clic en un grupo de la barra resalta sus átomos", async () => {
    mount();
    await screen.findByRole("group", { name: "Grafo de átomos" });
    const side = screen.getByRole("complementary", { name: "Grupos" });
    fireEvent.click(within(side).getByRole("button", { name: "reuniones" }));
    expect(node("a1")).not.toHaveClass("is-dim");
    expect(node("a2")).toHaveClass("is-dim");
    fireEvent.click(within(side).getByRole("button", { name: "reuniones" }));
    expect(node("a2")).not.toHaveClass("is-dim");
  });

  it("filtrar un tipo oculta sus aristas", async () => {
    mount();
    await screen.findByRole("group", { name: "Grafo de átomos" });
    fireEvent.click(screen.getByRole("button", { name: "motiva", pressed: true }));
    expect(screen.queryAllByRole("button", { name: /^Relación motiva/ })).toHaveLength(0);
  });

  it("inspector de átomo: relaciones, ancla, dirección y Ver en el texto; Escape cierra", async () => {
    mount();
    await screen.findByRole("group", { name: "Grafo de átomos" });
    fireEvent.keyDown(node("a2"), { key: "Enter" });
    const insp = screen.getByRole("complementary", { name: "Inspector" });
    expect(within(insp).getByText("AtomDoc:a2")).toBeInTheDocument();
    expect(within(insp).getAllByLabelText("entrante")).toHaveLength(3); // a5 directa + a3, a4 heredadas de infra
    expect(within(insp).queryAllByLabelText("saliente")).toHaveLength(0);
    expect(within(insp).getByTestId("anchor-state")).toHaveTextContent(/intacta|movida|huérfana/);
    fireEvent.click(within(insp).getByRole("button", { name: "Ver en el texto" }));
    expect(window.location.hash).toBe("#/atomos/texto/acta?atom=a2"); // lleva el átomo enfocado
    fireEvent.keyDown(node("a2"), { key: "Escape" });
    expect(screen.queryByRole("complementary", { name: "Inspector" })).toBeNull();
  });

  it("inspector de arista: origen, destino, tipo y RelationDoc", async () => {
    mount();
    await screen.findByRole("group", { name: "Grafo de átomos" });
    const direct = screen.getAllByRole("button", { name: /^Relación motiva:/ }).find((e) => !/heredada/.test(e.getAttribute("aria-label")!))!;
    fireEvent.click(direct);
    const insp = screen.getByRole("complementary", { name: "Inspector" });
    expect(within(insp).getByText("r1")).toBeInTheDocument();
    expect(within(insp).getByText("Relación explícita.")).toBeInTheDocument();
  });

  it("arrastrar de un átomo a otro abre el menú con los tipos válidos y crea el RelationDoc", async () => {
    const { createDocument } = mount();
    await screen.findByRole("group", { name: "Grafo de átomos" });
    connect("a1", "a3");
    const menu = screen.getByRole("menu", { name: "Tipo de relación" });
    // `cubre` no admite átomos como origen: solo `motiva`
    expect(within(menu).getAllByRole("menuitem").map((b) => b.textContent)).toEqual([expect.stringContaining("motiva")]);
    fireEvent.click(within(menu).getByRole("menuitem"));
    await waitFor(() => expect(createDocument).toHaveBeenCalledTimes(1));
    expect(createDocument).toHaveBeenCalledWith("RelationDoc", "rel-1", {
      title: expect.stringContaining("motiva"),
      source_id: "AtomDoc:a1",
      target_id: "AtomDoc:a3",
      relation_type: "motiva",
      condition: "",
      notes: "",
    });
    expect(await screen.findByText(/Relación rel-1 creada/)).toBeInTheDocument();
  });

  it("si la relación ya existe no hay tipos válidos: mensaje claro y no crea", async () => {
    const { createDocument } = mount();
    await screen.findByRole("group", { name: "Grafo de átomos" });
    connect("a5", "a2"); // ya existe a5 motiva a2
    expect(screen.getByRole("alert")).toHaveTextContent(/No hay tipos de relación válidos/);
    expect(screen.queryByRole("menuitem")).toBeNull();
    expect(createDocument).not.toHaveBeenCalled();
  });

  it("soltar fuera de un átomo no hace nada; soltar sobre sí mismo tampoco", async () => {
    mount();
    await screen.findByRole("group", { name: "Grafo de átomos" });
    connect("a1", "a1");
    expect(screen.queryByRole("menu")).toBeNull();
  });

  it("un error 409 del servidor se muestra y conserva la vista", async () => {
    const createDocument = vi.fn(async () => {
      throw new Error("409 documento ya existe");
    });
    mount({ createDocument });
    await screen.findByRole("group", { name: "Grafo de átomos" });
    fireEvent.click(screen.getByRole("button", { name: "Plegar grupo reuniones" }));
    fireEvent.click(screen.getByRole("button", { name: "Desplegar grupo reuniones" }));
    connect("a1", "a3");
    fireEvent.click(screen.getByRole("menuitem"));
    expect(await screen.findByText(/No se creó la relación: 409 documento ya existe/)).toBeInTheDocument();
    expect(node("a1")).toBeTruthy();
    expect(screen.queryByRole("menu")).toBeNull();
  });

  it("el nombre rel-<n> toma el siguiente libre", async () => {
    const withRel = [...docs, { id: "rel-4", model_name: "RelationDoc", path: "docs/rel-4.md", payload: {}, semantic_tags: [] } as unknown as GraphDocument];
    const { createDocument } = mount({ documents: async () => withRel });
    await screen.findByRole("group", { name: "Grafo de átomos" });
    connect("a1", "a3");
    fireEvent.click(screen.getByRole("menuitem"));
    await waitFor(() => expect(createDocument).toHaveBeenCalled());
    expect(createDocument.mock.calls[0]![1]).toBe("rel-5");
  });
});
