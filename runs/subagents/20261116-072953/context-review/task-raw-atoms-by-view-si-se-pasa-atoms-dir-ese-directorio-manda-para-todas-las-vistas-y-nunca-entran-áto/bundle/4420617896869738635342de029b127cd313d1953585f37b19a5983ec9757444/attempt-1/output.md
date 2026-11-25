## REFORMULACION

Encargo ejecutable único (`task.code`, nodo `ritual-execution`), no agregado.

**Propósito:** que `raw_atoms_by_view` (src/sldb/api/matching/atoms_by_view.py) use exclusivamente `parse_atoms(atoms_dir, findings)` para todas las vistas cuando `atoms_dir` es truthy, sin consultar el store de ninguna vista; sin `atoms_dir`, comportamiento actual.

**Resultado:** rama de `atoms_dir` reescrita, docstring actualizada, test nuevo en tests/matching/test_matching_refs.py (dos vistas: una con store con átomos y otra sin store, más `atoms_dir` con un átomo distinto; con `atoms_dir` ambas traen solo el del directorio; sin `atoms_dir`, la del store trae los suyos), línea en CHANGELOG.md.

**Repo:** sldb. **Límites:** no cambiar el descubrimiento del store sin `atoms_dir`; commit y push fuera del ejecutor (coordinador); validación `TMPDIR=/dev/shm pytest -q tests/matching/`; informe en `runs/subagents/<run-dir>/result-summary.md`; aviso a IR.

## AMBIGUEDADES

1. «sin llamar reader.atoms» y «no consulta ningún store» no precisan si `reader.findings` sigue anexándose al retorno: obligaría a inventar si el findings del reader se conserva o se vacía con `atoms_dir`.
2. «más un atoms_dir con un átomo distinto»: no fija forma del payload, id, tags ni alias esperados; obligaría a inventar el contenido del átomo y sus aserciones.
3. «bajo el encabezado "## 0.1.13 — not released yet"»: si a HEAD no existiera, no dice si crearlo ni con qué versión; obligaría a inventar versión/estructura.
4. «con las fixtures o helpers que ya usa el archivo de test nombrado»: el archivo no muestra un helper directo para un store con átomos y otro sin; obligaría a inventar la construcción vía `sldb.api`.

## DRY-RUN

**Lecturas:** atoms_by_view.py, tests/matching/test_matching_refs.py, grep de `raw_atoms_by_view`/`build_atoms_by_view` en src y tests, CHANGELOG.md, inbox de origen.
**Cambios previstos:** sustituir el dict por `reader.atoms(view.store)` cuando haya `atoms_dir` por asignación de `json.loads(parse_atoms(atoms_dir, findings))` a todas las claves; docstring; test nuevo; entrada CHANGELOG.
**Dependencias:** `parse_atoms`, `SpecView`, `StoreReader`, fixtures del test. **Validaciones futuras:** pytest tests/matching/ con `TMPDIR=/dev/shm`, suite completa si aplica, closeout y aviso a IR.

## FUTURO

Commit y push: coordinador con `deskops closeout commit`. Aviso a IR: `deskops message send --to IR` o línea en result-summary.md si no registrado. Cierre/verify y limpieza del Board: closeout.
