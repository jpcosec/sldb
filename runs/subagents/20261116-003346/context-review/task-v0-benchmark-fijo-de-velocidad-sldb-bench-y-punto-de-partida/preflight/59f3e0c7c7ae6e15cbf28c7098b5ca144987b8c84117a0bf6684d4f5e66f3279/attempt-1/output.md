REFORMULACION

El encargo es crear en el repo sldb el verbo reproducible `sldb bench` para medir rendimiento sin optimizar nada: copiar los desks a un directorio de trabajo y medir, en frío y caliente, tiempo de pared, CPU y RSS máximo de stores update (sin cambios y con un documento cambiado), stores check, stores build --check, deskops doctor, deskops status y arranque de ambos CLI, emitiendo JSON y tabla, y dejar el baseline en `reports/velocidad-baseline-20261115.md`. Límites: solo `src/sldb/cli/bench/`, parser/handler, tests `test_bench_*.py`, selfdoc sync y el informe; fuera: arreglos V1/V2 y cambios en deskops/MEPU.

AMBIGUEDADES

1. “copia desks a un directorio de trabajo” frente a “copias en /dev/shm”: no fija rutas origen, raíz temporal ni limpieza; obligaría a inventarlas.
2. “mide en frío y en caliente”: no define purga de caché, repeticiones, orden ni criterio de calentamiento; obligaría a inventar el protocolo.
3. “con un documento cambiado”: no indica qué documento ni qué cambio; obligaría a inventar el fixture.
4. “el arranque de ambos CLI”: no especifica comando, argumentos ni timeout; obligaría a inventar la invocación.
5. “entrega JSON más una tabla”: no fija esquema, columnas, unidades ni destino; obligaría a inventar el contrato.

DRY-RUN

Lecturas: TaskDoc, estructura de `src/sldb/cli`, parser/handler existentes, tests, selfdoc y `tools/check.sh`. Cambios previstos: paquete bench, subcomando, medición por subprocess con `os.wait4`, serialización JSON/tabla, tests, referencia selfdoc regenerada e informe. Dependencias: `/dev/shm`, deskops instalado, copia de MEPU, pytest, check.sh y selfdoc. Validaciones futuras: los cuatro comandos de Validation, ejecución manual de `sldb bench` y revisión de shas, máquina, tabla por desk/operación y metodología.

FUTURO

Un nodo ejecutor implementará código, tests y baseline; las validaciones emitirán pass/fail; un humano o nodo revisor aceptará el informe, y V1/V2 lo usarán como referencia comparativa.
