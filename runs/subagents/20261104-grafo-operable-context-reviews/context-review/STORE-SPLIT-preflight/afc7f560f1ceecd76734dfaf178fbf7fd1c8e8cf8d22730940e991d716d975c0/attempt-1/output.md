REFORMULACION
El nodo STORE-SPLIT es un TaskDoc ejecutable, no un agregado, para el repo sldb. Propósito: separar el store en .sldb/ operacional y versionado (store.yaml y core/) y .sldb_cache/ regenerable e ignorado, sin journal porque git conserva el pasado. Resultado: layout.py resuelve runtime como .sldb_cache; la política de .gitignore versiona core e ignora cache; init/build/check y un migrate-layout nuevo cumplen el contrato; docs y atom lo fijan; tests lo cubren. Límites: la migración de stores hermanos y los avisos externos quedan al supervisor/integración; debe coordinarse con task-congelar-journal-autoridad-arbol.

AMBIGUEDADES
1. «stores init escribe la línea .sldb_cache/ en .gitignore»: no fija si es el .gitignore de la raíz, del store o ambos, ni creación/idempotencia; obligaría a inventar ruta y política de actualización.
2. «mueva runtime/ a .sldb_cache/ y retire el journal»: no dice si mueve runtime/ o su contenido, qué hace ante colisiones ni si “retirar” borra, archiva o solo deja de usar; obligaría a inventar la migración y el tratamiento de datos.
3. «core versionado, cache ignorada, declaración versionada»: “declaración versionada” no identifica artefacto; tampoco aclara si migrate-layout elimina reglas previas que ignoran core/ y runtime/. Obligaría a inventar el contrato de .gitignore.
4. «stores check alerta si falta o si core/ está ignorado»: no define forma de alerta ni código de salida; obligaría a inventar la interfaz.
5. «los cinco stores de SLDB_1»: no los nombra; obligaría a inventar o descubrir la lista.

DRY-RUN
Un ejecutor futuro leería el TaskDoc, docs/architecture/derived-store-boundary.md, layout.py, gitignore_policy.py, comandos stores y tests, .gitignore y estructura runtime/ de los stores. Prevé cambiar layout, política gitignore, init/build/check, añadir migrate-layout, reescribir docs, crear atom y tests. Depende de task-congelar-journal-autoridad-arbol y del estado de los stores. Validaría con pytest -q tests -k 'layout or gitignore or stores or migrate', init en repo nuevo, build desde .sldb, check en cinco stores y git log de un documento. Sin ejecutar.

FUTURO
El supervisor revisa, migra los stores hermanos y cierra; al integrar se avisa por inbox a deskops, spec2viz, pron y scion. La aceptación final y los cambios externos de .gitignore corresponden a esos nodos/humanos.
