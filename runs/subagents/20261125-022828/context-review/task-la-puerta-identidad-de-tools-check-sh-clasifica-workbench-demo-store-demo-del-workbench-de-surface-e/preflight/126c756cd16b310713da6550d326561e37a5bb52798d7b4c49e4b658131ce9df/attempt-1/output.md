## REFORMULACION

Encargo ejecutable (no agregado): en el árbol de trabajo de la tarea del repo `/mnt/ssd/proyectos/SLDB_1/sldb`, añadir a `contracts/identity.toml` un bloque `[[foreign]]` para `workbench_demo`, con las cuatro claves de los bloques `surface` y `sldb` existentes: `path`, `files`, `what` y `verdict`. Resultado: `bash tools/check.sh --fast` devuelve rc 0 (puerta identidad sin violaciones). Límites: no mover ni borrar `workbench_demo/`; no tocar `tools/check_identity.py` salvo instrucción contradictoria (ver AMBIGUEDADES).

## AMBIGUEDADES

1. Alcance contradictorio: «contracts/identity.toml y, si la puerta lo necesita, tools/check_identity.py y su test» frente a «No tocar tools/check_identity.py salvo que check.sh siga en rojo… en ese caso parar y reportar en vez de cambiar la puerta». Obliga a inventar si el script y su test son editables.
2. Entorno de validación: «sale con rc 0 en main» frente a «en el arbol de trabajo de la tarea (no hace falta estar en main)». Obliga a inventar dónde se ejecuta la puerta.
3. Valor de `files`: «files = <salida de 'git ls-files workbench_demo | wc -l', hoy 213>». Obliga a inventar si se recalcula al ejecutar o se fija 213, y qué hacer si el conteo cambió.
4. Formato del bloque: «junto a los [[foreign]] existentes de 'surface' y 'sldb' (mismas cuatro claves)». El input no muestra el TOML; obliga a inventar orden, quoting y sintaxis exacta.
5. Categoría: «con la categoria que corresponda… (o la que el contrato prevea para fixtures o demos versionadas)» convive con la decisión fija de `[[foreign]]`. Obliga a inventar si cabe otra categoría.

## DRY-RUN

Lecturas: `contracts/identity.toml` (bloques `[[foreign]]` de `surface` y `sldb`), `tools/check.sh`, `tools/check_identity.py`, `git ls-files workbench_demo`. Cambios previstos: insertar un único bloque `[[foreign]]` con `path = "workbench_demo"`, `files` numérico, `what` y `verdict` según el texto del encargo. Dependencias: git disponible; parser TOML acepta el bloque. Validaciones futuras: `bash tools/check.sh --fast` (rc 0). Nada ejecutado.

## FUTURO

Un humano resuelve las ambigüedades 1–3 y 5; el ejecutor calcula o fija `files`; si la puerta sigue roja tras el bloque, para y reporta al coordinador (decisión ya tomada el 2026-11-24 sobre `workbench_demo` como ajeno). El cierre en `main` y la aceptación por testers de deskops corresponden a nodos posteriores.
