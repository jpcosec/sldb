/**
 * El rechazo de SLDB a un guardado, dicho en español para quien edita la wiki.
 *
 * Es presentación, no validación: aquí no se decide si un valor sirve. Se lee lo que SLDB ya
 * respondió y se dice en palabras qué pasó y qué hacer. `sldb serve` entrega `{ok: false, error}`
 * con un texto; cuando el contrato del tipo rechaza un valor (422), ese texto es el de pydantic:
 *
 *     corte: 1 validation error for ServicioDoc
 *     duracion_min
 *       Input should be greater than or equal to 5 [type=greater_than_equal, input_value=2, input_type=int]
 *         For further information visit https://errors.pydantic.dev/…
 *
 * Lo que no se reconoce no se adivina: va un aviso general y el texto original queda a la vista.
 */

export interface LineaRechazo {
  texto: string;
  /** El field al que se refiere (su raíz en el payload), si el rechazo nombra uno. */
  campo: string | null;
}

export interface Rechazo {
  lineas: LineaRechazo[];
  /** `false` cuando alguna parte no se pudo decir en español: ahí el original se muestra como detalle. */
  reconocido: boolean;
  /** El texto de SLDB, sin tocar. */
  original: string;
}

export interface OpcionesRechazo {
  /** Código HTTP de la respuesta, si la hubo. */
  status?: number;
  /** El nombre de un field para una persona (`duracion_min` → «Duración (minutos)»). */
  rotulo?: (clave: string) => string;
  /** La descripción que el tipo da de un field (su raíz), para explicar un formato. */
  ayuda?: (campo: string) => string | undefined;
}

interface ErrorDeCampo {
  loc: string[];
  msg: string;
  type: string | null;
  input: string | null;
}

const CABECERA = /^(?:.*?: )?\d+ validation errors? for [A-Za-z_][\w.]*\s*$/;
const DETALLE = /^(.*?)\s*\[type=([a-z_]+), input_value=([\s\S]*), input_type=[\w.]+\]$/;
/** Las ramas de una unión que pydantic agrega a la ruta (`precio.int`, `precio.literal['a cotizar']`). */
const RAMA = /^(int|str|float|bool|bytes|date|datetime|time|timedelta|decimal|none|(literal|list|dict|set|tuple|nullable|function-[a-z]+|is-instance|lax-or-strict|constrained-[a-z]+)\[.*\])$/;

const NUMERO = new Set(["int_parsing", "int_type", "float_parsing", "float_type", "decimal_parsing", "decimal_type", "int_parsing_size"]);
const ENTERO = new Set(["int_from_float"]);
const SI_NO = new Set(["bool_parsing", "bool_type"]);
const OPCION = new Set(["literal_error", "enum"]);
const FECHA = /^(date|datetime|time)_(parsing|type|from_date_parsing)$/;

/** Los mensajes que ya llegan en español claro (los escribe minegocio delante de SLDB). */
const YA_CLAROS = [
  /^Ya hay una página llamada /,
  /^Este negocio ya tiene su página /,
  /^Falta la clave del equipo/,
  /^No se pudo llegar al servidor de la wiki/,
];

function segmentos(loc: string): string[] {
  return loc.match(/[^.[\]]+(?:\[[^\]]*\])?/g) ?? [];
}

/** El texto de pydantic, en errores por campo; `null` si el texto no tiene esa forma. */
export function erroresDeCampo(message: string): ErrorDeCampo[] | null {
  const lineas = message.split("\n");
  if (!CABECERA.test(lineas[0] ?? "")) return null;
  const errores: { loc: string; msg: string | null }[] = [];
  for (const linea of lineas.slice(1)) {
    if (!linea.trim() || /^\s+For further information visit /.test(linea)) continue;
    const ultimo = errores[errores.length - 1];
    if (/^\S/.test(linea)) errores.push({ loc: linea.trim(), msg: null });
    else if (ultimo && ultimo.msg === null) ultimo.msg = linea.trim();
    else if (/^ {2}\S/.test(linea) || !ultimo) errores.push({ loc: "", msg: linea.trim() }); // error del documento entero
    else ultimo.msg = `${ultimo.msg}\n${linea.trim()}`;
  }
  return errores.map(({ loc, msg }) => {
    const detalle = DETALLE.exec(msg ?? "");
    return {
      loc: segmentos(loc),
      msg: (detalle?.[1] ?? msg ?? "").trim(),
      type: detalle?.[2] ?? tipoPorTexto(msg ?? ""),
      input: detalle?.[3] ?? null,
    };
  });
}

