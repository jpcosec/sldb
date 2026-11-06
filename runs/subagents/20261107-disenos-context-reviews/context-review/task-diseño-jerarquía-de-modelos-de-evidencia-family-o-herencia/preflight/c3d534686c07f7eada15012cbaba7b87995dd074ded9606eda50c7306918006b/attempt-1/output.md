## REFORMULACION
No es un agregado: es un encargo documental (`task.docs`) ejecutable por un redactor. **Propósito:** comparar `__family__` frente a herencia de clases para modelos de evidencia y exponer consecuencias para deskops. **Resultado:** un único documento en `docs/architecture/evidence-model-family.md`, trackeado en `.sldb/store.yaml` como `ArchitectureNarrativeDoc` con nombre `arch-evidence-model-family`, con las seis secciones de e5, recomendación y sección “Decisión del dueño” con `PENDIENTE: decide el dueño`. **Repo:** desk/sldb, con store `.sldb`. **Límites:** solo documento; sin cambios de código ni modelos en sldb o deskops; no crear `ProofDoc`; no decidir la política de cierre ni la jerarquía.

## AMBIGUEDADES
1. “con el modelo ArchitectureNarrativeDoc (docs.models:ArchitectureNarrativeDoc, como los otros docs/architecture)”: no se da el esquema/frontmatter exigido; obligaría a inventar campos, id, tags y metadatos.
2. “El documento existe, está trackeado y tiene la decisión del dueño anotada.” frente a “PENDIENTE: decide el dueño”: no queda claro si “anotada” admite el pendiente o exige una decisión real; obligaría a inventar el criterio de cierre.
3. “híbrido si aplica”: no define cuándo aplica ni si es obligatorio; obligaría a inventar el criterio.
4. “el hueco de la nota 8bd79409 … esta tratado en consecuencias”: “tratado” no tiene criterio observable y la nota no se incluye; obligaría a inventar profundidad y formato.

## DRY-RUN
**Lecturas previstas (hipotéticas):** taskdoc; docs/architecture existentes, `anchoring.md` §6, `rules-language.md`, `rules.md`; `deskops/models/run.py`, `closeout_gates.py`; nota `8bd79409` y drawer de origen; `.sldb/store.yaml`. **Cambios previstos:** crear el `.md` con secciones 1–6 y ejemplos pydantic; añadir su entrada trackeada en el store; nada en `src/`. **Dependencias:** modelo `ArchitectureNarrativeDoc`, CLI `sldb docs track`, fuentes de deskops solo lectura y decisión del dueño. **Validaciones futuras:** `TMPDIR=/dev/shm sldb docs show arch-evidence-model-family --store .sldb`; comprobar seis secciones, `PENDIENTE`, ejemplos `ProofDoc`/`RunDoc`/`TestDoc`, tabla de seis criterios y goldens/children; `TMPDIR=/dev/shm pytest tests/test_clean_code_rules.py tests/test_store_seams.py`.

## FUTURO
El dueño elige opción y sustituye `PENDIENTE`; otro nodo revisa y cierra. Deskops decide su política de cierre; cualquier implementación de `ProofDoc` o de la jerarquía es tarea separada.
