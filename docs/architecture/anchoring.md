# Anclaje

Documento de autoridad de sldb sobre qué es anclar, sus vías, sus reglas y la distinción entre
error y alerta. Las reglas de las secciones 3 y 4 son decisiones del dueño y no se rediscuten;
el diseño técnico que las implementa está en [code-anchoring.md](code-anchoring.md).

## 1. Definición

**Anclar es fundamentar una afirmación en su fuente**: «esto lo digo porque está dicho allá».
Un anclaje une lo que se afirma con el lugar exacto que lo respalda, y **guarda lo que vio**
de esa fuente. Por eso detecta mutaciones: cuando la fuente cambia, lo guardado y lo actual
dejan de coincidir, y el anclaje lo sabe.

Un anclaje que solo resuelve (encuentra a qué apunta) sin guardar lo que vio no verifica nada:
puede decir dónde está su fuente, pero no si sigue diciendo lo mismo.

Esta es la definición de sldb. El `AnchorDoc` de pron la usa con otro sentido, el de **alias**:
una palabra del léxico y lo que nombra (`pron.models:AnchorDoc`). Un alias resuelve; no
fundamenta ni guarda lo que vio.

## 2. Las dos vías

1. **AnchorDoc**: un documento cuyo `ref` apunta a algo del store (un modelo, un campo, un
   documento, una relación; sldb lo resuelve en `src/sldb/store/edge_index/anchor_targets.py`).
   Hoy resuelve, pero no verifica: no guarda lo que vio.
2. **Código, con tree-sitter**: un anclaje a un símbolo de código, `code:<ruta>::<qualified_name>`,
   resuelto por nombre y no por línea, que guarda un fingerprint de cada nodo que vio. Todavía
   no existe; su diseño está en [code-anchoring.md](code-anchoring.md).

## 3. Reglas del anclaje (decisión del dueño, 2026-10-19)

1. **Docstring y cuerpo son nodos distintos.** El anclaje guarda un fingerprint de cada uno por
   separado: el texto normalizado del nodo, no el hash del archivo. Los dos cuentan como
   mutación, pero el anclaje distingue cuál cambió: la docstring, el cuerpo o ambos (y la
   firma, si conviene).
2. **`changed` no es un error, es una alerta** (sección 4). La fuente se movió respecto de lo
   anclado; el estado es válido, pero hay que mirarlo.
3. **Una referencia rota se intenta reconectar.** Si el símbolo ya no está en su
   `qualified_name`, se busca dónde quedó, con la heurística de renombre de selfdoc adaptada
   a los fingerprints por nodo. Si se encuentra, se reporta «reconnected: de X a Y» y queda
   registrado; si no, se reporta «lost». Los dos casos son alertas explícitas, nunca
   silenciosas.

## 4. Error y alerta, en todo sldb (decisión del dueño, 2026-10-19)

- Un **error** es algo roto o que viola un contrato: no parsea, el store está corrupto, un
  documento es inválido, falta un archivo requerido, un modelo no importa.
- Una **alerta** es que la fuente se movió respecto de lo registrado: un anclaje cambió, un
  hash quedó atrás, un documento generado está viejo. El estado es válido, pero hay que
  mirarlo.

Reglas de salida:
- Una alerta no hace fallar el comando: si solo hay alertas, el exit code es 0.
- Una alerta **jamás es silenciosa**. Aparece en la salida de texto; con `--envelope`, en
  `warnings`; en el CI, como annotation; y en el resumen final, con su conteo.
- Un error sí hace fallar el comando.

La regla vale para todo sldb, no solo para los anclajes. Hoy varios comandos tratan un
movimiento de fuente como error (por ejemplo, `stores check` da FAIL por un hash atrasado).
La auditoría de cada caso y su reclasificación propuesta están en
[code-anchoring.md, sección 10](code-anchoring.md).
