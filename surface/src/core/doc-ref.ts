/**
 * Cómo la superficie nombra una página ante `sldb serve`.
 *
 * El nombre de una página es único dentro de su tipo, no en el store: puede haber un
 * `ServicioDoc` y un `ProfesionalDoc` llamados `corte`. SLDB resuelve una referencia por nombre,
 * por ruta o por `Tipo/nombre`, y rechaza el nombre solo cuando es ambiguo. Aquí la referencia
 * de una página es su nombre mientras sea único entre los documentos del store, y `Tipo/nombre`
 * cuando hay otra página con ese nombre en otro tipo. No se decide nada sobre el contenido: solo
 * se elige la forma de la referencia con lo que `/graph` ya entrega (`id` y `model_name`).
 */

export interface DocKey {
  id: string;
  model_name: string;
}

const MODELO = /^[A-Za-z_][A-Za-z0-9_]*$/;

/** `Tipo/nombre`: la forma que SLDB pide para una página cuyo nombre se repite. */
export const qualifiedRef = (model: string, name: string) => `${model}/${name}`;

/** Las partes de una referencia: `Tipo/nombre` o `Tipo:nombre` traen el tipo; un nombre solo, no. */
export function parseRef(ref: string): { model: string | null; name: string } {
  const cut = /^([^/:]+)[/:](.+)$/.exec(ref.trim());
  if (cut && MODELO.test(cut[1]!)) return { model: cut[1]!, name: cut[2]! };
  return { model: null, name: ref.trim() };
}

export const sameDocument = (a: DocKey, b: DocKey) => a.id === b.id && a.model_name === b.model_name;

/** La referencia de la página `name` del tipo `model`: calificada solo si el nombre se repite en otro tipo. */
export function refFor(documents: DocKey[], name: string, model?: string | null): string {
  return model && documents.some((d) => d.id === name && d.model_name !== model) ? qualifiedRef(model, name) : name;
}

/** La referencia con que se abre, se guarda y se quita un documento del store. */
export const docRef = (doc: DocKey, documents: DocKey[]) => refFor(documents, doc.id, doc.model_name);

/**
 * El documento que nombra una referencia. Con tipo, el de ese tipo si existe; si no, el que se
 * llame así (si el nombre se repite, el primero: una referencia vieja sin tipo sigue abriendo
 * una página). También se acepta la ruta con que el store lo sigue.
 */
export function findDocument<T extends DocKey & { path?: string }>(documents: T[], ref: string): T | undefined {
  const { model, name } = parseRef(ref);
  if (model) {
    const typed = documents.find((d) => d.id === name && d.model_name === model);
    if (typed) return typed;
  }
  return documents.find((d) => d.id === ref) ?? documents.find((d) => d.path === ref) ?? documents.find((d) => d.id === name);
}

/** Una referencia cualquiera (de un enlace, de la dirección) en su forma canónica; si no nombra un documento conocido, tal cual. */
export function canonicalRef(documents: DocKey[], ref: string): string {
  const found = findDocument(documents, ref);
  return found ? docRef(found, documents) : ref;
}
