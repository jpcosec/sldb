## REFORMULACION

**Propósito:** que los specs de `docs/architecture/spec2viz` se construyan con `specir catalog build` y se sincronicen al store con `sldb notations sync --catalog`, dejando de invocar `spec2viz` para construirlos.

**Resultado:** `docs/architecture/spec2viz/vistas.yml` y sus specs construidos por `specir`; instrucciones de build/sync, `contracts/identity.toml:299` y documentación afectada actualizadas; sin invocaciones de `spec2viz catalog build` en esos puntos.

**Repo:** `sldb` (`/mnt/ssd/proyectos/SLDB_1/sldb`).

**Límites:** no mover ni renombrar la carpeta; el cambio se limita a instrucción de build/sync, `identity.toml` y documentación que nombre `spec2viz catalog build`.

## AMBIGUEDADES

1. «Reemplazar las invocaciones de spec2viz catalog build por specir catalog build y sldb notations sync --catalog»: no se enumeran los archivos ni si el reemplazo es uno-a-uno o añade un paso de sync. Obliga a inventar el inventario de invocaciones.
2. «contracts/identity.toml:299»: la línea puede haber cambiado y no se indica el texto exacto a sustituir. Obliga a inventar el alcance del cambio.
3. «la documentación que nombra spec2viz catalog build»: no se delimita qué documentos entran. Obliga a inventar el conjunto documental.
4. «vistas.yml y sus specs»: no se lista qué specs componen el conjunto. Obliga a inventar los archivos objetivo.
5. «sin coincidencias de invocación»: no se distingue mención documental de invocación ejecutable. Obliga a inventar el patrón de grep y su criterio.

## DRY-RUN

**Lecturas:** TaskDoc; `contracts/identity.toml` en torno a la línea 299; instrucciones de build/sync bajo `docs/architecture/spec2viz`; grep de `spec2viz` en esos ámbitos.

**Cambios previstos:** sustituir invocaciones `spec2viz catalog build` por `specir catalog build`; añadir o ajustar `sldb notations sync --catalog`; actualizar `identity.toml`; corregir documentación.

**Dependencias:** que existan y funcionen `specir catalog build` y `sldb notations sync --catalog`; que la ruta de `vistas.yml` sea la correcta.

**Validaciones futuras:** `sldb notations sync --catalog docs/architecture/spec2viz/vistas.yml --check`; `bash tools/check.sh --fast`; grep sin invocaciones de `spec2viz`.

No se ejecuta nada.

## FUTURO

Mover o renombrar la carpeta queda para el archivado de `spec2viz`; el fin de la paridad y la retirada de los specs como fixtures los decide un humano.
