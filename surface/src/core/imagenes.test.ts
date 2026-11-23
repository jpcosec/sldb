import { describe, expect, it } from "vitest";
import { conImagen, crearSubidaDeImagenes, markdownDeImagen } from "./imagenes";

const archivo = new File([new Uint8Array([1, 2, 3])], "El salón_nuevo.JPG", { type: "image/jpeg" });

describe("subir una imagen", () => {
  it("entrega el archivo con su nombre y devuelve la ruta con que el texto la nombra", async () => {
    const pedidos: [string, RequestInit][] = [];
    const subir = crearSubidaDeImagenes("/panel/wiki/imagenes", async (url, init) => {
      pedidos.push([url, init]);
      return new Response(JSON.stringify({ ruta: "imagenes/el-salon-nuevo-1a2b3c4d.jpg" }));
    });
    expect(await subir(archivo)).toBe("imagenes/el-salon-nuevo-1a2b3c4d.jpg");
    expect(pedidos[0]![0]).toBe("/panel/wiki/imagenes?nombre=El%20sal%C3%B3n_nuevo.JPG");
    expect(pedidos[0]![1].method).toBe("POST");
    expect(pedidos[0]![1].body).toBe(archivo);
  });

  it("muestra el rechazo del servidor tal cual", async () => {
    const subir = crearSubidaDeImagenes("/x", async () => new Response(JSON.stringify({ error: "El archivo no es una imagen JPG, PNG, WebP ni GIF." }), { status: 422 }));
    await expect(subir(archivo)).rejects.toThrow("El archivo no es una imagen JPG, PNG, WebP ni GIF.");
  });
});

describe("la imagen dentro del texto", () => {
  it("se nombra por lo que dice el archivo", () => {
    expect(markdownDeImagen("imagenes/a-1.jpg", "El salón_nuevo.JPG")).toBe("![El salón nuevo](imagenes/a-1.jpg)");
  });

  it("queda en un párrafo propio, donde estaba el cursor o al final", () => {
    expect(conImagen("Uno.\n\nDos.", "![a](imagenes/a.jpg)")).toBe("Uno.\n\nDos.\n\n![a](imagenes/a.jpg)");
    expect(conImagen("Uno.\n\nDos.", "![a](imagenes/a.jpg)", 4)).toBe("Uno.\n\n![a](imagenes/a.jpg)\n\nDos.");
    expect(conImagen("", "![a](imagenes/a.jpg)")).toBe("![a](imagenes/a.jpg)");
  });
});
