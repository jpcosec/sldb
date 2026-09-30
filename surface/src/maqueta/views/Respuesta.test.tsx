import { describe, expect, it, vi } from "vitest";
import { fireEvent, render, screen, within } from "@testing-library/react";
import { SaveConflictError } from "../../core/client";
import type { Atom, Fuente, Informe, InformeSlotEntry, Respuesta as RespuestaDoc } from "../../core/contract";
import type { AtomStore } from "../../views/atoms/useAtomStore";
import type { ViewProps } from "../ViewProps";
import Respuesta from "./Respuesta";

const atom = (id: string, over: Partial<Atom> = {}): Atom => ({
  id,
  gid: `AtomDoc:${id}`,
  path: `docs/atoms/${id}.md`,
  kind: "criterio",
  status: "confirmado",
  source: id.startsWith("p") ? "FuenteDoc:prompt" : "FuenteDoc:folleto",
  source_field: "body",
  start: 0,
  end: 1,
  tags: [id.startsWith("p") ? "programa.asistente" : "paciente.situacion"],
  text: `texto de ${id}`,
  quote: "q",
  conf: 1,
  ...over,
});
const P = (id: string) => `docs/atoms/${id}.md`;
const fuente = (id: string, tipo: string, body = ""): Fuente => ({ id, gid: `FuenteDoc:${id}`, path: `docs/${id}.md`, title: id, tipo, base: "", descripcion: "", body });
const slot = (over: Partial<InformeSlotEntry> = {}): InformeSlotEntry => ({ name: "respuesta", titulo: "Respuesta al paciente", rotulo: "", atomos: [], query: "", pins: [], excluidos: [], modo: "prosa", ...over });
const informe = (s: InformeSlotEntry[]): Informe => ({ id: "s", path: "docs/s.md", modelName: "SalidaDoc", slots: {} as never, slotList: s, payload: {} }) as Informe;

const ATOMS = [atom("p5"), atom("p7"), atom("p2"), atom("f3", { tags: ["programa.receta"] }), atom("f5", { tags: ["programa.red"] })];
const RESP: RespuestaDoc = {
  id: "r1",
  path: "docs/r1.md",
  title: "Respuesta al paciente",
  caso: "caso-1",
  estado: "borrador",
  generadaPor: "modelo (borrador de demostración)",
  slot: "respuesta",
  mensaje: "msg",
  respuesta: "",
  frases: [
    { texto: "Ofrezco teleconsulta.", atomos: ["p5", "f3"] },
    { texto: "Centro en Pucón.", atomos: ["f5"] },
    { texto: "¿Algo más?", atomos: ["p7"] },
  ],
};
const CON_FANTASMA: RespuestaDoc = { ...RESP, frases: [...RESP.frases, { texto: "Dato viejo.", atomos: ["zz"] }] };

function mount(over: { respuesta?: RespuestaDoc | undefined; informe?: Informe; saveField?: () => Promise<unknown>; atoms?: Atom[] } = {}) {
  const saveField = vi.fn(over.saveField ?? (async () => ({ ok: true })));
  const go = vi.fn();
  const store = { atoms: over.atoms ?? ATOMS, grupos: [{ tag: "programa", title: "Programa" }, { tag: "paciente", title: "Paciente" }], edges: [], saveField, reload: vi.fn() } as unknown as AtomStore;
  const props: ViewProps = {
    store,
    acta: {} as never,
    fuentes: [fuente("prompt", "prompt"), fuente("msg", "mensaje", "Hola, soy Carolina.\n\n¿Dónde renuevo la receta?")],
    informe: over.informe ?? informe([slot({ atomos: [P("p5"), P("p7"), P("p2"), P("f3"), P("f5")] })]),
    respuesta: "respuesta" in over ? over.respuesta : RESP,
    caso: null,
    focusId: null,
    setFocusId: () => {},
    go,
  };
  render(<Respuesta {...props} />);
  return { saveField, go };
}

