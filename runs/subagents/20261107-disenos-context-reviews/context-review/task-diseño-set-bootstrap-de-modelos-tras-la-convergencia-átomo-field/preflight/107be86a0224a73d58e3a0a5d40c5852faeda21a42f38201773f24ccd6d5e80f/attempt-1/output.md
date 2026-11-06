## REFORMULACION
Propósito: redactar un documento de decisión, no código, sobre la propuesta de siete modelos tras la convergencia átomo/field. Resultado: `docs/architecture/bootstrap-model-set.md`, trackeado como `PlanDoc` con nombre `plan-bootstrap-model-set`, con estructura b5 y nueve puntos b3, cada uno con propuesta, cobertura/contradicción actual citada `archivo:línea`, ejemplo de documento real por export id, recomendación y `Decisión del dueño: PENDIENTE`. Repo: `/dev/shm/sldb-desk`, store `.sldb`. Límites: sin cambios en `src/` ni modelos, sin crear los siete modelos, sin decidir; cierre solo cuando el dueño marque cada punto.

## AMBIGUEDADES
1. “citando archivo:linea: AtomDoc de deskops, RelationDoc/RelationTypeDoc, __compositions__, base_models/herencia, anclas doc: de anchoring.md seccion 6, RuleDoc de rules.md, model_create/model_drafts de SV04, ViewDoc/notaciones de SV01”: faltan rutas y versiones; obligaría a inventar ubicaciones.
2. “los atoms de desk/atoms que traten atomo/field/procedencia/contrato”: criterio de selección impreciso; obligaría a inventar qué atoms incluir.
3. “docs/surface/PROPUESTA-SUPERFICIE.md (seccion 16 o la que hable de la espiral)”: sección exacta incierta; obligaría a elegir por conjetura.
4. “un ejemplo sobre un documento REAL del store de sldb (nombrado por su export id)”: formato del export id y criterio de selección no definidos; obligaría a inventarlos.
5. “PYTHONPATH que vea docs/models.py” y “Los cambios que el track deja en .sldb/ van en el mismo commit”: entorno y flujo git exactos no especificados; obligaría a inventar comandos/rama.
6. “principio del dueno 2026-11-05” y “G_BOUNDARY”: no se da fuente citable; obligaría a inventar referencia.

## DRY-RUN
Lecturas previstas: TaskDoc, drawer citado, `PROPUESTA-SUPERFICIE.md`, `docs/models.py`, módulos citados, `desk/atoms`, `.sldb/store.yaml`. Cambios previstos: crear solo el documento con cinco secciones, nueve subsecciones y tabla resumen, todo en PENDIENTE. Dependencias: CLI `sldb docs track`, modelo `PlanDoc`, PYTHONPATH, store y git. Validaciones futuras: `sldb docs show` renderiza; nueve puntos con ejemplo/export id/recomendación/PENDIENTE; tabla completa; pytest indicado verde. Sin ejecutar nada.

## FUTURO
El dueño decide cada punto como adoptado o rechazado. Otro nodo integra/trackea el documento y confirma el commit de `.sldb`; si algo se adopta, una tarea posterior implementaría, no esta.
