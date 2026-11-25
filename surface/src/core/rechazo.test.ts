/**
 * El traductor de rechazos, contra cuerpos reales: `__fixtures__/rechazos-sldb.json` son las
 * respuestas de un `sldb serve` (pydantic 2.14) a guardados fuera de contrato sobre la wiki de
 * la peluquería de prueba, capturadas sin editar.
 */
import { describe, expect, it } from "vitest";
import capturas from "./__fixtures__/rechazos-sldb.json";
import { erroresDeCampo, leerRechazo } from "./rechazo";

const ROTULOS: Record<string, string> = { duracion_min: "Duración (minutos)", telefono: "Teléfono", atencion: "Atención", lun: "Lunes", categoria: "Categoría", descripcion: "Descripción" };
const rotulo = (clave: string) => ROTULOS[clave] ?? clave.charAt(0).toUpperCase() + clave.slice(1).replace(/_/g, " ");

type Caso = keyof typeof capturas;
const leer = (caso: Caso, ayuda?: (campo: string) => string | undefined) =>
  leerRechazo(capturas[caso].body.error, { status: capturas[caso].status, rotulo, ayuda });
const textos = (caso: Caso) => leer(caso).lineas.map((l) => l.texto);

describe("leerRechazo · cuerpos reales de sldb serve", () => {
  it("campo obligatorio vacío, ausente o nulo", () => {
    expect(textos("obligatorio_vacio")).toEqual(["«Nombre» no puede quedar vacío. Escribe algo y vuelve a guardar."]);
    expect(textos("obligatorio_ausente")).toEqual(["Falta completar «Categoría». Escríbelo y vuelve a guardar."]);
    expect(textos("obligatorio_null")).toEqual(["«Descripción» no puede quedar vacío. Escribe algo y vuelve a guardar."]);
    expect(leer("obligatorio_vacio")).toMatchObject({ reconocido: true, lineas: [{ campo: "nombre" }] });
  });

  it("texto donde va un número, y decimal donde va un entero", () => {
    expect(textos("texto_por_numero")).toEqual(["En «Orden» va un número, sin letras ni símbolos. Escribiste «diez»."]);
    expect(textos("texto_por_numero_rango")).toEqual(["En «Duración (minutos)» va un número, sin letras ni símbolos. Escribiste «una hora»."]);
    expect(textos("decimal_por_entero")).toEqual(["En «Orden» va un número entero, sin decimales. Escribiste 10.5."]);
  });

  it("valor fuera del mínimo y del máximo", () => {
    expect(textos("bajo_minimo")).toEqual(["«Duración (minutos)» no puede ser menor que 5. Escribiste 2."]);
    expect(textos("sobre_maximo")).toEqual(["«Duración (minutos)» no puede ser mayor que 720. Escribiste 5000."]);
  });

  it("opción no permitida: las ramas de una unión se dicen una sola vez", () => {
    expect(textos("opcion_no_permitida_union")).toEqual(["«gratis» no sirve en «Precio»: va un número o «a cotizar»."]);
    expect(leer("opcion_no_permitida_union").lineas[0]!.campo).toBe("precio");
  });

  it("sí o no, y lista", () => {
    expect(textos("texto_por_booleano")).toEqual(["En «Visible» se elige sí o no."]);
    expect(textos("texto_por_lista")).toEqual(["En «Quienes» va una lista: un valor por línea."]);
  });

  it("formato: usa la descripción del campo si el tipo la da", () => {
    expect(textos("patron_telefono")).toEqual(["«Teléfono» no tiene el formato esperado. Escribiste «22 333». Revísalo y vuelve a guardar."]);
    const conAyuda = leer("patron_telefono", (campo) => (campo === "telefono" ? "Teléfono en formato internacional (+569…)." : undefined));
    expect(conAyuda.lineas[0]!.texto).toBe("«Teléfono» no tiene el formato esperado. Escribiste «22 333». Va así: Teléfono en formato internacional (+569…).");
    expect(conAyuda.lineas[0]!.texto).not.toContain("\\d");
  });

  it("varios errores: una línea por campo; los anidados nombran su ruta", () => {
    expect(textos("dos_errores")).toEqual([
      "«Nombre» no puede quedar vacío. Escribe algo y vuelve a guardar.",
      "«Duración (minutos)» no puede ser menor que 5. Escribiste 1.",
    ]);
    expect(textos("crear_faltan_obligatorios")).toHaveLength(5);
    expect(textos("crear_faltan_obligatorios")[0]).toBe("Falta completar «Categoría». Escríbelo y vuelve a guardar.");
    expect(textos("anidado_horario")[0]).toMatch(/^«Atención › Lunes › línea 1» no tiene el formato esperado\. Escribiste «25:00-26:00»\./);
    expect(leer("anidado_horario").lineas[0]!.campo).toBe("atencion");
    expect(textos("anidado_tipo")).toEqual(["En «Horario propio › Lunes» va una lista: un valor por línea."]);
  });

  it("el mensaje de un validador del tipo, que ya viene en español, pasa con el nombre del campo", () => {
    expect(textos("validador_propio")).toEqual([
      '«Atención › Lunes»: el tramo "19:00-10:00" cierra antes de abrir o no dura nada: va como apertura-cierre, por ejemplo "10:00-19:00".',
    ]);
  });

  it("conflicto: otra persona cambió la página", () => {
    for (const caso of ["conflicto", "borrar_conflicto"] as const) {
      const rechazo = leer(caso);
      expect(rechazo.reconocido).toBe(true);
      expect(rechazo.lineas[0]!.texto).toMatch(/^Alguien más cambió esta página mientras la tenías abierta.*Recarga la página/);
    }
  });

  it("nombre ya usado e identificador que no sirve", () => {
    expect(textos("nombre_ya_usado")).toEqual(["Ya hay una página con el nombre «color». Usa otro nombre."]);
    expect(textos("crear_id_invalido")).toEqual(["El nombre de la página solo puede llevar letras, números y guiones. Cámbialo y vuelve a intentar."]);
  });

  it("lo que no reconoce no lo adivina: aviso general y el original intacto", () => {
    for (const caso of ["cambio_de_tipo", "crear_tipo_inexistente"] as const) {
      const rechazo = leer(caso);
      expect(rechazo.reconocido).toBe(false);
      expect(rechazo.lineas[0]!.texto).toBe("No se pudo guardar. Revisa lo que escribiste e inténtalo de nuevo.");
      expect(rechazo.original).toBe(capturas[caso].body.error);
    }
  });

  it("ninguna captura reconocida deja inglés ni jerga de pydantic a la vista", () => {
    for (const caso of Object.keys(capturas) as Caso[]) {
      const rechazo = leer(caso);
      expect(rechazo.original).toBe(capturas[caso].body.error);
      for (const linea of rechazo.lineas) {
        expect(linea.texto, caso).not.toMatch(/validation error|Input should|\[type=|pydantic|input_value|SLDB/);
      }
    }
  });
});

describe("leerRechazo · otras formas", () => {
  it("los mensajes que sldb ya escribe en español pasan sin tocar", () => {
    const propio = "Ya hay una página llamada «ana» en la wiki. Usa otro nombre.";
    expect(leerRechazo(propio, { status: 409 })).toEqual({ lineas: [{ texto: propio, campo: null }], reconocido: true, original: propio });
  });

  it("un tipo de error que no conoce nombra el campo y deja el original como detalle", () => {
    const raro = "x: 1 validation error for ServicioDoc\nprecio\n  Algo nuevo de pydantic [type=tipo_nuevo, input_value=1, input_type=int]";
    const rechazo = leerRechazo(raro, { status: 422, rotulo });
    expect(rechazo.reconocido).toBe(false);
    expect(rechazo.lineas).toEqual([{ texto: "«Precio» tiene un valor que no se acepta. Revísalo y vuelve a guardar.", campo: "precio" }]);
  });

  it("opciones de un enumerado, mínimo de letras y máximo de letras", () => {
    const de = (cuerpo: string) => leerRechazo(`x: 1 validation error for M\n${cuerpo}`, { rotulo }).lineas[0]!.texto;
    expect(de("atiende\n  Input should be 'asistente', 'por_tomar' or 'persona' [type=literal_error, input_value='nadie', input_type=str]")).toBe(
      "«nadie» no es una opción de «Atiende». Elige entre «asistente», «por_tomar» o «persona».",
    );
    expect(de("nombre\n  String should have at most 40 characters [type=string_too_long, input_value='aaaa', input_type=str]")).toBe(
      "«Nombre» es muy largo: caben hasta 40 letras. Acórtalo.",
    );
    expect(de("clave\n  String should have at least 16 characters [type=string_too_short, input_value='abc', input_type=str]")).toBe(
      "«Clave» es muy corto: necesita al menos 16 letras.",
    );
  });

  it("sin `[type=…]` (texto recortado) reconoce el error por su frase", () => {
    expect(leerRechazo("servicio: 1 validation error for ServicioDoc\nnombre\n  Field required", { rotulo }).lineas[0]!.texto).toBe(
      "Falta completar «Nombre». Escríbelo y vuelve a guardar.",
    );
  });

  it("un fallo del servidor o de la red se dice como tal, con el original de detalle", () => {
    expect(leerRechazo("SLDB respondió 500", { status: 500 })).toMatchObject({ reconocido: false, lineas: [{ texto: expect.stringMatching(/problema del sistema/) }] });
    expect(leerRechazo("Failed to fetch")).toMatchObject({ reconocido: false, lineas: [{ texto: expect.stringMatching(/No hay conexión/) }] });
  });

  it("erroresDeCampo no inventa: un texto que no es de pydantic no tiene campos", () => {
    expect(erroresDeCampo("corte cambió en SLDB. Recarga para evitar sobrescribirlo.")).toBeNull();
  });
});
