## REFORMULACION

Encargo: devolver a `main` de sldb un CI en verde. Resultado observable: el workflow CI de sldb termina en `success` sobre `main` en los jobs `test 3.12`, `test 3.13` y `store`; este último debe construir el store una sola vez y acabar con margen dentro del límite de 6 h, conservando las comprobaciones de `stores build --check` y `selfdoc check`. Repo: sldb (`jpcosec/sldb`). Superficie: `.github/workflows/ci.yml`, `src/`, `tests/`, `CHANGELOG.md`; reproducción local con clones en `/dev/shm/sci/{sldb,deskops,pron}` y el venv indicado. Límites: no cambiar deskops ni pron, no optimizar símbolos más allá de lo necesario, no usar skip/xfail/timeouts como arreglo; el ejecutor commitea en local y el integrador pushea.

## AMBIGUEDADES

1. «primero reproducir y escribir la causa con evidencia (archivo y línea), después arreglar» frente a «La causa: stores build --check reconstruye una copia scratch y no escribe nada». ¿La causa ya está establecida o debe verificarse? Obliga a inventar si se acepta el diagnóstico o se trata como hipótesis.
2. «termine con holgura dentro del límite de 6 h». No define margen ni umbral medible; obliga a inventar el criterio de “holgura”.
3. «sldb de la rama del ejecutor». No nombra rama ni convención; obliga a inventar el nombre y el punto de partida.
4. «gh run list --repo jpcosec/sldb --branch main --limit 1». No garantiza que la última corrida corresponda al commit integrado; obliga a inventar cómo comprobarlo.

## DRY-RUN

Lecturas: task doc, referencias de inbox, `.github/workflows/ci.yml`, código de `stores build`/`--check`, `selfdoc check`, `tools/check.sh`, historial git. Cambios previstos: probablemente `ci.yml`; según opción, `src/` y tests para un modo de build que verifique y escriba, y `CHANGELOG.md`. Dependencias: clones de sldb/deskops/pron, venv, credenciales de lectura, runner y permisos del integrador. Validaciones futuras: `bash tools/check.sh --fast`, `pytest -q -n 4 -p no:cacheprovider`, reproducción local del job store con tiempos antes/después y un solo build, y verificación del run de CI del commit integrado. Sin ejecutar nada.

## FUTURO

El ejecutor elige y justifica la opción (a/b/c), produce el commit local y el informe. El integrador (`wA:p1`) pushea con `jpcosec`. El CI genera la URL y el estado final; un humano o nodo integrador decide aceptar el resultado si el run es `success`.
