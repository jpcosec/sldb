# Resultado (intento 2)

Defecto: un nombre solo del store se detectaba como conocido pero se validaba con load_notation/load_palette (solo builtin/archivo) → falso '-invalid'.

Cambio (commit 8d487dd8): src/sldb/cli/commands/notations_validate.py, tests/notations/test_notations_validate_cli.py.
- Detección en el store con api.select_documents; el documento se resuelve con select_documents(ref, model, expect="one") (fila con path).
- **Desvío del encargo**: no se valida "ese archivo por ruta con load_notation/load_palette": el archivo del store es markdown con front matter (load_palette falla con "expected a single document") y una NotationDoc solo guarda refs (los glifos/links son otros documentos), así que no es un NotationSpec. En su lugar: load_runtime_documents (el modelo del store valida el documento) y, para paletas, el payload sin "id" se reconstruye como PaletteSpec y pasa check_palette (contraste incluido). El error lleva la ruta del store.
- Un documento inválido del store ya no da exit 2: es un finding error, exit 1.
- Tests nuevos: notación y paleta solo en store (exit 0, sin --store exit 2), paleta del store con contraste insuficiente (exit 1), notación del store inválida (exit 1).

Validación: ver validation.log (15 tests pasan; check.sh --fast solo falla 'identidad' por workbench_demo, autorizado).
Sin cambios de CLI/flags: selfdoc y CHANGELOG sin cambios nuevos.
