## REFORMULACION

Encargo ejecutable sobre el repo `/mnt/ssd/proyectos/SLDB_1`: ampliar `sldb.code` para que los facts de Python incluyan, sin semántica de framework, bases de clase (`extends`), decoradores con argumentos (`attrs.decorators`), llamadas entre símbolos (`calls` + `attrs.calls`) y un `kind` nuevo `assignment` para asignaciones de módulo/clase cuyo valor sea llamada o literal simple. Resultado: readers nuevos en módulos del paquete, integración en `scan_file` para `.py`, fixture Django/DRF en `tests/fixtures/treesitter/`, tests en `tests/selfdoc/test_treesitter_symbols.py`, CHANGELOG, commit y aviso a IR. Límites: no interpretar Django/DRF (eso es specIR), no resolver tipos/imports de llamadas, no tocar TS/JS.

## AMBIGUEDADES

1. «router.register(...) como llamada de módulo (kind call, con func y args)» frente a «un kind nuevo assignment para asignaciones [...] cuyo valor es una llamada»: obliga a inventar si `router.register(...)` es nodo `call` o `assignment`.
2. «urlpatterns = [path(...)]»: una lista de llamadas no es «una llamada o un literal simple»; obliga a inventar su representación.
3. «args, kwargs [...] como texto normalizado»: no define normalización (espacios, comillas, saltos); obliga a inventar reglas.
4. «literal simple»: no enumera qué literales cuentan; obliga a inventar (str, int, bool, listas?).
5. «por la regla de 80 líneas»: no cita la regla ni su alcance; obliga a inventar el criterio de división.
6. «llamadas [...] a otros nombres»: no aclara si incluye builtins (`print`, `len`); obliga a inventar filtrado.
7. «si cambia la forma de los facts existentes, se sube»: no indica versión ni formato; obliga a inventar el valor de NORMALIZATION.
8. El fixture se nombra en Scope pero no figura en `files`; obliga a inventar rutas concretas.

## DRY-RUN

Lecturas: `src/sldb/code/readers.py`, `scan.py`, `facts.py`, `fingerprints.py`, tests citados y fixture existente. Cambios previstos: módulos reader nuevos, esquema de facts ampliado, integración en `scan_file`, fixture y tests, CHANGELOG. Dependencias: tree-sitter Python ya presente, esquema de facts y anclas actuales. Validaciones futuras: los siete comandos de Validation y `tools/check.sh --fast`. Sin ejecutar nada.

## FUTURO

Decisión humana/coordinador sobre NORMALIZATION y representación de `urlpatterns`; interpretación Django/DRF en specIR; aviso a IR y commit los produce el cierre del nodo.
