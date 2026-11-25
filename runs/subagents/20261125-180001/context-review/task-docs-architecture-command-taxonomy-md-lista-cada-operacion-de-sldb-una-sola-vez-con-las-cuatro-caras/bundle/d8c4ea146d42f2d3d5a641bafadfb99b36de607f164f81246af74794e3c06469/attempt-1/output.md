## REFORMULACION

Propósito: producir la taxonomía de comandos de sldb (paso 1 del ADR `one-command-taxonomy-served-by-fastmcp`), inventariando cada operación una sola vez a través de sus cuatro caras actuales. Resultado: `docs/architecture/command-taxonomy.md` con tabla aprobable por JP (sustantivo, verbo, lee/escribe, permiso, nombres actuales en `sldb.api`, CLI, `sldb serve`, `sldb mcp`, duplicados/huecos/renombres y nombre canónico propuesto), más `tests/test_command_taxonomy.py` que la mantiene completa. Repo: `/mnt/ssd/proyectos/SLDB_1/sldb`. Límites: solo documento y prueba; no renombrar ni mover código, no tocar CLI ni fastmcp, no cambiar comportamiento; es inventario. No es agregado ni paquete: es una tarea única ejecutable.

## AMBIGUEDADES

1. «cada nombre público de sldb.api» frente a «sldb.api.__all__»: no define si "público" es `__all__` o todo atributo sin guion bajo. Obligaría a inventar el criterio de inclusión.
2. «cada comando hoja de la CLI»: no aclara grupos, alias, comandos ocultos ni comandos compuestos. Obligaría a inventar qué cuenta como hoja.
3. «cada ruta de sldb serve»: no distingue métodos HTTP, rutas internas, OpenAPI/docs/health ni estáticas. Obligaría a inventar el universo de rutas.
4. «nivel de permiso»: no existe escala ni modelo de permisos citado. Obligaría a inventar niveles y su semántica.
5. «un nombre canónico propuesto»: no fija convención de nombres ni criterio de desempate. Obligaría a inventar la convención.
6. «Cada fila dice si lee o escribe»: no contempla operaciones que hacen ambas o ninguna. Obligaría a inventar el tratamiento.
7. «decir en el documento qué se reutiliza»: no determina si SurfaceDoc/selfdoc son fuente, validación o solo mención. Obligaría a inventar su rol.

## DRY-RUN

Lecturas: ADR citado, `docs/architecture/mcp.md`, `sldb.api.__all__`, parser CLI, enrutador `src/sldb/cli/serve`, registro `src/sldb/mcp`, `knowledge/surfaces/` (SurfaceDoc), `sldb selfdoc`, Board y rituales. Cambios previstos: crear el documento y la prueba; ninguno en código. Dependencias: `depends_on: []`, `pills: []`, `atoms: []`, `files: []`; el ADR es dependencia lógica no declarada. Validación futura: `python -m pytest -q tests/test_command_taxonomy.py` y el criterio de completitud del Done When. Sin ejecutar.

## FUTURO

JP aprueba la tabla y decide nombres canónicos y niveles de permiso; otro nodo implementa el servidor fastmcp y el compositor de interfaces sobre esta taxonomía; closeout commitea documento y prueba atómicamente.
