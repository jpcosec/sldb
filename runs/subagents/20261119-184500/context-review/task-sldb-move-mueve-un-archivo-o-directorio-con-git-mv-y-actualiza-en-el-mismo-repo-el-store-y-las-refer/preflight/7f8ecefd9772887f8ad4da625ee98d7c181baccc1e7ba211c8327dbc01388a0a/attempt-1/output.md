## REFORMULACION

Encargo ejecutable (`task.code`, no agregado): implementar en el repo `sldb` el comando `sldb move <origen> <destino> [--store S] [--dry-run] [--format text|json]`. Propósito: mover archivos/directorios registrando el renombre en git y dejando coherentes el store y los Markdown del propio repo. Resultado: comando CLI, API `move_path` que reutiliza `move_document`, reescritura de valores de campos y links, tests, referencia CLI regenerada, docs y CHANGELOG. Límites: solo el repo/store propio; no otros repos ni stores enlazados; no reescribir texto libre; no modificar `move_document` salvo para usar `git mv`.

## AMBIGUEDADES

1. «Todo pasa en una Transaction: si algo falla, el árbol y el store quedan como estaban». No se define cómo una Transaction revierte `git mv` y cambios de archivos fuera del store; obligaría a inventar el mecanismo de rollback del árbol e índice git.
2. «Si el origen está versionado en git, usa git mv». No aclara qué ocurre con directorios parcialmente trackeados, archivos ignorados dentro de ellos ni destinos ya versionados; obligaría a inventar la regla de decisión.
3. «todo valor de campo que sea exactamente la ruta vieja». No define “valor de campo” para listas, objetos, campos calculados, rutas absolutas, `./` o barras normalizadas; obligaría a inventar el alcance y la comparación.
4. «los links relativos e inline a la ruta vieja». No aclara imágenes, links por referencia, anclas, query, links absolutos ni desde qué archivo se calcula la relatividad; obligaría a inventar el parser y la resolución.
5. «la referencia de CLI regenerada con selfdoc sync». No indica si el ejecutor debe commitearla ni con qué mensaje además del trailer `Task-Id`; obligaría a inventar el flujo de commit.

## DRY-RUN

Un ejecutor futuro leería `move_document.py`, `transaction.py`, `transaction_ops.py`, la API de campos, CLI y tests. Crearía primero tests fallidos en repo git temporal; luego implementaría `move_path`, reescritura de campos/links y CLI; después ejecutaría `selfdoc sync`, actualizaría docs/CHANGELOG y correría `pytest` indicado, `selfdoc check`, `tools/check.sh --fast` y la suite completa. Depende de git, store temporal y API de sldb. No se ejecuta nada aquí.

## FUTURO

Otro nodo integrador ejecutará la suite completa y deskops; un humano validará alcance y commit. `selfdoc sync` producirá la referencia CLI.
