REFORMULACION
Propósito: limpiar residuos de kgdb y cáscaras vacías de la API en los archivos nombrados, sin alterar comportamiento observable (CLI, API pública, tests). Resultado: cada archivo borrado, reducido o conservado con evidencia en `result-summary.md`, entrada en `CHANGELOG.md` y commit. Repo: `/mnt/ssd/proyectos/SLDB_1`; superficies: `src/sldb/cli/parsers/graph.py`, `stores.py` (partes), `src/sldb/cli/commands/help_texts_graph.py`, `src/sldb/store/graph/ingest_sldb.py`, `src/sldb/selfdoc/python_source_graph.py` y módulos de `src/sldb/api` sin lógica propia. Límites: no cambiar comandos CLI ni API pública; mantener `__all__`; nada fuera de esos archivos y la API. Es una tarea ejecutable (`task.code`), no un agregado.

AMBIGUEDADES
1. «cada módulo de src/sldb/api que no tenga lógica propia»: no define "lógica propia"; obligaría a inventar el criterio (¿solo reexports? ¿constantes?).
2. «cáscaras vacías»: no se enumeran; solo se nombran cinco archivos y "además de módulos de la API"; obligaría a inventar cuáles.
3. «src/sldb/cli/parsers/stores.py (partes)»: no dice qué partes; obligaría a inventar el subconjunto.
4. «si nada lo usa»: no define "uso" (import estático, entry point, selfdoc, tests, consumidores externos); obligaría a inventar el método.
5. «sin cambiar ningún comportamiento observable (CLI, API pública, tests)» frente a «No entra: cambiar comandos del CLI»: no aclara si retirar un subcomando huérfano cuenta como cambio; obligaría a decidir por cuenta propia.
6. «reducido a lo que se usa»: sin umbral; obligaría a inventar cuánto conservar.
7. `result-summary.md`: sin ruta; obligaría a inventar ubicación.
8. `pills: []`, `atoms: []`, `depends_on: []`: el ritual exige pills ligadas y auditoría de contexto; sin materia, obligaría a inventar cobertura.

DRY-RUN (hipotético, sin ejecutar)
Lecturas: Board, rituales, TaskDoc, los cinco archivos, `src/sldb/api/*`, tests citados, CHANGELOG y `git log`. Cambios previstos: grep de imports/entry points/selfdoc por archivo; borrar o reducir; ajustar imports; escribir `result-summary.md` con tabla archivo→decisión+evidencia; CHANGELOG. Dependencias: tests existentes, `uv --frozen`, `tools/check.sh`, deskops para Board/closeout. Validaciones futuras: los cinco comandos listados, más auditoría de git/artefactos/árbol limpio.

FUTURO
Deciden humano/supervisor: criterio de "lógica propia" y "cáscaras" (puntos 1-3), confirmación de ausencia de consumidores externos (4), y aprobación de pills/átomos ausentes. Otro nodo/closeout produce commit atómico y verificación deskops.
