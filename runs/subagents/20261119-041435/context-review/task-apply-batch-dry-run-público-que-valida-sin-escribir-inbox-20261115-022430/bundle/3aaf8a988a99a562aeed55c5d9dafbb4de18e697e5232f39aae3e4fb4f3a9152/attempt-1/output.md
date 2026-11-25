## REFORMULACION
Nodo ejecutable (`task.code`), no agregado. **Propósito:** hacer público un modo `dry_run` en `apply_batch` para que el MCP de specIR valide una propuesta sin escribir. **Resultado:** `apply_batch(store, changes, dry_run=True)` ejecuta la prevalidación existente —forma, modelo, round-trip, guardas y destinos— y devuelve informe o errores, sin transacción ni escritura; el store y el proyecto quedan byte a byte idénticos. **Repo:** `SLDB_1/sldb`; superficies: `src/sldb/api/documents/apply_batch.py`, `batch_prevalidate.py`, `batch_guards.py`, `src/sldb/api/__init__.py`, `src/sldb/mcp/write/tools.py`, tests, `docs/architecture/mcp.md` y `CHANGELOG`. **Límites:** `apply_batches` no cambia; `dry_run=False` por defecto; cobertura de lote válido e inválido; commit con rutas y `Task-Id`; cierre de la nota del inbox.

## AMBIGUEDADES
1. “devuelve un BatchReport con saved vacío y applied=False (o el campo que se agregue, documentado)” — el contrato público no está fijado; obligaría a inventar campos y semántica del informe.
2. “suite de a un archivo, tools/check.sh y stores build --check” — no coincide con la sección Validation y “stores build --check” no está definido; obligaría a inventar el comando o el alcance del gate.
3. “si propose_changes reimplementa la prevalidación... si ya usa prevalidate_changes, dejarlo y decirlo” — exige inspección del MCP; el input no fija su estado y obligaría a inventar si se modifica.
4. “Cerrar la nota del inbox al terminar” — no indica archivo ni verbo de cierre; obligaría a inventar el mecanismo.
5. “las mismas guardas” — no enumera cuáles; obligaría a inventar el conjunto exacto si `batch_guards.py` no basta.

## DRY-RUN
Un ejecutor leería Board, TaskDoc, rituales, `apply_batch.py`, `batch_prevalidate.py`, `batch_guards.py`, `api/__init__.py`, `propose_changes`, tests y docs. Añadiría `dry_run=False` a `apply_batch`, llamaría `prevalidate_changes` bajo el cerrojo y retornaría antes de abrir transacción; exportaría lo necesario; agregaría tests de no escritura y mismo error; actualizaría docstring, `mcp.md` si aplica y `CHANGELOG`; condicionalmente adaptaría `propose_changes`. Depende de `BatchReport`, prevalidación, guardas, `apply_batches`, `tools/check.sh`, deskops e inbox. Validaría `pytest tests/api`, `tests/mcp`, `check.sh --fast`, `stores build --check` y closeout verify.

## FUTURO
Otro nodo/MCP decide migrar `propose_changes`; deskops cierra la nota del inbox; un humano fija el contrato público de `BatchReport` si no se documenta; closeout verifica tests, commit y árbol limpio.