/** El tipo de error de pydantic cuando el texto llega sin su `[type=…]`. */
function tipoPorTexto(msg: string): string | null {
  const tabla: [RegExp, string][] = [
    [/^Field required/, "missing"],
    [/should have at least \d+ character/, "string_too_short"],
    [/should have at most \d+ character/, "string_too_long"],
    [/greater than or equal to/, "greater_than_equal"],
    [/less than or equal to/, "less_than_equal"],
    [/should be greater than/, "greater_than"],
    [/should be less than/, "less_than"],
    [/valid integer, got a number with a fractional part/, "int_from_float"],
    [/valid (integer|number)/, "int_parsing"],
    [/valid boolean/, "bool_parsing"],
    [/valid string/, "string_type"],
    [/valid list/, "list_type"],
    [/should match pattern/, "string_pattern_mismatch"],
    [/^Value error, /, "value_error"],
  ];
  return tabla.find(([patron]) => patron.test(msg))?.[1] ?? null;
}

/** `'diez'` → «diez»; `2` → 2; `None` y lo que pydantic recorta no se muestran. */
function escrito(input: string | null): string | null {
  if (input === null || input === "None" || input.includes("...")) return null;
  const texto = /^(['"])([\s\S]*)\1$/.exec(input);
  if (texto) return texto[2] ? `«${texto[2]}»` : null;
  return /^-?\d+(\.\d+)?$/.test(input) ? input : null;
}

const conLoEscrito = (frase: string, input: string | null) => {
  const valor = escrito(input);
  return valor ? `${frase} Escribiste ${valor}.` : frase;
};

function opcionesDe(msg: string): string[] {
  return Array.from(msg.matchAll(/'((?:[^'\\]|\\.)*)'/g), (m) => m[1]!);
}

const lista = (items: string[], final: string) =>
  items.length > 1 ? `${items.slice(0, -1).join(", ")} ${final} ${items[items.length - 1]}` : (items[0] ?? "");

const limite = (msg: string) => /(-?\d+(?:\.\d+)?)\s*(?:characters?|items?)?\s*$/.exec(msg)?.[1] ?? null;

/** Lo que una rama de una unión acepta, en palabras; `null` si no se sabe decir. */
function loQueAcepta(error: ErrorDeCampo): string | null {
  if (error.type && (NUMERO.has(error.type) || ENTERO.has(error.type))) return "un número";
  if (error.type && OPCION.has(error.type)) return lista(opcionesDe(error.msg).map((o) => `«${o}»`), "o") || null;
  if (error.type && SI_NO.has(error.type)) return "sí o no";
  if (error.type === "string_type") return "un texto";
  return null;
}

function frase(error: ErrorDeCampo, campo: string, ayuda: string | undefined): string | null {
  const { type, msg, input } = error;
  const n = limite(msg);
  if (type === "missing") return `Falta completar ${campo}. Escríbelo y vuelve a guardar.`;
  if (type === "string_too_short") {
    return n === "1" || n === null
      ? `${campo} no puede quedar vacío. Escribe algo y vuelve a guardar.`
      : `${campo} es muy corto: necesita al menos ${n} letras.`;
  }
  if (type === "string_too_long") return n ? `${campo} es muy largo: caben hasta ${n} letras. Acórtalo.` : `${campo} es muy largo. Acórtalo.`;
  if (type === "string_type") return input === "None" ? `${campo} no puede quedar vacío. Escribe algo y vuelve a guardar.` : `En ${campo} va un texto.`;
  if (type && NUMERO.has(type)) return conLoEscrito(`En ${campo} va un número, sin letras ni símbolos.`, input);
  if (type && ENTERO.has(type)) return conLoEscrito(`En ${campo} va un número entero, sin decimales.`, input);
  if (type === "greater_than_equal" && n) return conLoEscrito(`${campo} no puede ser menor que ${n}.`, input);
  if (type === "greater_than" && n) return conLoEscrito(`${campo} tiene que ser mayor que ${n}.`, input);
  if (type === "less_than_equal" && n) return conLoEscrito(`${campo} no puede ser mayor que ${n}.`, input);
  if (type === "less_than" && n) return conLoEscrito(`${campo} tiene que ser menor que ${n}.`, input);
  if (type && OPCION.has(type)) {
    const opciones = opcionesDe(msg).map((o) => `«${o}»`);
    const valor = escrito(input);
    if (!opciones.length) return null;
    return `${valor ?? "Ese valor"} no es una opción de ${campo}. Elige ${opciones.length > 1 ? "entre " : ""}${lista(opciones, "o")}.`;
  }
  if (type && SI_NO.has(type)) return `En ${campo} se elige sí o no.`;
  if (type === "list_type") return `En ${campo} va una lista: un valor por línea.`;
  if (type && FECHA.test(type)) return conLoEscrito(`En ${campo} va una fecha u hora válida.`, input);
  if (type === "string_pattern_mismatch") {
    return [conLoEscrito(`${campo} no tiene el formato esperado.`, input), ayuda ? `Va así: ${ayuda}` : "Revísalo y vuelve a guardar."].join(" ");
  }
  if (type === "value_error") {
    const propio = msg.replace(/^Value error, /, "").trim();
    return propio ? `${campo}: ${propio}${/[.!?]$/.test(propio) ? "" : "."}` : null;
  }
  return null;
}

function lineasDeCampos(errores: ErrorDeCampo[], opciones: OpcionesRechazo): { lineas: LineaRechazo[]; reconocido: boolean } {
  const rotulo = opciones.rotulo ?? ((clave: string) => clave);
  const grupos = new Map<string, { ruta: string[]; errores: ErrorDeCampo[] }>();
  for (const error of errores) {
    const ruta = [...error.loc];
    while (ruta.length > 1 && RAMA.test(ruta[ruta.length - 1]!)) ruta.pop();
    const clave = ruta.join(".");
    const grupo = grupos.get(clave) ?? { ruta, errores: [] };
    grupo.errores.push(error);
    grupos.set(clave, grupo);
  }
  const lineas: LineaRechazo[] = [];
  let reconocido = true;
  for (const { ruta, errores: delCampo } of grupos.values()) {
    const raiz = ruta[0] ?? null;
    const campo = raiz
      ? `«${ruta.map((s) => (/^\d+$/.test(s) ? `línea ${Number(s) + 1}` : rotulo(s))).join(" › ")}»`
      : "La página";
    const ayuda = raiz ? opciones.ayuda?.(raiz) : undefined;
    let texto: string | null;
    if (delCampo.length > 1) {
      // Una unión (un número o «a cotizar»): pydantic da un error por rama; se dice una sola vez qué va.
      const acepta = delCampo.map(loQueAcepta);
      const valor = escrito(delCampo[0]!.input);
      texto = acepta.every((a): a is string => a !== null)
        ? `${valor ?? "Ese valor"} no sirve en ${campo}: va ${lista(Array.from(new Set(acepta)), "o")}.`
        : null;
    } else {
      texto = frase(delCampo[0]!, campo, ayuda);
    }
    if (texto === null) {
      reconocido = false;
      texto = `${campo} tiene un valor que no se acepta. Revísalo y vuelve a guardar.`;
    }
    lineas.push({ texto, campo: raiz });
  }
  return { lineas, reconocido };
}

const una = (texto: string, reconocido = true): Omit<Rechazo, "original"> => ({ lineas: [{ texto, campo: null }], reconocido });

function sinCampos(message: string, status: number | undefined): Omit<Rechazo, "original"> {
  if (YA_CLAROS.some((patron) => patron.test(message))) return una(message);
  if (/ cambió en SLDB\b/.test(message)) {
    return una(
      "Alguien más cambió esta página mientras la tenías abierta, así que no se guardó lo que hiciste. Recarga la página para ver cómo quedó e inténtalo de nuevo.",
    );
  }
  const usado =
    /^Ya existe el documento (.+?)\.?$/.exec(message) ??
    /^El archivo de (.+?) ya existe/.exec(message) ??
    /^Doc '(.+?)' already tracked/.exec(message);
  if (usado) return una(`Ya hay una página con el nombre «${usado[1]}». Usa otro nombre.`);
  if (/^El ID nuevo solo admite/.test(message)) {
    return una("El nombre de la página solo puede llevar letras, números y guiones. Cámbialo y vuelve a intentar.");
  }
  if (status !== undefined && status >= 500) {
    return una("No se pudo guardar por un problema del sistema; no cambió nada. Inténtalo de nuevo en un momento y, si sigue, avisa a quien te da soporte.", false);
  }
  if (status === undefined && /failed to fetch|networkerror|load failed/i.test(message)) {
    return una("No hay conexión con el servidor, así que no se guardó. Revisa tu internet e inténtalo de nuevo.", false);
  }
  return una("No se pudo guardar. Revisa lo que escribiste e inténtalo de nuevo.", false);
}

/** El rechazo de un guardado, en líneas en español; el texto de SLDB queda en `original`. */
export function leerRechazo(message: string, opciones: OpcionesRechazo = {}): Rechazo {
  const errores = erroresDeCampo(message);
  const leido = errores?.length ? lineasDeCampos(errores, opciones) : sinCampos(message, opciones.status);
  return { ...leido, original: message };
}
