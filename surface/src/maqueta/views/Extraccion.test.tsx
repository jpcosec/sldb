import { useState } from "react";
import { describe, expect, it, vi } from "vitest";
import { act, fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import fixture from "../../core/__fixtures__/atoms.json";
import { SaveConflictError, SldbHttpError, type SldbClient } from "../../core/client";
import type { Acta, GraphDocument } from "../../core/contract";
import { SldbProvider } from "../../react/context";
import { useAtomStore } from "../../views/atoms/useAtomStore";
import Extraccion from "./Extraccion";

const DOCS = fixture.documents as unknown as GraphDocument[];

/** Caso con tres fuentes (prompt, folleto, mensaje) y un átomo en cada una. */
const B_P = "Eres el asistente.\n\nNunca sugieras dosis.";
const B_F = "Folleto uno.\n\nLa teleconsulta es gratuita.";
const B_M = "Hola, tengo una duda.";
const doc = (id: string, model_name: string, payload: Record<string, unknown>) => ({ id, model_name, path: `docs/${id}.md`, version: "v", semantic_tags: [], payload }) as unknown as GraphDocument;
const at = (id: string, source: string, body: string, quote: string, kind: string, status = "propuesto") =>
  doc(id, "AtomDoc", { kind, status, source, source_field: "body", start: body.indexOf(quote), end: body.indexOf(quote) + quote.length, tags: ["programa.asistente"], text: quote, quote, conf: 0.9 });
const CASO: GraphDocument[] = [
  doc("system-prompt", "FuenteDoc", { title: "System prompt del asistente", tipo: "prompt", base: "Programa", descripcion: "Instrucción de sistema.", body: B_P }),
  doc("folleto", "FuenteDoc", { title: "Folleto del programa", tipo: "folleto", base: "Programa", descripcion: "", body: B_F }),
  doc("mensaje-paciente", "FuenteDoc", { title: "Mensaje de la paciente", tipo: "mensaje", base: "Paciente", descripcion: "", body: B_M }),
  doc("programa-asistente", "GrupoDoc", { tag: "programa.asistente", title: "Asistente", description: "" }),
  at("p1", "FuenteDoc:system-prompt", B_P, "Nunca sugieras dosis", "regla", "confirmado"),
  at("f1", "FuenteDoc:folleto", B_F, "La teleconsulta es gratuita", "criterio"),
  at("f2", "FuenteDoc:folleto", B_F, "Folleto uno", "logistica"),
  at("c1", "FuenteDoc:mensaje-paciente", B_M, "tengo una duda", "pregunta"),
];

function Harness({ initialFocus = null }: { initialFocus?: string | null }) {
  const store = useAtomStore();
  const [focus, setFocus] = useState<string | null>(initialFocus);
  const acta = store.actas[0] ?? (store.fuentes[0] as unknown as Acta | undefined);
  if (!acta) return <div>cargando</div>;
  return <Extraccion store={store} acta={acta} fuentes={store.fuentes} informe={undefined} respuesta={undefined} caso={null} focusId={focus} setFocusId={setFocus} go={() => {}} />;
}

function mount(overrides: Partial<SldbClient> = {}, initialFocus: string | null = null, docsIn: GraphDocument[] = DOCS) {
  const save = vi.fn(async (_c: unknown[]) => ({ ok: true, saved: [] as string[] }));
  const createDocument = vi.fn(async (_m: string, name: string, _p: unknown) => ({ ok: true, id: name, version: "v" }));
  const client = {
    documents: async () => docsIn,
    getEdges: async () => [],
    document: async (id: string) => {
      const d = docsIn.find((x) => x.id === id)!;
      return { id: d.id, model_name: d.model_name, path: d.path, payload: d.payload };
    },
    save,
    createDocument,
    ...overrides,
  } as unknown as SldbClient;
  render(
    <SldbProvider client={client}>
      <Harness initialFocus={initialFocus} />
    </SldbProvider>,
  );
  return { save, createDocument };
}

const card = (id: string) => document.getElementById(`card-${id}`) as HTMLElement;
const mark = (id: string) => document.querySelector(`[data-atom="${id}"]`) as HTMLElement | null;

describe("Extracción de la maqueta", () => {
  it("cuenta, subraya con offsets reales y avisa de anclas movidas y huérfanas", async () => {
    mount();
    expect(await screen.findByText("5 átomos en este documento, 3 sin confirmar")).toBeInTheDocument();
    await waitFor(() => expect(mark("a1")).toHaveTextContent("Reunión del 14/09"));
    expect(mark("a1")!.className).toContain("anc t-entidad");
    expect(mark("a1")!.className).not.toContain("is-draft");
    expect(mark("a5")!.className).toContain("is-draft");
    // movida: subrayada donde está la cita, con Reparar
    expect(mark("a3")).toHaveTextContent("Tomás será responsable de la ingesta");
    expect(within(card("a3")).getByText("Ancla movida")).toBeInTheDocument();
    expect(within(card("a3")).getByRole("button", { name: "Reparar" })).toBeInTheDocument();
    // huérfana: sin subrayado
    expect(mark("a4")).toBeNull();
    expect(within(card("a4")).getByText("El texto cambió")).toBeInTheDocument();
    // descartado: fuera de la lista principal, dentro de Descartados
    expect(screen.getByText("Descartados (1)").closest("details")).toContainElement(screen.getByRole("button", { name: "Restaurar" }));
    expect(screen.getByRole("region", { name: "Texto fuente" }).querySelector(".ProseMirror")).toBeTruthy();
  });

  it("con una sola fuente hay una sola pestaña, con su contador", async () => {
    mount();
    await screen.findByText("5 átomos en este documento, 3 sin confirmar");
    const tabs = screen.getAllByRole("tab");
    expect(tabs).toHaveLength(1);
    expect(tabs[0]).toHaveAttribute("aria-selected", "true");
    expect(tabs[0]).toHaveTextContent("5");
  });

  it("Re-extraer queda visible pero deshabilitado, explicando por qué", async () => {
    mount();
    const b = await screen.findByRole("button", { name: "Re-extraer lo no confirmado" });
    expect(b).toBeDisabled();
    expect(b).toHaveAttribute("title", "Falta el extractor: aún no hay un modelo de extracción conectado al servidor");
  });

  it("filtra por tipo con aria-pressed", async () => {
    mount();
    await screen.findByText("5 átomos en este documento, 3 sin confirmar");
    const riesgo = within(screen.getByRole("group", { name: "Filtrar por tipo" })).getByRole("button", { name: "Riesgo" });
    fireEvent.click(riesgo);
    expect(riesgo).toHaveAttribute("aria-pressed", "true");
    expect(card("a4")).toBeTruthy();
    expect(mark("a1")).toBeNull();
  });

  it("Baja confianza primero ordena las tarjetas por confianza", async () => {
    const docs = DOCS.map((d) => (d.id === "a5" ? { ...d, payload: { ...d.payload, conf: 0.2 } } : d));
    mount({ documents: async () => docs });
    await screen.findByText("5 átomos en este documento, 3 sin confirmar");
    const order = () => [...document.querySelectorAll("aside article")].map((a) => a.parentElement!.id);
    expect(order()[0]).toBe("card-a1");
    fireEvent.click(screen.getByLabelText("Baja confianza primero"));
    expect(order()[0]).toBe("card-a5");
  });

  it("Confirmar, Descartar, Restaurar y cambiar tipo persisten con saveField", async () => {
    const { save } = mount();
    await screen.findByText("5 átomos en este documento, 3 sin confirmar");
    fireEvent.click(within(card("a5")).getByRole("button", { name: "Confirmar" }));
    await waitFor(() => expect(save).toHaveBeenCalledTimes(1));
    expect(save.mock.calls[0]![0]).toMatchObject([{ id: "a5", action: "update", payload: { status: "confirmado" } }]);
    fireEvent.click(within(card("a5")).getByRole("button", { name: "Descartar" }));
    await waitFor(() => expect(save).toHaveBeenCalledTimes(2));
    expect(save.mock.calls[1]![0]).toMatchObject([{ id: "a5", payload: { status: "descartado" } }]);
    fireEvent.click(screen.getByRole("button", { name: "Restaurar" }));
    await waitFor(() => expect(save).toHaveBeenCalledTimes(3));
    expect(save.mock.calls[2]![0]).toMatchObject([{ id: "a6", payload: { status: "propuesto" } }]);
    fireEvent.click(within(card("a5")).getByRole("button", { name: /Pendiente ▾/ }));
    fireEvent.click(screen.getByRole("menuitem", { name: "Riesgo" }));
    await waitFor(() => expect(save).toHaveBeenCalledTimes(4));
    expect(save.mock.calls[3]![0]).toMatchObject([{ id: "a5", payload: { kind: "riesgo" } }]);
  });

  it("Reparar persiste start y end donde está la cita", async () => {
    const { save } = mount();
    await screen.findByText("5 átomos en este documento, 3 sin confirmar");
    fireEvent.click(within(card("a3")).getByRole("button", { name: "Reparar" }));
    await waitFor(() => expect(save).toHaveBeenCalledTimes(2));
    const body = (DOCS.find((d) => d.id === "acta")!.payload.body as string);
    const at = body.indexOf("Tomás será responsable de la ingesta");
    const payloads = save.mock.calls.map((c) => (c[0] as { payload: Record<string, unknown> }[])[0]!.payload);
    expect(payloads.some((p) => p.start === at)).toBe(true);
    expect(payloads.some((p) => p.end === at + "Tomás será responsable de la ingesta".length)).toBe(true);
  });

  it("un fallo de escritura se muestra en la tarjeta; un conflicto ofrece Recargar", async () => {
    const save = vi.fn(async () => {
      throw new SaveConflictError("cambió", {});
    });
    mount({ save } as unknown as Partial<SldbClient>);
    await screen.findByText("5 átomos en este documento, 3 sin confirmar");
    fireEvent.click(within(card("a5")).getByRole("button", { name: "Confirmar" }));
    const alert = await within(card("a5")).findByRole("alert");
    expect(alert).toHaveTextContent(/cambió en el servidor/);
    expect(within(card("a5")).getByRole("button", { name: "Recargar" })).toBeInTheDocument();
    // otro error: sin Recargar
    save.mockImplementation(async () => {
      throw new SldbHttpError("boom", 500, null);
    });
    fireEvent.click(within(card("a1")).getByRole("button", { name: "Descartar" }));
    expect(await within(card("a1")).findByRole("alert")).toHaveTextContent("No se pudo guardar: boom");
    expect(within(card("a1")).queryByRole("button", { name: "Recargar" })).toBeNull();
  });

  it("deshabilita los botones de la tarjeta mientras guarda", async () => {
    let release: () => void = () => {};
    const save = vi.fn(() => new Promise<{ ok: boolean; saved: string[] }>((r) => (release = () => r({ ok: true, saved: [] }))));
    mount({ save } as unknown as Partial<SldbClient>);
    await screen.findByText("5 átomos en este documento, 3 sin confirmar");
    fireEvent.click(within(card("a5")).getByRole("button", { name: "Confirmar" }));
    await waitFor(() => expect(within(card("a5")).getByRole("button", { name: "Descartar" })).toBeDisabled());
    await act(async () => release());
  });

  it("crear átomo desde la selección: offsets reales sobre acta.body", async () => {
    const body = "Primero uno.\n\nSegundo dos tres.\n\nTercero.";
    const docs = DOCS.map((d) => (d.id === "acta" ? { ...d, payload: { ...d.payload, body } } : d.model_name === "AtomDoc" ? { ...d, payload: { ...d.payload, status: "descartado" } } : d));
    const { createDocument } = mount({ documents: async () => docs });
    await screen.findByText("0 átomos en este documento, 0 sin confirmar");
    const p2 = document.querySelectorAll(".ProseMirror p")[1]!.firstChild as Text; // "Segundo dos tres."
    (document.querySelector(".ProseMirror") as HTMLElement).focus();
    const sel = window.getSelection()!;
    const range = document.createRange();
    range.setStart(p2, 8);
    range.setEnd(p2, 11); // "dos"
    sel.removeAllRanges();
    sel.addRange(range);
    fireEvent(document, new Event("selectionchange"));
    const btn = await screen.findByRole("button", { name: "Crear átomo desde la selección" });
    fireEvent.click(btn);
    await waitFor(() => expect(createDocument).toHaveBeenCalledTimes(1));
    const [model, name, payload] = createDocument.mock.calls[0]! as [string, string, Record<string, unknown>];
    expect(model).toBe("AtomDoc");
    expect(name).toBe("a7");
    expect(payload).toMatchObject({ kind: "hecho", status: "propuesto", source: "ActaDoc:acta", quote: "dos" });
    expect(body.slice(payload.start as number, payload.end as number)).toBe("dos");
  });

  it("rechaza selecciones que cruzan párrafos con un mensaje visible", async () => {
    const body = "Primero uno.\n\nSegundo dos tres.";
    const docs = DOCS.map((d) => (d.id === "acta" ? { ...d, payload: { ...d.payload, body } } : d));
    const { createDocument } = mount({ documents: async () => docs });
    await screen.findByText(/átomos en este documento, /);
    (document.querySelector(".ProseMirror") as HTMLElement).focus();
    const ps = document.querySelectorAll(".ProseMirror p");
    const range = document.createRange();
    range.setStart(ps[0]!.firstChild!, 3);
    range.setEnd(ps[1]!.firstChild!, 4);
    window.getSelection()!.removeAllRanges();
    window.getSelection()!.addRange(range);
    fireEvent(document, new Event("selectionchange"));
    fireEvent.click(await screen.findByRole("button", { name: "Crear átomo desde la selección" }));
    expect(await screen.findByRole("alert")).toHaveTextContent(/cruza un límite de párrafo/);
    expect(createDocument).not.toHaveBeenCalled();
  });

  it("caso con varias fuentes: pestañas con ícono y contador, átomos y tipos de la fuente activa", async () => {
    mount({}, null, CASO);
    await screen.findByText("1 átomos en este documento, 0 sin confirmar");
    const tabs = screen.getAllByRole("tab");
    expect(tabs.map((t) => t.textContent)).toEqual(["\u2699\uFE0FSystem prompt del asistente1", "\u{1F4C4}Folleto del programa2", "\u{1F4AC}Mensaje de la paciente1"]);
    expect(tabs[0]).toHaveAttribute("aria-selected", "true");
    expect(screen.getByRole("heading", { name: "System prompt del asistente" })).toBeInTheDocument();
    expect(screen.getByText("Instrucción de sistema.")).toBeInTheDocument();
    expect(document.querySelector(".src-prompt")).toBeTruthy();
    expect(card("p1")).toBeTruthy();
    expect(card("f1")).toBeNull();
    // tag como subgrupo en display
    expect(within(card("p1")).getByText("Asistente")).toBeInTheDocument();
    // filtros: los cinco tipos del caso
    const group = within(screen.getByRole("group", { name: "Filtrar por tipo" }));
    expect(group.getAllByRole("button").map((b) => b.textContent)).toEqual(["Regla", "Criterio", "Logística", "Dato del paciente", "Pregunta"]);
    await waitFor(() => expect(mark("p1")).toHaveTextContent("Nunca sugieras dosis"));
    expect(mark("p1")!.className).toContain("t-regla");
    // cambiar de pestaña
    fireEvent.click(tabs[1]!);
    await screen.findByText("2 átomos en este documento, 2 sin confirmar");
    expect(card("p1")).toBeNull();
    await waitFor(() => expect(mark("f1")).toHaveTextContent("La teleconsulta es gratuita"));
    expect(document.querySelector(".src-prompt")).toBeNull();
    expect(document.querySelector(".src-paciente")).toBeNull();
    fireEvent.click(tabs[2]!);
    await screen.findByText("1 átomos en este documento, 1 sin confirmar");
    expect(document.querySelector(".src-paciente")).toBeTruthy();
  });

  it("foco en un átomo de otra fuente activa esa pestaña", async () => {
    mount({}, "c1", CASO);
    await screen.findByText("1 átomos en este documento, 1 sin confirmar");
    expect(screen.getByRole("tab", { name: /Mensaje de la paciente/ })).toHaveAttribute("aria-selected", "true");
    await waitFor(() => expect(mark("c1")).toHaveTextContent("tengo una duda"));
  });

  it("crear un átomo en la fuente folleto ancla contra el body de esa fuente y usa un id libre", async () => {
    const { createDocument } = mount({}, null, CASO);
    await screen.findByRole("tab", { name: /Folleto/ });
    fireEvent.click(screen.getByRole("tab", { name: /Folleto/ }));
    await screen.findByText("2 átomos en este documento, 2 sin confirmar");
    await waitFor(() => expect(document.querySelectorAll(".ProseMirror p")).toHaveLength(2));
    await waitFor(() => expect(mark("f1")).toBeTruthy());
    const p2 = mark("f1")!.firstChild as Text; // "La teleconsulta es gratuita" (subrayado de f1)
    (document.querySelector(".ProseMirror") as HTMLElement).focus();
    const range = document.createRange();
    range.setStart(p2, 3);
    range.setEnd(p2, 15); // "teleconsulta"
    window.getSelection()!.removeAllRanges();
    window.getSelection()!.addRange(range);
    fireEvent(document, new Event("selectionchange"));
    fireEvent.click(await screen.findByRole("button", { name: "Crear átomo desde la selección" }));
    await waitFor(() => expect(createDocument).toHaveBeenCalledTimes(1));
    const [, name, payload] = createDocument.mock.calls[0]! as [string, string, Record<string, unknown>];
    expect(name).toBe("f3");
    expect(payload).toMatchObject({ kind: "regla", source: "FuenteDoc:folleto", quote: "teleconsulta" });
    expect(B_F.slice(payload.start as number, payload.end as number)).toBe("teleconsulta");
  });
});
