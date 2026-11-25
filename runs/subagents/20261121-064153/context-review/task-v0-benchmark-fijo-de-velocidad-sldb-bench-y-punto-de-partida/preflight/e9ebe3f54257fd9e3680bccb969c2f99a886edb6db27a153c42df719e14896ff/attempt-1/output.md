## REFORMULACION

Propósito: tener una medición fija y repetible de velocidad de sldb y deskops antes de optimizar. Resultado: verbo `sldb bench` en `src/sldb/cli/bench/` (parser, handler, medición por subprocess con `os.wait4`), tests `tests/test_bench_*.py`, CLI selfdoc sincronizada e informe `reports/velocidad-baseline-20261115.md` con shas, máquina, tabla por desk/op y metodología. Repo: sldb; deskops se invoca como CLI externo y MEPU solo se copia. Límites: solo medición; nada de arreglos V1/V2 ni cambios en deskops/MEPU; el protocolo de copias, frío/caliente, orden de operaciones, documento tocado, arranque, JSON y tabla queda fijado por el encargo.

## AMBIGUEDADES

1. «reports/velocidad-baseline-20261115.md»: no indica raíz ni si el sufijo debe coincidir con la fecha de ejecución (el encargo es del 21-11). Obliga a inventar la ubicación y el nombre.
2. «python -m sldb --help con el sldb bajo prueba»: no define cómo se selecciona ese intérprete o instalación. Obliga a inventar un flag o convención.
3. «cuyo path es .md y existe»: no aclara si «.md» es sufijo del nombre ni qué hacer si la lista no arroja ninguno. Obliga a inventar criterio y fallback.
4. «mediana si N>1»: con N par no define el cálculo. Obliga a elegir convención.
5. «los desks de sldb, deskops y MEPU»: no da rutas ni nombres, y «MEPU» no se define. Obliga a inventar el mapeo `NOMBRE=RUTA` del baseline.
6. «se copia el árbol de trabajo ... incluye .git»: tensión léxica entre árbol de trabajo y copiar `.git`; (c) la resuelve, pero deja dudas sobre archivos ignorados.

## DRY-RUN

Lecturas: TaskDoc, CLI y estructura actuales de sldb, selfdoc y tests existentes. Cambios previstos: paquete `bench` (parser, handler, medición, agregación JSON/tabla), registro del verbo, tests unitarios, selfdoc sync e informe. Dependencias: deskops en PATH o `--deskops`, git, `/dev/shm`, `sldb docs list`, permisos de copia. Validaciones futuras: los cuatro comandos de Validation y `sldb bench` sobre las copias. Sin ejecución.

## FUTURO

Decide un humano: rutas y nombres de los desks del baseline, máquina y workdir definitivos, y aprobación del informe. Los arreglos de velocidad V1/V2 corresponden a otros nodos.
