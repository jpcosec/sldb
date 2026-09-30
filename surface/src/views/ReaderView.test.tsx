import { describe, expect, it, vi } from "vitest";
import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import type { SldbClient } from "../core/client";
import { SldbHttpError } from "../core/client";
import type { SchemaModel } from "../core/contract";
import { SldbProvider } from "../react/context";
import { ReaderView } from "./ReaderView";

/** El contrato real del store: `pron.models:AnchorDoc`. */
const anchorDoc: SchemaModel = {
  id: "AnchorDoc",
  model_ref: "pron.models:AnchorDoc",
  fields: [
    { name: "symbol", kind: "string", required: true },
    { name: "forms", kind: "stringlist", required: false },
    { name: "ref", kind: "string", required: true },
    { name: "steps", kind: "list", required: false },
    { name: "motive", kind: "string", required: true },
  ],
};

const TEXT = "el cliente manifiesta que no será\nposible una conexión directa a SAP.";

function mount() {
  const save = vi.fn(async () => ({ ok: true, saved: ["anchor-no-sera-posible-una"] }));
  const client = { schema: async () => ({ models: [anchorDoc], errors: [] }), save } as unknown as SldbClient;
  render(
    <SldbProvider client={client}>
      <ReaderView />
    </SldbProvider>,
  );
  return { save };
}

/** Pega texto y selecciona un tramo, como lo haría el usuario en el textarea. */
function selectRange(textarea: HTMLTextAreaElement, start: number, end: number) {
  fireEvent.change(textarea, { target: { value: TEXT } });
  textarea.setSelectionRange(start, end);
  fireEvent.select(textarea);
  return textarea;
}

describe("ReaderView", () => {
  it("arma el formulario desde el schema y solo muestra campos declarados", async () => {
    mount();
    const textarea = (await screen.findByLabelText("Texto crudo")) as HTMLTextAreaElement;
    selectRange(textarea, 0, 2);
    expect(await screen.findByText(/línea 1/)).toBeInTheDocument();
    expect(screen.getByRole("textbox", { name: /^symbol/ })).toBeInTheDocument();
    expect(screen.getByRole("textbox", { name: /^ref/ })).toBeInTheDocument();
    expect(screen.getByRole("textbox", { name: /^motive/ })).toBeInTheDocument();
    // `provenance` no lo declara este modelo: no hay campo para él.
    expect(screen.queryByRole("textbox", { name: /provenance/ })).toBeNull();
  });

  it("dice que la sugerencia de duplicados no está disponible", async () => {
    mount();
    expect(await screen.findByText(/no disponible/i)).toBeInTheDocument();
  });

  it("guarda con POST /save y enlaza al documento creado", async () => {
    const { save } = mount();
    const textarea = (await screen.findByLabelText("Texto crudo")) as HTMLTextAreaElement;
    fireEvent.change(textarea, { target: { value: TEXT } });
    textarea.setSelectionRange(3, 46);
    fireEvent.select(textarea);

    fireEvent.change(screen.getByRole("textbox", { name: /^ref/ }), { target: { value: "(model DomainAtom)" } });
    fireEvent.change(screen.getByRole("textbox", { name: /^motive/ }), { target: { value: "el cliente no quiere conexión directa" } });
    fireEvent.click(screen.getByRole("button", { name: "Guardar anchor" }));

    await waitFor(() => expect(save).toHaveBeenCalledTimes(1));
    expect(save).toHaveBeenCalledWith([
      {
        id: "anchor-cliente-manifiesta-que-no",
        action: "create",
        model: "AnchorDoc",
        payload: {
          symbol: "cliente-manifiesta-que-no",
          ref: "(model DomainAtom)",
          motive: "el cliente no quiere conexión directa",
        },
      },
    ]);
    const link = await screen.findByRole("link", { name: "Abrir documento" });
    expect(link).toHaveAttribute("href", "#/doc/anchor-cliente-manifiesta-que-no");
    // El tramo anclado queda marcado en el texto.
    expect(document.querySelectorAll("mark.reader-mark").length).toBe(1);
  });

  it("muestra el mensaje del backend tal cual", async () => {
    const client = {
      schema: async () => ({ models: [anchorDoc], errors: [] }),
      save: async () => {
        throw new SldbHttpError("AnchorDoc: ref inválido.", 422, { error: "AnchorDoc: ref inválido." });
      },
    } as unknown as SldbClient;
    render(
      <SldbProvider client={client}>
        <ReaderView />
      </SldbProvider>,
    );
    const textarea = (await screen.findByLabelText("Texto crudo")) as HTMLTextAreaElement;
    fireEvent.change(textarea, { target: { value: TEXT } });
    textarea.setSelectionRange(0, 10);
    fireEvent.select(textarea);
    fireEvent.change(screen.getByRole("textbox", { name: /^ref/ }), { target: { value: "x" } });
    fireEvent.change(screen.getByRole("textbox", { name: /^motive/ }), { target: { value: "y" } });
    fireEvent.click(screen.getByRole("button", { name: "Guardar anchor" }));
    expect(await screen.findByText("AnchorDoc: ref inválido.")).toBeInTheDocument();
  });
});
