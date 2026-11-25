## REFORMULACION

Propósito: completar las decisiones 3 y 4 de §6 de OPERACIONALIZACION-VISTAS en surface/dev, tras la convergencia átomo/field. Resultado: en levira-store/models.py, campos generado:bool y hash_origen:str (sha256 de los source_hash de los átomos citados), función que compara y detecta desactualización y marcador en plantilla; un extractor CLI que usa sldb.api.create_document para escribir AtomDoc con status propuesto sin tocar confirmados; §6 del doc declarando las cuatro decisiones tomadas y su ubicación; seeds y tests. Repo: SLDB_1, rutas surface/dev y docs/surface. Límites: no UI, no modelos de átomo base (los define la tarea bootstrap); exige coordinación con JP y surface/ commiteado; bloqueada por task-diseño-set-bootstrap-de-modelos-tras-la-convergencia-átomo-field.

## AMBIGUEDADES

1. "Esperar a que la tarea del set bootstrap esté cerrada": no define señal de cierre (status, commit, aviso); obliga a inventar el criterio.
2. "Acordar con JP el estado de surface/": sin canal ni evidencia; obliga a inventar procedimiento y qué cuenta como acuerdo.
3. "el sha256 de los source_hash de sus átomos de origen": no fija orden, delimitador ni normalización; obliga a inventar el esquema de concatenación.
4. "una función de lectura dice si está desactualizado": sin nombre, firma ni ubicación; obliga a inventar la API.
5. "un extractor por línea de comandos": sin entrada, formato ni criterio de "propuesto"; obliga a inventar el contrato CLI.
6. "agregar al seed.sh los documentos de ejemplo de prosa generada": sin cantidad ni contenido; obliga a inventar fixtures.

## DRY-RUN

Lecturas: los dos models.py, §6 del doc, ambos seed.sh, posible carpeta de tests en surface/dev. Cambios previstos: campos y marcador en levira, función de comparación, script extractor, §6, seed.sh y tests. Dependencias: cierre de la tarea bootstrap, confirmación de JP, campos ya presentes en atoms-store (152fc723), sldb.api.create_document. Validaciones futuras: los dos comandos seed.sh + stores check; doble ejecución del extractor (sin duplicados ni toque a confirmados); lectura de prosa con hash viejo como desactualizada.

## FUTURO

JP confirma el estado de surface/ y aprueba el commit. La tarea bootstrap produce el set de modelos y su cierre. Un humano valida el criterio de "cerrada" y el contrato del extractor si persisten las ambigüedades 3–5.
