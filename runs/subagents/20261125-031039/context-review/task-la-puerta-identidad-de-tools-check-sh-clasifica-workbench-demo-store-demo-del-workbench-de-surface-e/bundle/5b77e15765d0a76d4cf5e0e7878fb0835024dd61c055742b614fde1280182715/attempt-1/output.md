## REFORMULACION

Encargo: añadir en `contracts/identity.toml` un bloque `[[foreign]]` para `workbench_demo`, con `path`, `files`, `what` y `verdict`, para que la puerta identidad de `tools/check.sh` deje de fallar. Resultado: `bash tools/check.sh --fast` sale con rc 0. Repo: `/mnt/ssd/proyectos/SLDB_1/sldb`, en el árbol de trabajo de la tarea. Límites: solo `contracts/identity.toml`; no tocar `tools/check_identity.py` ni su test, ni mover/borrar `workbench_demo/`; si la puerta sigue en rojo tras el bloque, parar y reportar.

## AMBIGUEDADES

1. Cita: “files = <salida de 'git ls-files workbench_demo | wc -l', hoy 213>”. Obligaría a inventar si debe escribirse `213` fijo o el recuento real al ejecutar cuando difiera.
2. Cita: “junto a los [[foreign]] existentes de 'surface' y 'sldb' (mismas cuatro claves)”. El bundle no incluye `contracts/identity.toml`; obligaría a inventar formato exacto, orden y sintaxis TOML concreta.
3. Cita del ritual de testing: “the test suite, plus stores check, tools/check.sh and tools/check_claims.py when the change touches the store, the gates or documented claims”. El TaskDoc solo valida `bash tools/check.sh --fast`; obligaría a inventar si hacen falta esas comprobaciones adicionales.

## DRY-RUN

Lecturas: TaskDoc, rituales, `contracts/identity.toml`, salida de `git ls-files workbench_demo`, y `tools/check.sh`/`check_identity.py` solo para entender la puerta. Cambios previstos: un único bloque `[[foreign]]` en `contracts/identity.toml` con las cuatro claves y los textos indicados. Dependencias: árbol de trabajo, Git y la puerta existente; no hay pills ni átomos ligados. Validaciones futuras: contar archivos, revisar el diff y ejecutar `bash tools/check.sh --fast` esperando rc 0; si sigue rojo, detenerse y reportar.

## FUTURO

El nodo ejecutor produce el cambio y la evidencia de validación. `deskops`/un humano actualizan Board, cierran la tarea y deciden el commit conforme a los rituales. Si la puerta persiste en rojo o el recuento difiere de 213, decide el coordinador; no es una ambigüedad del encargo sino una contingencia de ejecución.
