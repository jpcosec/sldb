## REFORMULACION
Encargo ejecutable (`task.code`) en el repo `/mnt/ssd/proyectos/SLDB_1/sldb`: corregir cuatro huecos del CLI detectados por la matriz UX de sldb-ui. Resultado esperado: `fields update`/`append` aceptan `--string` para tratar el valor literalmente y `--format json|text|yaml`; `inbox --show` de una nota inexistente informa por stderr con exit ≠ 0; `inbox <msg> --store <dir>` sin `.sldb` falla sin escribir. Incluye ayuda, tests en `tests/test_cli_v2.py`, `CHANGELOG.md`, sincronización de selfdoc por flags nuevos y gates. Límites: no incluye `promote` del inbox ni otros comandos.

## AMBIGUEDADES
1. “los de fields” (Implementation Path): `files` solo nombra `inbox_create.py` e `inbox_parse.py`; obliga a inventar qué módulos implementan `fields update`/`append`.
2. “--string (el valor se toma literal, sin YAML)” y “--format json|text|yaml”: no aclara si ambos flags aplican a `update` y `append` ni cómo interactúan entre sí; obliga a inventar matriz de compatibilidad.
3. “inbox --show ... exit distinto de 0”: no fija código ni texto exacto; obliga a inventar el contrato observable.
4. “falla con un error que lo dice”: no especifica mensaje ni exit; obliga a inventar redacción y código.
5. “commitear la referencia CLI que regenere”: no dice ruta del artefacto generado ni si entra en el commit; obliga a inventar alcance del commit.
6. “aviso a sldb-ui”: no define canal ni formato; obliga a inventar el mecanismo.

## DRY-RUN
Un ejecutor leería TaskDoc, referencias, parsers/comandos de fields e inbox, tests existentes, CHANGELOG y configuración de selfdoc. Cambiaría parsers/ayuda para `--string` y `--format`, el manejo de errores de `inbox --show` y la validación de `--store`, añadiría tests que fallen antes y actualizaría CHANGELOG. Dependencias: módulos reales de fields, convención existente de `--format`, infraestructura de tests y selfdoc. Validaciones posteriores: pytest de `test_cli_v2.py`, `test_address_surface.py`, `test_clean_code_rules.py`, `bash tools/check.sh --fast`, `selfdoc sync/check`; después commit con rutas y `Task-Id`.

## FUTURO
La ejecución produce código, tests, CHANGELOG, referencia CLI regenerada y commit. Otro nodo integra y verifica gates/selfdoc; un humano decide aceptación y publicación. sldb-ui consume el contrato resultante.
