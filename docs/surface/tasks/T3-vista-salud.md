# T3 · Vista SALUD

Estado: **HECHO** · Dificultad: baja · Depende de: T1
Worktree: `/home/jp/proyectos/hum-ecosystem-worktrees/sldb-surface/surface`

## Qué
Vista de lectura sobre datos que ya existen: lint, ciclos, nodos aislados,
divergencias (`stores check`) y ruido estructural (headings sin declarar en el modelo).

Propuesta §6.5.

## Corrección de la premisa
El enunciado original decía que no existen endpoints de salud y que había que derivar
todo en el cliente. Es falso. SLDB sí sirve `GET /lint`, `GET /graph/cycles` y
`GET /graph/isolated`: los tres responden 200 contra el backend y están declarados en
`src/sldb/cli/serve/routes.py`. `graph_ui` ya los consumía desde antes. La
vista `#/salud` los consume tal cual y solo deriva lo que no está servido.

En `knowledge_antonia-cobranza`:

- `/lint`: 0 problemas.
- `/graph/cycles`: 1 ciclo, `step-cobranza-respuesta → step-cobranza-reenviar`.
- `/graph/isolated`: 3 documentos aislados — `complete-systemprompt`,
  `fallback-cobranza`, `self-antonia-cobranza` (se omiten los nodos de tipo field:
  un campo declarado que nadie referencia todavía es normal).

## Derivado en el cliente

### Ruido estructural (hallazgo principal)
Un heading dentro del valor de un field es una sección que el modelo no declara. No es corrupción del documento: `domain-cobranza-spec` (DomainAtom, template de 2 headings, 7 en el render) extrae, renderiza byte a byte y abre en la superficie; lo que pierde es `owning_section` en sus 9 fields. Es un contrato incompleto; la salida es un modelo que herede del actual y declare esas secciones como campos `optrev`.

Se deriva del contenido de `/document/segments` (200), no de un error: el backend solo loguea el warning `Cannot map template fields` y devuelve el mapa de `owning_section` vacío.

En `knowledge_antonia-cobranza` la detección real es: `domain-cobranza-spec` → 5 secciones (Entidades, Herramientas trazadas, Medición 1, Medición 2, Consultas de verificación) y `domain-cobranza-multiples-facturas` → 1 (Domain Ref).

### Documentos no canónicos
`canonical:false` sale de sondear `/document/segments`: el archivo en disco no coincide
con el render del payload.

### Modelos que no cargan
`/schema.errors` informa `{model, error}`; la vista muestra el mensaje crudo, sin causa
estructurada (template vs import vs dependencia).

## Brecha abierta

- **Divergencias (`stores check`)**: sigue sin endpoint HTTP. No se pueden listar las divergencias entre modelo y archivo en disco; de eso solo se deriva `canonical:false` sondeando `/document/segments`.
- **`/graph` no expone estado de salud por documento**: para saber si un documento tiene ruido estructural hay que sondear `/document/segments` documento por documento (N+1). Falta un endpoint de lote del tipo `/health` o `/documents/health`.
- **No hay señal directa de `owning_section` perdida**: el backend loguea el warning pero responde 200 sin exponer ni el conteo de headings del template ni los del render. La superficie infiere el ruido contando headings dentro de valores de field.
- **`/document/segments` no distingue** por sí solo "no se pudo leer" de un documento sano sin ruido: la vista separa explícitamente los documentos sin lectura para no presentarlos como ruido estructural.
