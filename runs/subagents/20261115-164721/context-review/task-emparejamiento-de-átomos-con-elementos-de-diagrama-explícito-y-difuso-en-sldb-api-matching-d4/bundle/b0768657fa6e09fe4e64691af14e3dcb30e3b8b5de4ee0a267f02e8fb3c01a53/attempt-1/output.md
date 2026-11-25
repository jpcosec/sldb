## REFORMULACION
Propósito: centralizar en sldb.api.matching el emparejamiento genérico átomo–elemento de diagrama (decisión JP 2026-11-15), evitando matchers por consumidor. Resultado: emparejamiento explícito (vínculo `atoms:`, resolución por id, alias por título y etiquetas) y difuso (similitud), con cobertura y avisos, tests portados verdes y sin matcher duplicado. Repo: sldb; origen: deskops de spec2viz (SldbAtomResolver, parse_atoms, build_atoms_by_view, collect_explicit_atoms, build_explicit_atoms, UnknownAtomError, collect_explicit_refs, build_explicit_refs, attach_atom_edges, build_coverage_by_view, label_key) y tests test_atoms_matching/test_explicit_atoms. Límites: solo lógica de emparejamiento y cobertura; la inyección en HTML del catálogo queda en la capa visual; spec2viz no se retira (gate IR13); migrar, no reescribir.

## AMBIGUEDADES
1. «SI EL CÓDIGO YA EXISTE, SE MIGRA, NO SE REESCRIBE» no indica dónde reside hoy el código de spec2viz; obligaría a inventar ruta y acceso.
2. «si ya cubre el emparejamiento difuso se reutiliza» carece de criterio de comparación; obligaría a inventar umbral/semántica de aceptación.
3. «servirlas con sldb serve si alcanza»: «si alcanza» no se define; obligaría a inventar el juicio de viabilidad.
4. «avisos» sin formato ni comportamiento; obligaría a inventar su contrato.
5. Validación cita «pytest -q de los archivos tocados» sin nombrarlos; obligaría a inventar la lista de tests objetivo.
6. Implementation Path y summary vacíos y depends_on vacío pese a tres tareas hermanas listadas; obligaría a inventar dependencias.

## DRY-RUN
Sin ejecutar. Lecturas: TaskDoc, rituales execution/testing/closeout, código deskops de spec2viz y sus tests, fuente actual de sldb.api.matching (matcher difflib, índice, protocolo embedder). Cambios previstos: comparar; reutilizar el difuso; portar a sldb.api.matching lo explícito (id, alias por título/etiquetas), cobertura y avisos; portar tests. Dependencias: presencia/API del código origen, contrato del embedder, gate IR13. Validaciones futuras: pytest por archivo (TMPDIR=/dev/shm), tools/check.sh, sldb stores build --check.

## FUTURO
Las tres tareas hermanas (generador de spec, modelos por tipo de diagrama, specsync/notations/palettes) transfieren sus piezas en nodos propios. Un humano decide el retiro de spec2viz tras IR13 y si sldb serve cubre el autoguardado o se registra nota al desk.
