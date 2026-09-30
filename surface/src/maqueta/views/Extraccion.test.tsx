import { useState } from "react";
import { describe, expect, it, vi } from "vitest";
import { act, fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import fixture from "../../core/__fixtures__/atoms.json";
import { SaveConflictError, SldbHttpError, type SldbClient } from "../../core/client";
import type { GraphDocument } from "../../core/contract";
import { SldbProvider } from "../../react/context";
import { useAtomStore } from "../../views/atoms/useAtomStore";
import Extraccion from "./Extraccion";

const DOCS = fixture.documents as unknown as GraphDocument[];

function Harness({ initialFocus = null }: { initialFocus?: string | null }) {
  const store = useAtomStore();
  const [focus, setFocus] = useState<string | null>(initialFocus);
  const acta = store.actas[0];
  if (!acta) return <div>cargando</div>;
  return <Extraccion store={store} acta={acta} focusId={focus} setFocusId={setFocus} go={() => {}} />;
}

function mount(overrides: Partial<SldbClient> = {}, initialFocus: string | null = null) {
  const save = vi.fn(async (_c: unknown[]) => ({ ok: true, saved: [] as string[] }));
  const createDocument = vi.fn(async (_m: string, name: string, _p: unknown) => ({ ok: true, id: name, version: "v" }));
  const client = {
    documents: async () => DOCS,
    getEdges: async () => [],
    document: async (id: string) => {
      const d = DOCS.find((x) => x.id === id)!;
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
    expect(await screen.findByText("5 átomos, 3 sin confirmar")).toBeInTheDocument();
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

  it("Re-extraer queda visible pero deshabilitado, explicando por qué", async () => {
    mount();
    const b = await screen.findByRole("button", { name: "Re-extraer lo no confirmado" });
    expect(b).toBeDisabled();
    expect(b).toHaveAttribute("title", "Falta el extractor: aún no hay un modelo de extracción conectado al servidor");
  });

  it("filtra por tipo con aria-pressed", async () => {
    mount();
    await screen.findByText("5 átomos, 3 sin confirmar");
    const riesgo = within(screen.getByRole("group", { name: "Filtrar por tipo" })).getByRole("button", { name: "Riesgo" });
    fireEvent.click(riesgo);
    expect(riesgo).toHaveAttribute("aria-pressed", "true");
    expect(card("a4")).toBeTruthy();
    expect(mark("a1")).toBeNull();
  });

  it("Baja confianza primero ordena las tarjetas por confianza", async () => {
    const docs = DOCS.map((d) => (d.id === "a5" ? { ...d, payload: { ...d.payload, conf: 0.2 } } : d));
    mount({ documents: async () => docs });
    await screen.findByText("5 átomos, 3 sin confirmar");
    const order = () => [...document.querySelectorAll("aside article")].map((a) => a.parentElement!.id);
    expect(order()[0]).toBe("card-a1");
    fireEvent.click(screen.getByLabelText("Baja confianza primero"));
    expect(order()[0]).toBe("card-a5");
  });

  it("Confirmar, Descartar, Restaurar y cambiar tipo persisten con saveField", async () => {
    const { save } = mount();
    await screen.findByText("5 átomos, 3 sin confirmar");
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
    await screen.findByText("5 átomos, 3 sin confirmar");
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
    await screen.findByText("5 átomos, 3 sin confirmar");
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
    await screen.findByText("5 átomos, 3 sin confirmar");
    fireEvent.click(within(card("a5")).getByRole("button", { name: "Confirmar" }));
    await waitFor(() => expect(within(card("a5")).getByRole("button", { name: "Descartar" })).toBeDisabled());
    await act(async () => release());
  });

  it("crear átomo desde la selección: offsets reales sobre acta.body", async () => {
    const body = "Primero uno.\n\nSegundo dos tres.\n\nTercero.";
    const docs = DOCS.map((d) => (d.id === "acta" ? { ...d, payload: { ...d.payload, body } } : d.model_name === "AtomDoc" ? { ...d, payload: { ...d.payload, status: "descartado" } } : d));
    const { createDocument } = mount({ documents: async () => docs });
    await screen.findByText("0 átomos, 0 sin confirmar");
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
    await screen.findByText(/átomos, /);
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
});
