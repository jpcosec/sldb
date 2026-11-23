/**
 * Subir una imagen del negocio para mostrarla dentro de un texto.
 *
 * La superficie no guarda archivos: se los entrega a quien la sirve (`POST <url>?nombre=…`, el archivo en el cuerpo)
 * y recibe la ruta con que el texto la nombra (`imagenes/el-salon-1a2b3c4d.jpg`). Qué imagen se acepta lo decide ese
 * servidor; su rechazo se muestra tal cual.
 */
export type SubirImagen = (archivo: File) => Promise<string>;

type Pedir = (url: string, init: RequestInit) => Promise<Response>;

export function crearSubidaDeImagenes(url: string, pedir: Pedir = (u, init) => fetch(u, init)): SubirImagen {
  return async (archivo) => {
    const respuesta = await pedir(`${url}?nombre=${encodeURIComponent(archivo.name)}`, { method: "POST", body: archivo });
    const cuerpo = (await respuesta.json().catch(() => null)) as { ruta?: string; error?: string } | null;
    if (!respuesta.ok || !cuerpo?.ruta) throw new Error(cuerpo?.error ?? "No se pudo subir la imagen. Inténtalo de nuevo.");
    return cuerpo.ruta;
  };
}

/** El Markdown que muestra una imagen: lo que se ve si no carga es el nombre del archivo, sin la extensión. */
export function markdownDeImagen(ruta: string, nombreDelArchivo: string): string {
  const texto = nombreDelArchivo.replace(/\.[^.]+$/, "").replace(/[[\]_-]+/g, " ").trim() || "imagen";
  return `![${texto}](${ruta})`;
}

/** El texto con la imagen agregada en un párrafo propio, donde estaba el cursor (o al final). */
export function conImagen(texto: string, imagen: string, cursor: number = texto.length): string {
  const antes = texto.slice(0, cursor).trimEnd();
  const despues = texto.slice(cursor).trimStart();
  return [antes, imagen, despues].filter(Boolean).join("\n\n");
}
