## REFORMULACION

Encargo ejecutable (task.code, no agregado): centralizar en `sldb.api.matching` el emparejamiento de átomos con elementos de diagrama, por vínculo explícito (`atoms:` en el elemento) y por similitud difusa, migrando la lógica ya existente del módulo deskops de spec2viz (`SldbAtomResolver`, `parse_atoms`, `build_atoms_by_view`, `collect_explicit_atoms`, `build_explicit_atoms`, `UnknownAtomError`, `collect_explicit_refs`, `build_explicit_refs`, `attach_atom_edges`, `build_coverage_by_view`, `label_key`) y sus tests. Resultado: emparejamiento explícito y difuso en `sldb.api.matching`, tests portados verdes, sin matcher duplicado, y decisión sobre `sldb serve` registrada. Repo: `/mnt/ssd/proyectos/SLDB_1/sldb`. Límites: solo emparejamiento y cobertura; la inyección de átomos en el HTML del catálogo queda en la capa visual; spec2viz no se retira.

## AMBIGUEDADES

1. "Primero comparar con sldb.api.matching […] si ya cubre el emparejamiento difuso se reutiliza; migrar lo que falte": no se declara qué cubre hoy el módulo ni qué divergencia cuenta como "falta"; obliga a inventar el criterio reutilizar/migrar.
2. "servirlas con sldb serve si alcanza; si no, registrar el pedido como nota al desk de sldb": "si alcanza" carece de criterio y la nota no tiene formato.
3. "sin matcher duplicado" frente a "spec2viz no se retira (gate IR13)": no aclara si spec2viz conserva su matcher.
4. "pytest -q de los archivos tocados, uno a la vez": no enumera rutas ni destino de los tests portados.
5. "gate IR13": no definido; obliga a inventar su significado.
6. "alias por título y etiquetas": semántica de alias no especificada.
7. Implementation Path vacío ("_Outline the expected implementation route…_"): el ejecutor debe inventar la ruta.

## DRY-RUN

Lecturas: `sldb/api/matching`, módulo deskops de spec2viz, `test_atoms_matching`/`test_explicit_atoms`, `tools/check.sh`. Cambios previstos: portar funciones faltantes, adaptar imports, portar tests, resolver la nota sobre `sldb serve`. Dependencias: matcher difflib, índice de documentos, protocolo de embedder, gate IR13. Validaciones futuras (sin ejecutar): pytest de a un archivo con `TMPDIR=/dev/shm`, `tools/check.sh`, `sldb stores build --check`.

## FUTURO

La decisión sobre `sldb serve` corresponde a JP o a otro nodo; la aprobación del gate IR13 a un humano; la inyección de átomos en el HTML, a la capa visual.
