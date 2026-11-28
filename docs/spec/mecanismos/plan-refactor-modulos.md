# Refactor de sldb hacia módulos: plan y primer despacho

## Contexto

El refactor por anillos ya está en `main` (PR #5, `19327c799`): puertas de dirección entre
anillos y de tamaño, con la deuda escrita en `contracts/anillos_deuda.toml` (138 imports y 3
funciones largas) y la regla de que solo puede achicarse.

Después se definió qué es kernel (JP, 2026-11-27): lo que si falta, sldb deja de ser sldb, en
módulos con frontera; y se midió con dos criterios, quién importa a quién y qué no debería
cambiar. Resultado en `docs/spec/mecanismos/modulos.md` y `reparto-completo.md`:

- kernel que ya está en su lugar: Puertos, Grafo, errores y hallazgos;
- kernel a media altura porque depende de los modelos: Árboles, Anclaje, Proyección, Consulta;
- el centro equivocado de hoy: la base de los modelos;
- tres piezas sostienen 78 de los 138 imports de deuda: abrir un store (48), validar (18) y
  ubicar un store (12);
- la interfaz con git no existe: son doce llamadas sueltas.

Este plan dice cómo seguir, partiendo de la maquinaria que ya funciona y sin romperla.

## Cómo funciona hoy, y lo que eso obliga

Leído en el código el 2026-11-28.

| Hecho | Consecuencia para el plan |
|---|---|
| Un eje es una lista de rutas en `contracts/layers.toml`; una ruta puede ser un archivo suelto. | Muchos "movimientos" se hacen en el contrato, sin mover el archivo ni cambiar su ruta de import. |
| El orden de anillos está en `RINGS` de `tools/check_axes.py:42`. Un import viola si va a un anillo de más afuera. | Cambiar el orden es cambiar la puerta: va con su test. |
| La deuda se compara por clave `archivo` + `módulo`. Mover un archivo deja una entrada "vencida" y crea una "nueva". | La lista se edita a mano en cada paso. No se regenera entera. |
| Las unidades llevan `needs` y `needed_by` escritos a mano, y la puerta los comprueba. | Se actualizan en cada paso. |
| El refactor fusionado no dejó alias: cada movimiento fue un rename más actualizar a quien importa. | Se sigue igual dentro de sldb. |
| deskops entra a `sldb.runtime.validation` 73 veces y a `store.io` 18; specIR y graph_ui usan `sldb.api`, `mcp` y `cli.serve`. `tools/check_surface.py` lo compara con `contracts/identity.toml [surface]`. El CI de graph_ui sigue a `main` de sldb. | Ninguna ruta que use otro repo se mueve ni se borra en esta etapa. |
| `tools/check_claims.py` falla si un documento nombra una ruta que ya no existe. | Al mover un archivo se corrigen los documentos que lo nombran. |
| Unos 103 tests importan `sldb.store.<módulo>` por ruta. | Mover un archivo de `store/` obliga a tocar tests. Se evita mientras se pueda. |
| Un archivo declarado en dos ejes no se detecta: gana el último. Caso real: `store/runtime_cache.py`. | Es un hoyo de la puerta. Se cierra primero. |
| El CI corre `bash tools/check.sh --fast`, la suite entera y el build, en Python 3.12 y 3.13. La suite local tarda unos 21 minutos. | La suite entera se corre una vez al principio y una al final. |

## Tres etapas

Solo la primera se despacha ahora.

### Etapa 1: lo mecánico, sin cambiar los anillos (se despacha)

Meta: bajar la deuda de 138 a cerca de 60, crear el primer módulo del kernel que no existe
(Puertos, por git) y cerrar un hoyo de la puerta. No cambia `RINGS`, no mueve rutas que usen
otros repos.

Un worktree nuevo desde `main`, rama `refactor/modulos-1`. Un commit por paso. Sin push ni merge.

**Paso 0. Línea base.** `bash tools/check.sh --fast` y la suite entera con `--basetemp` en un
directorio de `mktemp -d` que se borra al final. Anotar los fallos previos (se conocen dos: un
test de símbolos de TypeScript, y tres de `tests/test_document_segments.py` que dependen del
orden de import del deskops vecino).

**Paso 1. Cerrar el hoyo de la puerta.**
- En `tools/check_axes.py`, puerta por defecto: error si un archivo calza en las rutas de dos
  ejes. Mensaje en el estilo de los existentes.
- Test nuevo en `tests/test_check_axes_anillos.py`, con árbol falso, igual que los que hay.
- Arreglar el caso real: `store/runtime_cache.py` queda en un solo eje (`cache`).

**Paso 2. Puertos: la interfaz con git.**
- Paquete nuevo `src/sldb/ports/`, con `git.py`: una función que corre git y las pocas
  operaciones con nombre que hoy se usan (leer un archivo en un commit, listar archivos,
  historia de una ruta, rama actual, raíz del repo, leer y escribir configuración, mover,
  consultar si algo está ignorado).
- Declararlo: una capa en `[[layers]]` de `contracts/layers.toml` (nivel más bajo, sin
  dependencias), su clasificación en `contracts/identity.toml`, un `[[axis]] id="puertos"
  ring="0a"`, y su unidad.
- Reemplazar las llamadas sueltas, una por una, sin cambiar comportamiento:
  `store/package_version.py`, `store/diagnostics_models/text_history.py`,
  `api/documents/document_history.py`, `relocate_file.py`, `move_path_files.py`,
  `api/stores/derived_recovery.py`, `branch_stores.py`, `ensure_merge_driver.py`,
  `merge_driver_install.py`, `gitignore_policy.py`, y en `cli/`: `commands/stores_build_check.py`
  y `bench/meta.py`.
- Puerta nueva en `tools/check_axes.py`: una llamada a `subprocess` cuyo comando empieza con
  `git`, fuera del eje `puertos`, es error. Con su lista de deuda si alguna no se alcanza a
  mover, con la misma regla de que solo se achica. Engancharla en `tools/check.sh`.
- Tests de la puerta en `tests/test_check_axes_anillos.py`, y tests del puerto en
  `tests/ports/` que usen un repo git temporal.
- No son git y no se tocan: `api/stores/apply_findings.py` (corre un comando del usuario) y los
  procesos de `cli/bench`.

**Paso 3. Abrir y ubicar un store bajan al centro.**
- `api/stores/store_location.py` solo importa pydantic: se declara en el eje `persistencia`
  (anillo 0b) en `contracts/layers.toml`, sin mover el archivo. Caen 12 entradas de deuda.
- `api/stores/open_store.py`: hoy importa `store.migration` (anillo 2) y
  `api.stores.store_discovery`. Para declararlo en 0b hay que cortar esos dos imports sin
  cambiar lo que hace `open_store(store, mode)` para quien lo llama. Si `store_discovery` y lo
  que usa de `migration` son lectura pura del disco, se declaran también en 0b. Si migrar
  escribe, no se fuerza: se deja `open_store` donde está y se anota, porque es una decisión de
  diseño.
- La ruta de import no cambia, así que ni los tests ni los otros repos se enteran.
- Sacar a mano de `contracts/anillos_deuda.toml` las entradas que desaparecen, y actualizar
  `needs` y `needed_by` de las unidades.

**Paso 4. Partir la validación.**
- `runtime/validation.py` tiene dos funciones que solo usan plantilla y texto,
  `extract_payload` y `render_markdown`, y cinco que reciben la clase del modelo.
- Las dos primeras pasan a un archivo del eje `render` (anillo 0a), en `core/`.
- `sldb.runtime.validation` las sigue exportando con el mismo nombre, porque deskops entra por
  ahí. Es la única reexportación de la etapa y queda declarada en `identity.toml [surface]`.
- Dentro de sldb, quien solo usa esas dos (mirar `models/structured_doc.py` y
  `store/runtime_codec.py`) pasa a importarlas de su lugar nuevo. Si con eso se cierra la
  reparación pendiente R3, se mueve de `[[pending]]` a `[[done]]`.
- Las cinco que reciben el modelo no se tocan: quién las llama desde el centro es la etapa 3.

**Paso 5. Cierre.** La suite entera una vez, contra la línea base. `bash tools/check.sh` completo
(incluye afirmaciones de documentos y selfdoc). Informe.

**Reglas para el agente.**
- No se vale: import perezoso dentro de una función, `importlib`, una reexportación para
  esconder un import (salvo la declarada del paso 4), cambiar el anillo de un eje para que pase,
  ni regenerar la deuda con `--write-debt`.
- Nunca `git add -A`: se agregan archivos por nombre. No usar `git stash`.
- Si un corte exige una decisión de diseño, no se hace: se anota.
- No se borran los archivos sin usuarios (`api/edges/edges_blocked.py`, `api/graph/traverse.py`,
  `api/schema/field_description.py`): se reexportan en `sldb.api` y pueden ser API pública.

### Etapa 2: el contrato pasa a hablar de módulos (planeada, no se despacha)

- Redibujar los ejes para que cada eje sea un módulo de `modulos.md`. Los ejes que ya lo son se
  quedan (`vistas`, `enlaces`, `vocabulario_visual`, `indice_de_aristas`, `semantica`,
  `persistencia`, `errores`). Los que son mezcla se parten listando rutas: `grafo` en tres
  (consulta, almacén del grafo, análisis), `codigo` en tres, y el bloque operación en los
  módulos que salieron del reparto (documentos, modelos, código de un modelo, lotes, relaciones,
  grafo de proyecto, administración del store).
- Insumo: los 512 archivos que Jev ubicó con seguridad (`reparto-completo.json`). Los dudosos
  van a un eje con nombre explícito de "por ubicar", para que se vean.
- Cambiar `RINGS` al orden del kernel: Puertos y errores; Grafo; Consulta y Árboles; Anclaje;
  Proyección; Sostén y Acción; librerías; caras.
- Como cambia la vara, la deuda se vuelve a medir una vez. Es la única excepción a "solo se
  achica", y se entrega con la cuenta de antes y la de después y la explicación de cada
  diferencia.
- Puerta nueva: una librería no importa a otra librería salvo que esté declarado.
- Necesita antes una revisión de JP del reparto, porque fija los nombres de los módulos.

### Etapa 3: invertir la dependencia de los modelos (sin planear)

Hoy Árboles, Anclaje y Proyección importan a los modelos de documento. Para que sean kernel
tienen que dejar de hacerlo: leer una fuente sin modelo. Es diseño, no mecánica, y es la pieza
más grande. Se planea cuando las etapas 1 y 2 muestren cuánto queda.

## Cómo se reparte el trabajo

- Etapa 1: un solo agente, en su propio worktree. Los cinco pasos tocan
  `contracts/layers.toml`, `contracts/anillos_deuda.toml` y `tools/check_axes.py`, así que van en
  serie, en el orden escrito.
- Yo reviso sus commits y el informe antes de proponer el PR. El PR entra por squash, como el
  anterior.

## Archivos críticos

- `contracts/layers.toml`, `contracts/anillos_deuda.toml`, `contracts/identity.toml`
- `tools/check_axes.py`, `tools/check.sh`
- `tests/test_check_axes_anillos.py`, `tests/test_store_seams.py`
- `src/sldb/ports/git.py` (nuevo)
- `src/sldb/api/stores/open_store.py`, `store_location.py`, `store_discovery.py`
- `src/sldb/runtime/validation.py`

## Verificación

- `bash tools/check.sh` completo pasa.
- `python tools/check_axes.py --rings` pasa y la lista de deuda bajó; se informa de 138 a
  cuánto, y qué entradas salieron por cada paso.
- La suite entera da lo mismo que la línea base, o mejor.
- `grep` de `subprocess` con `git` en `src/sldb` solo encuentra `ports/git.py`, o lo que quedó
  en la lista de deuda nueva.
- `python tools/check_surface.py` pasa: nada de lo que usan deskops, specIR y graph_ui cambió de
  ruta.
- `git diff --stat main` no muestra archivos renombrados fuera de los previstos.
