/**
 * La referencia de una página ante `sldb serve`: el nombre mientras sea único en el store,
 * `Tipo/nombre` cuando otra página de otro tipo se llama igual (la forma que SLDB pide entonces).
 */
import { describe, expect, it, vi } from "vitest";
import { createHttpClient } from "./client";
import { canonicalRef, docRef, findDocument, parseRef, qualifiedRef, refFor } from "./doc-ref";

const docs = [
  { id: "documento", model_name: "DocumentoDoc", path: "documento.md" },
  { id: "color", model_name: "ServicioDoc", path: "servicios/color.md" },
  { id: "corte", model_name: "ServicioDoc", path: "servicios/corte.md" },
  { id: "ana", model_name: "ProfesionalDoc", path: "equipo/ana.md" },
  { id: "corte", model_name: "ProfesionalDoc", path: "equipo/corte.md" },
];

describe("doc-ref", () => {
  it("un nombre único viaja solo; uno repetido, con su tipo delante", () => {
    expect(docs.map((d) => docRef(d, docs))).toEqual(["documento", "color", "ServicioDoc/corte", "ana", "ProfesionalDoc/corte"]);
    expect(refFor(docs, "color", "ServicioDoc")).toBe("color");
    expect(refFor(docs, "corte", "ProfesionalDoc")).toBe("ProfesionalDoc/corte");
    expect(refFor(docs, "corte")).toBe("corte"); // sin tipo no hay cómo calificar
    expect(refFor(docs, "nueva", "ServicioDoc")).toBe("nueva");
    expect(qualifiedRef("ServicioDoc", "corte")).toBe("ServicioDoc/corte");
  });

  it("lee `Tipo/nombre`, `Tipo:nombre` y el nombre solo", () => {
    expect(parseRef("ServicioDoc/corte")).toEqual({ model: "ServicioDoc", name: "corte" });
    expect(parseRef("ServicioDoc:corte")).toEqual({ model: "ServicioDoc", name: "corte" });
    expect(parseRef("corte")).toEqual({ model: null, name: "corte" });
  });

  it("encuentra el documento del tipo nombrado y no su homónimo", () => {
    expect(findDocument(docs, "ProfesionalDoc/corte")?.path).toBe("equipo/corte.md");
    expect(findDocument(docs, "ServicioDoc:corte")?.path).toBe("servicios/corte.md");
    expect(findDocument(docs, "equipo/corte.md")?.model_name).toBe("ProfesionalDoc"); // por su ruta
    expect(findDocument(docs, "corte")?.model_name).toBe("ServicioDoc"); // sin tipo: el primero
    expect(findDocument(docs, "fantasma")).toBeUndefined();
  });

  it("deja cualquier referencia en su forma canónica", () => {
    expect(canonicalRef(docs, "ServicioDoc/color")).toBe("color"); // único: sin tipo, como lo abre SLDB hoy
    expect(canonicalRef(docs, "ServicioDoc:color")).toBe("color");
    expect(canonicalRef(docs, "ProfesionalDoc:corte")).toBe("ProfesionalDoc/corte");
    expect(canonicalRef(docs, "ServicioDoc/corte")).toBe("ServicioDoc/corte");
    expect(canonicalRef(docs, "ServicioDoc/fantasma")).toBe("ServicioDoc/fantasma"); // desconocida: tal cual
  });
});

describe("cliente HTTP · la referencia calificada viaja entera", () => {
  it("en lecturas va en la query (con la barra escapada) y en /save como `id`", async () => {
    const fetchImpl = vi.fn(async (_url: string, _init?: RequestInit) => new Response(JSON.stringify({ ok: true, markdown: "" }), { status: 200 }));
    const client = createHttpClient("/api/wiki", fetchImpl);
    await client.segments("ProfesionalDoc/corte");
    await client.document("ProfesionalDoc/corte");
    await client.render("ProfesionalDoc/corte");
    await client.save([{ id: "ProfesionalDoc/corte", action: "delete", model: "ProfesionalDoc", expected: {} }]);
    expect(fetchImpl.mock.calls.slice(0, 3).map((c) => c[0])).toEqual([
      "/api/wiki/document/segments?id=ProfesionalDoc%2Fcorte",
      "/api/wiki/document?id=ProfesionalDoc%2Fcorte",
      "/api/wiki/render?doc=ProfesionalDoc%2Fcorte",
    ]);
    expect(JSON.parse(String(fetchImpl.mock.calls[3]![1]!.body)).changes[0].id).toBe("ProfesionalDoc/corte");
  });
});
