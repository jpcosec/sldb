# Informe del worker D3

Tarea: migrar a sldb los modelos de spec por tipo de diagrama de spec2viz, con carga y validación (D3).

## Qué se migró, de dónde a dónde

Origen: `spec2viz/spec2viz/{models,loader.py,validator.py,exceptions.py}`. spec2viz no se tocó.
Destino: `src/sldb/models/notation/diagram_specs/`, junto a SpecDoc. Un módulo por clase (regla de una clase por archivo).

- `base/`: DocRef, move_extensions, Metadata, Style, BaseDiagram. `DiagramType` NO se migró.
- Ocho tipos, un subpaquete cada uno (`sequence`, `state`, `component`, `activity`, `deployment`, `matrix`, `class_diagram`, `reflection`), más `catalog`. Las clases son las mismas, con los mismos campos y el mismo texto. Los alias (`Identifier`, `StepTone`, `_PATH_RULE`...) van en `aliases.py` de cada subpaquete. El `model_rebuild()` de `MatrixComponentModel` queda junto a la clase.
- `loader/`: `load`, `unknown_keys`, `AnyDiagram`, `ADAPTER`, `VALID_TYPES` (antes `_valid_types`). `load` se trocea en `read_raw` y `schema_error`, con los mismos mensajes.
- `validator/`: `validate` con un módulo por tipo. Los validadores largos se trocearon en helpers de máximo 10 líneas (`check_members`, `check_relations`, `check_inheritance_cycles`, `validate_packages`, `node_parents`, `check_connections`, `containment`). Los mensajes y el orden de las comprobaciones se conservan.
- `ParseError`: nueva en `src/sldb/notations/errors/parse_error.py`, cuelga de `NotationError` y se exporta desde `sldb.notations.exceptions`.
- API: `src/sldb/api/notations/spec_models.py` con `load_spec(ruta)` y `validate_spec(modelo)`, exportadas desde `sldb.api.notations`.

## Qué se reutilizó de sldb

- `DiagramType` (`sldb.notations.diagram_type`, los mismos ocho valores).
- Las excepciones de `sldb.notations.exceptions`: ValidationError, UnknownReferenceError, EndpointKindError, StructureError, UnknownIconError.
- En `validate_style`, `resolve_color` (`sldb.notations.color_resolution`) y `_builtin_default` (`sldb.notations.styling`), que sustituyen a `spec2viz.palette` y `spec2viz.styling`.
- SpecDoc y SpecNodeDoc quedan sin cambios. No se tocó SpecSync.
- pyproject sin cambios: pydantic y pyyaml ya estaban declarados.
- El subpaquete no importa spec2viz ni renderers.

## Paridad de errores

Un script de una sola vez ejecutó load + validate con spec2viz y con sldb sobre los 35 yml de examples/ y tests/fixtures/ de spec2viz. Compara clase de error, `str(error)` y `model_dump_json` de los que cargan. Resultado: 0 diferencias (25 ok, 4 ParseError, 4 ValidationError, 2 UnknownReferenceError). La única diferencia de diseño es la clase raíz (NotationError frente a Spec2VizError).

## Tests (de a uno, comando indicado, `tests/notations/`)

Fixtures copiadas a `tests/fixtures/specs/` (yml de fixtures, `invalid/` y `examples/*.yml`).

| Archivo | Resultado |
|---|---|
| test_spec_base_model.py | 3 passed |
| test_spec_models_activity.py | 3 passed |
| test_spec_models_component.py | 3 passed |
| test_spec_models_deployment.py | 4 passed |
| test_spec_models_matrix.py | 4 passed |
| test_spec_models_sequence.py | 3 passed |
| test_spec_models_state.py | 3 passed |
| test_spec_loader.py | 20 passed (16 tests; el parametrizado cuenta 5) |
| test_spec_validator.py | 19 passed |
| test_spec_exceptions.py | 2 passed |
| test_spec_class_diagram.py | 17 passed (los 4 de modelo y validación, parametrizados) |
| test_spec_class_packages.py | 7 passed |
| tests/test_clean_code_rules.py | 1103 passed |

`tools/check.sh --fast`: PASS núcleo aislado, capas (0 violaciones), identidad, ejes y superficie. Se omiten afirmaciones, pruebas y selfdoc por `--fast`, así que no se vieron las 11 afirmaciones falsas preexistentes. Con el python del sistema, `ejes` falla por falta de networkx; con el venv del repo pasa.

## Dudas

1. `test_activity_steps_take_project_annotations_only_as_x_keys` está entre los 16 de test_loader del TaskDoc, pero usa compile_ir y render. Lo porté sin las comparaciones de render (quedan las aserciones de `extensions` y el error de clave desconocida), y la comparación de render sigue en spec2viz.
2. `test_every_example_and_fixture_has_only_known_keys` lee los yml copiados en `tests/fixtures/specs/examples`, una copia de lo que existe hoy en spec2viz.
3. No se ejecutaron `sldb stores build --check`, selfdoc ni `deskops graph missing` (el encargo no lo pidió). Es probable que los modelos nuevos pidan regenerar knowledge/ o .sldb; no se hizo. El coordinador debe decidirlo.
4. No se corrió "todos los tests/*.py de a uno" (control de entrega); solo los archivos nuevos o tocados y clean_code.
5. El worker esperó unos 45 min el lock `/dev/shm/sldb1-tests.lock`, ocupado por un `sldb stores build --check` ajeno.
6. `uv.lock` ya aparecía modificado antes de empezar; no es de este trabajo y no se commitea.
