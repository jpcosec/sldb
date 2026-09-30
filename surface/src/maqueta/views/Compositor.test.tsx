import { describe, expect, it, vi } from "vitest";
import { fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import fixture from "../../core/__fixtures__/atoms.json";
import { SaveConflictError, type SldbClient } from "../../core/client";
import type { Edge, GraphDocument, SaveResult } from "../../core/contract";
import { SldbProvider } from "../../react/context";
import { useAtomStore } from "../../views/atoms/useAtomStore";
import Compositor from "./Compositor";

const clone = <T,>(x: T): T => JSON.parse(JSON.stringify(x));
const RENDERED = `# Informe de prueba\n\n## Resumen\n\n- Hecho uno\n\n## Decisiones\n\n- D1\n\n## Riesgos\n\n## Pendientes\n`;
const pubDoc = (version: number): GraphDocument => ({
  id: `inf1-v${version}`,
  model_name: "PublicacionDoc",
  path: `docs/inf1-v${version}.md`,
  payload: { informe: "inf1", version, title: "Informe de prueba", atoms: [], resumen: "", decisiones: "", riesgos: "", pendientes: "" },
});

function Host({ go }: { go: (tab: string, id?: string | null) => void }) {
  const store = useAtomStore();
  if (store.status !== "ok") return <div>cargando</div>;
  const acta = store.actas[0]!;
  return <Compositor store={store} acta={acta} fuentes={[]} informe={store.informes[0]} respuesta={undefined} caso={null} focusId={null} setFocusId={() => {}} go={go as never} />;
}

function mount(opts: { published?: number[]; noInforme?: boolean; saveImpl?: (ops: any[]) => Promise<SaveResult>; createImpl?: (m: string, n: string, p: any, docs: GraphDocument[]) => Promise<any>; resumenQuery?: string; mutate?: (inf: GraphDocument) => void } = {}) {
  const docs = clone(fixture.documents) as unknown as GraphDocument[];
  const edges = clone(fixture.edges) as Edge[];
  const inf = docs.find((d) => d.id === "inf1")!;
  inf.payload.resumen_query = opts.resumenQuery ?? "tipo:hecho";
  inf.payload.riesgos_query = "tipo:riesgo";
  inf.payload.riesgos_modo = "tabla";
  inf.payload.title = "Informe de prueba";
  opts.mutate?.(inf);
  if (opts.noInforme) docs.splice(docs.indexOf(inf), 1);
  for (const v of opts.published ?? []) docs.push(pubDoc(v));
  const save = vi.fn(
    opts.saveImpl ??
      (async (ops: any[]) => {
        for (const op of ops) docs.find((x) => x.id === op.id)!.payload = clone(op.payload);
        return { ok: true, saved: ops.map((o) => o.id) };
      }),
  );
  const createDocument = vi.fn(
    opts.createImpl ??
      (async (model: string, name: string, payload: any, all: GraphDocument[]) => {
        if (all.some((d) => d.id === name)) throw new SaveConflictError("ya existe", null);
        all.push({ id: name, model_name: model, path: `docs/${name}.md`, payload });
        return { ok: true, id: name, version: "h" };
      }),
  );
  const client = {
    documents: async () => clone(docs),
    getEdges: async () => clone(edges),
    document: async (id: string) => clone(docs.find((d) => d.id === id)!),
    render: async () => RENDERED,
    createDocument: (m: string, n: string, p: any) => createDocument(m, n, p, docs),
    save,
  } as unknown as SldbClient;
  const go = vi.fn();
  render(
    <SldbProvider client={client}>
      <Host go={go} />
    </SldbProvider>,
  );
  return { save, docs, go, createDocument };
}

const field = (save: ReturnType<typeof vi.fn>, call: number, f: string) => (save.mock.calls[call]![0][0].payload as Record<string, unknown>)[f];
const slotSection = () => screen.getByRole("region", { name: "Slot seleccionado" });
const card = (text: string) => within(slotSection()).getByText(text).closest("li") as HTMLElement;

describe("Compositor (maqueta)", () => {
  it("barra, esqueleto con contadores y punto de nuevos, y gate", async () => {
    mount({ published: [1] });
    expect(await screen.findByText("Informe de prueba", { selector: "span" })).toBeInTheDocument();
    expect(screen.getByText("Publicado como v1.")).toBeInTheDocument();
    expect(screen.getByText("Desde entonces: 2 átomos nuevos por revisar")).toBeInTheDocument();
    const publicar = screen.getByRole("button", { name: "Publicar v2" });
    expect(publicar).toBeDisabled();
    expect(publicar).toHaveAttribute("title", "Revisa los átomos nuevos antes de republicar");
    const nav = screen.getByRole("navigation", { name: "Esqueleto del documento" });
    expect(within(nav).getAllByRole("button")).toHaveLength(5);
    expect(within(nav).getByRole("button", { name: /Resumen/ })).toHaveAttribute("aria-current", "true");
    expect(within(nav).getByRole("button", { name: /Riesgos/ }).querySelector("[title='Tiene átomos nuevos sin revisar']")).not.toBeNull();
    expect(within(nav).getByRole("button", { name: /Decisiones/ }).querySelector("[title='Tiene átomos nuevos sin revisar']")).toBeNull();
    const add = within(nav).getByRole("button", { name: "Agregar sección" });
    expect(add).toBeDisabled();
    expect(add).toHaveAttribute("title", "Las secciones las define el tipo de informe");
  });

  it("el slot muestra sus estados: nuevo primero, por consulta, fijado y excluido", async () => {
    mount();
    await screen.findByLabelText("Documento final");
    expect(within(slotSection()).getByText("Átomos (2)")).toBeInTheDocument();
    expect(within(card("Reunión del 14/09")).queryByText("Nuevo, sin revisar")).toBeNull();
    fireEvent.click(within(screen.getByRole("navigation", { name: "Esqueleto del documento" })).getByRole("button", { name: /Riesgos/ }));
    const lis = within(slotSection()).getAllByRole("listitem");
    expect(within(lis[0]!).getByText("Nuevo, sin revisar")).toBeInTheDocument();
    expect(within(lis[1]!).getByText("Excluido a mano")).toBeInTheDocument();
    expect(within(lis[1]!).getByRole("button", { name: "Volver a incluir" })).toBeInTheDocument();
  });

  it("Aceptar un nuevo lo persiste en la lista y baja el gate", async () => {
    const { save, docs } = mount();
    await screen.findByLabelText("Documento final");
    const nuevo = within(slotSection()).getAllByRole("listitem")[0]!;
    fireEvent.click(within(nuevo).getByRole("button", { name: "Aceptar" }));
    await waitFor(() => expect(save).toHaveBeenCalledTimes(1));
    expect(field(save, 0, "resumen")).toContain("docs/atoms/a3.md");
    await waitFor(() => expect(screen.getByText("Desde entonces: 1 átomo nuevo por revisar")).toBeInTheDocument());
    expect((docs.find((d) => d.id === "inf1")!.payload.resumen as string[]).includes("docs/atoms/a3.md")).toBe(true);
  });

  it("Excluir, Fijar, Soltar pin y Volver a incluir escriben un campo por cambio", async () => {
    const { save } = mount();
    await screen.findByLabelText("Documento final");
    fireEvent.click(within(within(slotSection()).getAllByRole("listitem")[0]!).getByRole("button", { name: "Excluir" }));
    await waitFor(() => expect(save).toHaveBeenCalledTimes(1));
    expect(field(save, 0, "resumen_excluidos")).toEqual(["docs/atoms/a3.md"]);
    fireEvent.click(await within(slotSection()).findByRole("button", { name: "Volver a incluir" }));
    await waitFor(() => expect(save).toHaveBeenCalledTimes(2));
    expect(field(save, 1, "resumen_excluidos")).toEqual([]);
    // Fijar el átomo de la lista y soltarlo (nuevo otra vez a3 queda arriba)
    const a1 = await waitFor(() => card("Reunión del 14/09"));
    fireEvent.click(within(a1).getByRole("button", { name: "Fijar" }));
    await waitFor(() => expect(save).toHaveBeenCalledTimes(3));
    expect(field(save, 2, "resumen_pins")).toEqual(["docs/atoms/a1.md"]);
    fireEvent.click(await within(slotSection()).findByRole("button", { name: "Soltar pin" }));
    await waitFor(() => expect(save).toHaveBeenCalledTimes(4));
    expect(field(save, 3, "resumen_pins")).toEqual([]);
  });

  it("cambiar el modo guarda _modo; el documento final cambia de forma", async () => {
    const { save } = mount();
    await screen.findByLabelText("Documento final");
    expect(screen.getByText("Vista previa unida, no redactada por un modelo")).toBeInTheDocument();
    fireEvent.click(screen.getByRole("radio", { name: "viñetas" }));
    await waitFor(() => expect(save).toHaveBeenCalledTimes(1));
    expect(field(save, 0, "resumen_modo")).toBe("viñetas");
    await waitFor(() => expect(screen.queryByText("Vista previa unida, no redactada por un modelo")).toBeNull());
    fireEvent.click(screen.getByRole("radio", { name: "tabla" }));
    await waitFor(() => expect(save).toHaveBeenCalledTimes(2));
    expect(field(save, 1, "resumen_modo")).toBe("tabla");
    const doc = screen.getByLabelText("Documento final");
    expect(await within(doc).findByRole("columnheader", { name: "Entidad" })).toBeInTheDocument();
    expect(within(doc).getByRole("columnheader", { name: "Evidencia" })).toBeInTheDocument();
    expect(within(doc).getByText("Sin relación")).toBeInTheDocument();
    expect(within(doc).getByText(/El documento guardado en disco siempre renderiza viñetas/)).toBeInTheDocument();
  });

  it("la consulta guarda _query al salir del campo y recalcula los nuevos; los chips salen del texto", async () => {
    const { save } = mount();
    await screen.findByLabelText("Documento final");
    expect(within(slotSection()).getByText("Tipo:")).toBeInTheDocument();
    const q = screen.getByLabelText("Qué va en este slot");
    fireEvent.change(q, { target: { value: "tipo:pendiente" } });
    expect(save).not.toHaveBeenCalled();
    fireEvent.blur(q);
    await waitFor(() => expect(save).toHaveBeenCalledTimes(1));
    expect(field(save, 0, "resumen_query")).toBe("tipo:pendiente");
    await waitFor(() => expect(within(slotSection()).getByText("Nuevo, sin revisar")).toBeInTheDocument());
    fireEvent.click(within(slotSection()).getByRole("button", { name: "Quitar filtro Tipo" }));
    await waitFor(() => expect(save).toHaveBeenCalledTimes(2));
    expect(field(save, 1, "resumen_query")).toBe("");
    await waitFor(() => expect(screen.queryByText("Desde entonces: 2 átomos nuevos por revisar")).toBeNull());
  });

  it("Agregar filtro abre el desplegable y suma el token", async () => {
    const { save } = mount();
    await screen.findByLabelText("Documento final");
    fireEvent.click(screen.getByRole("button", { name: "Agregar filtro" }));
    fireEvent.change(screen.getByLabelText("Filtrar por"), { target: { value: "estado" } });
    fireEvent.change(screen.getByLabelText("Valor del filtro"), { target: { value: "confirmado" } });
    fireEvent.click(screen.getByRole("button", { name: "Agregar" }));
    await waitFor(() => expect(save).toHaveBeenCalledTimes(1));
    expect(field(save, 0, "resumen_query")).toBe("tipo:hecho estado:confirmado");
  });

  it("una frase abre 'Viene de N átomos' con la ancla y Abrir en Extracción navega", async () => {
    const { go } = mount();
    await screen.findByLabelText("Documento final");
    const doc = screen.getByLabelText("Documento final");
    fireEvent.click(within(doc).getByText("Reunión del 14/09."));
    expect(within(doc).getByText("Viene de 1 átomo")).toBeInTheDocument();
    expect(within(doc).getByText(/Ancla:/)).toBeInTheDocument();
    fireEvent.click(within(doc).getByRole("button", { name: "Abrir en Extracción" }));
    expect(go).toHaveBeenCalledWith("extraccion", "a1");
    fireEvent.click(within(doc).getByRole("button", { name: "Cerrar origen" }));
    expect(within(doc).queryByText("Viene de 1 átomo")).toBeNull();
  });

  it("Origen de una tarjeta lleva a Extracción con el átomo", async () => {
    const { go } = mount();
    await screen.findByLabelText("Documento final");
    fireEvent.click(within(card("Reunión del 14/09")).getByRole("button", { name: "Origen" }));
    expect(go).toHaveBeenCalledWith("extraccion", "a1");
  });

  it("publica: foto v2 con el render real; 409 relee y reintenta una vez", async () => {
    let calls = 0;
    const { createDocument, docs } = mount({
      published: [1],
      resumenQuery: "",
      createImpl: async (model, name, payload, all) => {
        calls += 1;
        if (calls === 1) {
          all.push(pubDoc(2));
          throw new SaveConflictError("ya existe", null);
        }
        all.push({ id: name, model_name: model, path: `docs/${name}.md`, payload });
        return { ok: true, id: name, version: "h" };
      },
    });
    // riesgos_query = tipo:riesgo deja un nuevo: se acepta para liberar el gate.
    await screen.findByLabelText("Documento final");
    fireEvent.click(within(screen.getByRole("navigation", { name: "Esqueleto del documento" })).getByRole("button", { name: /Riesgos/ }));
    fireEvent.click(await within(slotSection()).findByRole("button", { name: "Aceptar" }));
    const btn = await screen.findByRole("button", { name: "Publicar v2" });
    await waitFor(() => expect(btn).toBeEnabled());
    fireEvent.click(btn);
    await screen.findByText("Publicado como v3.");
    expect(createDocument).toHaveBeenCalledTimes(2);
    expect(createDocument.mock.calls[1]![1]).toBe("inf1-v3");
    expect(docs.some((d) => d.id === "inf1-v3")).toBe(true);
  });

  it("un error del servidor al guardar se muestra y no rompe la vista", async () => {
    mount({ saveImpl: async () => ({ ok: false, saved: [], error: "rechazado" }) as SaveResult });
    await screen.findByLabelText("Documento final");
    fireEvent.click(within(within(slotSection()).getAllByRole("listitem")[0]!).getByRole("button", { name: "Aceptar" }));
    expect(await screen.findByRole("alert")).toHaveTextContent("rechazado");
    expect(within(slotSection()).getByText("Nuevo, sin revisar")).toBeInTheDocument();
  });

  it("sin informe: mensaje", async () => {
    mount({ noInforme: true });
    expect(await screen.findByText("El store no tiene ningún informe con slots.")).toBeInTheDocument();
  });

  it("informe con slots propios: títulos, rótulos y 'Agregar filtro' con todos los tipos", async () => {
    mount({
      mutate: (inf) => {
        inf.model_name = "SalidaDoc";
        inf.payload = { title: "Salida de prueba", uno: [], uno_titulo: "Primera sección", uno_rotulo: "Mensaje uno", uno_query: "base:infra distancia:1", uno_modo: "viñetas", uno_pins: [], uno_excluidos: [] };
      },
    });
    expect((await screen.findAllByRole("heading", { name: "Primera sección" })).length).toBe(2);
    expect(screen.getByText("Mensaje uno")).toBeInTheDocument();
    expect(screen.getByText("Base:")).toBeInTheDocument();
    expect(screen.getByText("Distancia:")).toBeInTheDocument();
    fireEvent.click(screen.getByRole("button", { name: "Agregar filtro" }));
    const kinds = within(screen.getByRole("group", { name: "Nuevo filtro" })).getByLabelText("Filtrar por");
    expect(within(kinds).getAllByRole("option").map((o) => o.textContent)).toEqual(["Tipo", "Estado", "Base", "Tag", "Distancia", "Relación"]);
    expect(screen.getByRole("button", { name: "Agregar sección" })).toBeDisabled();
  });
});
