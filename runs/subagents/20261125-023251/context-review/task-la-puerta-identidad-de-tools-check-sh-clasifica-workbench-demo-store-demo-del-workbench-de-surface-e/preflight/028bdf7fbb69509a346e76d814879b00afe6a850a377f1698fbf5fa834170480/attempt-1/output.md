## REFORMULACION

Propósito: restaurar la puerta de identidad de `tools/check.sh`, que falla porque `workbench_demo/` está versionado y no clasificado en `contracts/identity.toml`.

Resultado: un bloque `[[foreign]]` en `contracts/identity.toml` para `workbench_demo`, con `path`, `files`, `what` y `verdict`, de modo que `bash tools/check.sh --fast` salga con rc 0.

Repo: `/mnt/ssd/proyectos/SLDB_1/sldb`, en el árbol de trabajo de la tarea; no exige estar en `main`.

Límites: solo `contracts/identity.toml`; no tocar `tools/check_identity.py` ni su test; no mover ni borrar `workbench_demo/`; validar con `bash tools/check.sh --fast`.

## AMBIGUEDADES

1. «No tocar tools/check_identity.py salvo que check.sh siga en rojo por la puerta identidad despues del bloque; en ese caso parar y reportar en vez de cambiar la puerta.»  
   La excepción “salvo que” sugiere que podría tocarse, pero la continuación ordena parar y reportar. Obliga a inventar si existe algún caso en que tocarlo sea admisible; la lectura segura es no tocarlo nunca.

2. «junto a los [[foreign]] existentes de 'surface' y 'sldb' (mismas cuatro claves)»  
   No fija posición ni orden exactos. Obliga a decidir si basta con añadirlo cerca o si el validador exige un orden concreto.

3. «files = <salida de 'git ls-files workbench_demo | wc -l', hoy 213>»  
   Mezcla un valor calculado con un valor “hoy”. Si el conteo actual difiere de 213, obliga a decidir si prevalece el cálculo o el número citado; el texto indica recalcular.

## DRY-RUN

Lecturas previstas: el TaskDoc, `contracts/identity.toml` (bloques `[[foreign]]` existentes), `tools/check.sh`, salida de `git ls-files workbench_demo | wc -l` y estado del árbol.

Cambios previstos: añadir un único bloque `[[foreign]]` con `path = "workbench_demo"`, `files` como entero calculado, y los textos indicados en `what` y `verdict`.

Dependencias: `git`, `bash` y sintaxis TOML válida.

Validaciones futuras: revisar el diff, ejecutar `bash tools/check.sh --fast` y confirmar rc 0; si la puerta identidad sigue roja, parar y reportar sin modificar la puerta.

## FUTURO

Si tras el bloque la puerta sigue en rojo, el ejecutor reporta y la decisión de cambiar la puerta, el test o `workbench_demo/` queda en manos de un humano o del coordinador. La posible actualización del conteo en metadatos si difiere de 213 también corresponde a otro nodo.
