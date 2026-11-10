## REFORMULACION

Encargo ejecutable (`task.code`), no agregado. Propósito: que `sldb stores build` y `build --check` toleren un store enlazado ausente emitiendo una alerta, para desbloquear el CI de deskops sin repos hermanos. Resultado: build no lanza y reporta `links_missing`; `--check` da ok con alerta `build/link-missing` (nombre y ruta); links presentes o destinos inválidos no cambian. Repo: sldb origin/main; superficie: `apply_declaration.py`, `build_store.py`, `cli/commands/stores_build*.py`, `tests/api/`, `CHANGELOG.md`. Límites: no tocar `link_store` para links presentes; deskops solo como prueba consumidora.

## AMBIGUEDADES

1. «apply_links salta el link cuyo destino no tiene store (store_exists sobre root/path)»: no define `store_exists` (¿nueva o existente?, ¿comprueba `.sldb/store.yaml`, directorio?). Obliga a inventar la detección y su semántica.
2. «un link cuyo destino existe pero no es un store válido [...] sigue siendo error»: no explica cómo separar "no existe" de "existe pero inválido" si `_check_other_exists` usa el mismo error. Obliga a inventar el criterio.
3. «links_missing (lista de {name, path})»: no fija el esquema exacto ni su forma en el plan (`apply=False`). Obliga a inventar el shape.
4. «código build/link-missing, subject = nombre del link y what = la ruta declarada...»: no define la API/campos de `alert_sink` ni la severidad. Obliga a inventar el registro.
5. «termina con exit 0 y con las 4 alertas build/link-missing»: no enumera los links de deskops. Obliga a asumir que son exactamente 4 y todos ausentes.
6. «un clon limpio de deskops wt/main-en-verde-2 en /dev/shm»: no da URL ni procedimiento de clonado. Obliga a inventarlo.
7. «los tests existentes de stores build y build --check (grep stores_build en tests/)»: no lista los tests. Obliga a inventar el conjunto.

## DRY-RUN

Lecturas: `apply_declaration.py:24`, `link_store.py:50`, `build_store.py`, `stores_build*.py`, `tests/api/`, `tests/test_clean_code_rules.py`, `CHANGELOG.md` y grep de tests. Cambios previstos: s1 skip y retorno de missing; `build_store` añade `links_missing` en build y plan; s2 alerta al sink sin cambiar `ok`; s3 resumen; s5 test nuevo y ajustes; s6 prueba manual. Dependencias: semántica de `store_exists`, contrato de `alert_sink`, clon de deskops. Validaciones futuras: pytest del test nuevo y de los existentes de a uno, `test_clean_code_rules`, y `build --check` en clon sin hermanos con exit 0 y 4 alertas. Sin ejecutar.

## FUTURO

El ejecutor implementa y corre las validaciones; un humano/coordinador confirma la decisión revisable (b) y el número de links; otro nodo podría encargarse de CI o del CHANGELOG.
