# T6 · Ruido estructural: bloquear al registrar

Estado: **HECHO** · Worktree: `hum-ecosystem-worktrees/sldb-noise`
Rama: `feat/structural-noise-detection`
Commit: `9450ada` — "noise: rechazar ruido estructural al registrar, con error visible"
Request: `sldb/docs/requests/structural-noise-detection.md`

## Reescrita

La versión anterior de esta tarea decía "fuga de estructura en documentos
compuestos" y proponía componer fields en vez de documentos enteros. **Estaba mal
planteada**: el síntoma que se veía al componer era consecuencia de otra cosa.

## Tesis

SLDB desarma texto en proposiciones, sin ruido de estructura ni gramática: es el
paso previo a un grafo de conocimiento. **Un `#` en medio de un field es una
declaración que falta en el modelo**, no prosa.

## El caso

`domain-cobranza-spec` está trackeado como `DomainAtom`, cuyo template declara dos
headings. El documento tiene siete: dentro de `answer` hay cinco más
(`## Entidades`, `## Herramientas trazadas`, `## Medición 1`, `## Medición 2`,
`## Consultas de verificación`).

Verificado: el documento **no está roto**. Extrae bien, `render == disco` byte a
byte, abre en la superficie. Lo que pierde es `owning_section` en sus 9 fields.

Esos cinco headings son campos que el modelo no declara. `## Entidades` es una
lista de refs a otros atoms — información que SLDB maneja como grafo, y que quedó
como markdown suelto porque el modelo no tenía dónde ponerla.

Origen: se escribió el Markdown a mano, salteándose el CLI.

## Decisión

**Bloquea.** `docs track` y `docs create` rechazan el documento con un error que
nombra los headings y manda a crear un modelo que herede del actual y los declare
`optrev`.

`stores check` reporta los que ya entraron (diagnóstico, no bloqueo).

Romper stores existentes es deseado: no se rompe algo que venía bueno, se saca a
la luz un caso de error que estaba tapado.

## Lo que NO se hace

Volver tolerante el mapeo de `cli/graph_ops/map_fields.py` (emparejar por título,
mapear el prefijo). Sería tapar el síntoma: ese `warning` está haciendo bien su
trabajo, solo avisa tarde y suave.

## Por qué la herencia es la salida

- Los modelos heredan como pydantic normal (manual §8); el store guarda `base_models`
- `optrev` ya cubre campos declarados que pueden no estar
- **El heading ya nombra la clave**: el mapeo a diccionario sale solo

## Relación con T3

El ruido estructural es la señal principal de la vista SALUD. La vista cubre los
documentos que entraron antes de que el bloqueo exista.

## Resultado
`docs track` y `docs create` BLOQUEAN con un `SLDBValidationError` que nombra cada
heading sobrante; `stores check` reporta sin bloquear. Suite: 1081 passed en su momento.

Verificado contra `domain-cobranza-spec` (5 headings sin declarar).