describe("Respuesta", () => {
  it("muestra el mensaje, la respuesta, la nota y los átomos por base", () => {
    mount();
    expect(screen.getByText("Hola, soy Carolina.")).toBeTruthy();
    expect(screen.getByText("Ofrezco teleconsulta.")).toBeTruthy();
    expect(screen.getByText(/Redactada por modelo \(borrador de demostración\) desde el slot “Respuesta al paciente”/)).toBeTruthy();
    expect(screen.getByText("Borrador, todavía no se envía.")).toBeTruthy();
    expect(screen.getByText(/Base Programa/).textContent).toContain("(5)");
    expect(screen.getAllByText("frase 1").length).toBeGreaterThan(0);
  });
  it("una referencia sin átomo se muestra como átomo no encontrado y deja la frase stale", () => {
    mount({ respuesta: CON_FANTASMA });
    expect(screen.getByText(/1 frase depende/)).toBeTruthy();
    expect(screen.getByText(/átomo no encontrado/).textContent).toContain("zz");
  });
  it("hover de una frase y de un átomo se resaltan mutuamente", () => {
    mount();
    fireEvent.mouseEnter(screen.getByText("Centro en Pucón."));
    const li = screen.getByText("texto de f5").closest("li")!;
    expect(li.style.opacity).toBe("1");
    expect(screen.getByText("texto de f3").closest("li")!.style.opacity).toBe("0.35");
    fireEvent.mouseLeave(screen.getByText("Centro en Pucón."));
    fireEvent.mouseEnter(screen.getByText("texto de f3").closest("li")!);
    expect((screen.getByText("Ofrezco teleconsulta.") as HTMLElement).style.opacity).toBe("1");
    expect((screen.getByText("Centro en Pucón.") as HTMLElement).style.opacity).toBe("0.35");
  });
  it("verificaciones: solo p5 y p7 con ✓; el resto sin ✓ y marcado", () => {
    mount();
    const list = screen.getByText("Reglas del system prompt").nextElementSibling as HTMLElement;
    const items = within(list).getAllByRole("listitem");
    expect(items).toHaveLength(3);
    expect(list.textContent!.match(/✓/g)).toHaveLength(2);
    expect(within(list).getAllByText("sin verificación automática")).toHaveLength(1);
    expect(list.textContent).toContain("texto de p2");
  });
  it("Enviar guarda estado enviada cuando no hay pendientes", async () => {
    const { saveField } = mount();
    expect(screen.getByText("Nada pendiente.")).toBeTruthy();
    fireEvent.click(screen.getByRole("button", { name: "Enviar al paciente" }));
    await Promise.resolve();
    expect(saveField).toHaveBeenCalledWith("r1", "estado", "enviada");
  });
  it("Enviar queda deshabilitado con átomos nuevos", () => {
    mount({ informe: informe([slot({ query: "tag:programa", atomos: [P("p5"), P("p7"), P("f3")], excluidos: [P("f5")] })]) });
    const btn = screen.getByRole("button", { name: "Enviar al paciente" }) as HTMLButtonElement;
    expect(btn.disabled).toBe(true);
    expect(screen.getByText(/átomo(s)? nuevo(s)? sin revisar en el Compositor/)).toBeTruthy();
    expect(btn.title).toContain("nuevo");
  });
  it("frase stale si un átomo salió del slot", () => {
    mount({ informe: informe([slot({ atomos: [P("p5"), P("p7"), P("p2"), P("f5")] })]) });
    expect(screen.getByText(/1 frase depende de átomos que ya no están/)).toBeTruthy();
    expect((screen.getByRole("button", { name: "Enviar al paciente" }) as HTMLButtonElement).disabled).toBe(true);
  });
  it("estado enviada", () => {
    mount({ respuesta: { ...RESP, estado: "enviada" } });
    expect(screen.getByText(/Enviada \(marcada en el store; no hay canal de entrega conectado\)/)).toBeTruthy();
    expect((screen.getByRole("button", { name: "Enviada" }) as HTMLButtonElement).disabled).toBe(true);
  });
  it("error de guardado visible", async () => {
    mount({ saveField: async () => { throw new SaveConflictError("conflicto", {}); } });
    fireEvent.click(screen.getByRole("button", { name: "Enviar al paciente" }));
    expect((await screen.findByRole("alert")).textContent).toContain("cambió en SLDB");
  });
  it("Editar en el Compositor y Origen navegan", () => {
    const { go } = mount();
    fireEvent.click(screen.getByText("Editar en el Compositor"));
    expect(go).toHaveBeenCalledWith("compositor");
    fireEvent.click(within(screen.getByText("texto de f3").closest("li")!).getByText("Origen"));
    expect(go).toHaveBeenCalledWith("extraccion", "f3");
  });
  it("sin respuesta: mensaje de estado; slot inexistente: aviso y sin enviar", () => {
    mount({ respuesta: undefined });
    expect(document.querySelector(".mq-state")).toBeTruthy();
  });
  it("slot inexistente avisa y deshabilita", () => {
    mount({ informe: informe([slot({ name: "otro" })]) });
    expect(screen.getByText(/no tiene el slot “respuesta”/)).toBeTruthy();
    expect((screen.getByRole("button", { name: "Enviar al paciente" }) as HTMLButtonElement).disabled).toBe(true);
  });
});
