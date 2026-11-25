## REFORMULACION

Propósito: obtener de JP la decisión 6 —(a) extraer `sldb/src/sldb/store/` a un paquete propio o (b) conservar el desacople interno ya hecho en `beb8a99c`— y dejarla registrada. Resultado: sección de decisión en `docs/architecture/store-extraction-proposal.md` con fecha ISO y motivo; `desk/STANDARDS.md:19` sin declararla pendiente; recibo `owner` aceptado por JP; si (a), tarea de refactor creada con contrato completo; commit del coordinador. Repo: `/mnt/ssd/proyectos/SLDB_1`. Límites: no mover código, no hacer push, no cerrar sin recibo aceptado; la recomendación (b) es insumo, no decisión por defecto. Nodo no ejecutable por agente: es una puerta humana con preparación documental.

## AMBIGUEDADES

1. Mecanismo de edición de STANDARDS.md. El TaskDoc dice: «desk/STANDARDS.md no es un documento modelado por deskops (no está en el store), así que se edita en el mismo commit»; la pill dice: «desk/STANDARDS.md está trackeado en el store de sldb y su regla 4 dice que se edita con sldb fields update»; STANDARDS.md:4 dice: «Los documentos que modela este desk (SPEC.md, STANDARDS.md) se editan con sldb fields update». Obliga a inventar cuál mecanismo usar y si hay edición manual.
2. Título exacto de la sección: el TaskDoc pide «## <nombre de la sección>» y «sección "Decisión 6"»; la pill exige «exactamente '## Decisión 6'». Obliga a fijar el literal.
3. Manejo de silencio o rechazo de JP: solo se prevé «(a)… o (b)». Obliga a inventar timeout, tercera opción o bloqueo.
4. «vía la CLI que corresponda»: no nombra el comando si STANDARDS.md sí está modelado. Obliga a elegir entre `sldb fields update` y edición en commit.

## DRY-RUN

Lecturas: `docs/architecture/store-extraction-proposal.md`, `desk/STANDARDS.md`, `tests/test_store_seams.py`, `contracts/layers.toml`, historial de `beb8a99c`. Cambios previstos: preguntar a JP por herdr/supervisor copiando opciones, costos y recomendación; registrar recibo con `deskops review record ... --kind owner`; escribir la sección; actualizar la línea de STANDARDS.md; si (a), `deskops add task`; `deskops closeout commit`. Dependencias: respuesta y `dispose accepted` de JP, CLI deskops, árbol limpio. Validaciones futuras: `grep -n 'Decisión 6'`, `TMPDIR=/dev/shm pytest -q tests/test_store_seams.py`, `deskops closeout verify`.

## FUTURO

JP elige y acepta el recibo; el coordinador redacta y commitea; el integrador hace push. Si (a), otro nodo ejecuta el refactor.
