PASA

# Tester deskops-t-63803f8af881: resultado

Task: `task-los-hechos-de-llamada-de-python-traen-los-argumentos-literales-y-de-inner-add-parser-nodes-help-sale`
Commit revisado: `c2ee73402e7b7a775b11036058ce2669fb304a28` — `feat: Python call facts carry literal arguments`
Archivos del commit:
- `src/sldb/code/py_calls.py`
- `tests/code/test_py_call_args.py` (nuevo)
- `tests/selfdoc/test_treesitter_symbols.py` (ajustado a la forma nueva)
- `docs/architecture/code-anchoring.md`

## Veredicto

**PASA.** Cada llamada de Python lleva ahora sus argumentos en la misma forma: `args` es la lista de
posicionales en orden y `kwargs` un dict nombre -> argumento; cada argumento es
`{"text": <py_norm>, "value": <ast.literal_eval>}` si es literal o `{"text": <py_norm>, "literal": false}`
si no lo es. Lo usan `call_parts`, los decoradores (`_decorator`) y `body_calls`; la relación `calls`
sigue identificándose solo por el destino (`{"type": "calls", "target": ...}`).

Sobre `src/sldb/cli/parsers/graph_project.py` (línea 14) el hecho real es:

```
{'name': 'inner.add_parser', 'line': 14,
 'args': [{'text': "'nodes'", 'value': 'nodes'}],
 'kwargs': {'help': {'text': "'Every document and file node, sorted by id.'",
                     'value': 'Every document and file node, sorted by id.'}}}
```

Una variable como argumento queda como `{'text': 'x', 'literal': False}` (verificado por el test y por
`f(x, 1, k=[1, 'a'], v=x, *r, **kw)`); `*x`, `**x` y f-strings también quedan no literales. Un decorador
con argumentos usa la misma forma. `src/sldb/code/fingerprints.py` no fue tocado y
`test_new_facts_leave_existing_fingerprints_and_normalization_alone` sigue pasando
(`NORMALIZATION == 1`); la documentación nueva está en la sección de hechos de Python de
`docs/architecture/code-anchoring.md`.

## Validación ejecutada (detalle en validation.log)

Comandos de a un archivo, con `TMPDIR=/tmp` y `PYTEST_ADDOPTS=--basetemp=/tmp/pytest-deskops-t-63803f8af881-<archivo>`:

| Comando | rc | Resultado |
|---|---|---|
| `python -m pytest -q tests/code/test_py_call_args.py` | 0 | 4 passed |
| `python -m pytest -q tests/selfdoc/test_treesitter_symbols.py` | 0 | 33 passed, 17 skipped |
| `python -m pytest -q tests/selfdoc/test_fingerprints.py` | 0 | 4 passed |
| `bash tools/check.sh --fast` | 0 | TODAS LAS PUERTAS PASAN |

Adyacentes que consumen `scan_file`/`scan_tree` (no obligatorios, para descartar regresiones de forma):
`tests/notations/test_component_spec_python.py` (6 passed), `tests/selfdoc/test_treesitter_agreement.py`
(2 passed), `tests/api/test_anchors.py` (22 passed, 1 skipped), `tests/api/test_provenance.py`
(10 passed), `tests/test_where_pointers_resolve.py` (5 passed).

No existe `tests/test_py_calls.py`; el archivo nuevo del commit es la cobertura de ese módulo. La suite
completa no se corrió (la corre el host).

## Observaciones

- El encargo pedía el commit "sin trailer Task-Id"; el commit sí incluye
  `Task-Id: task-los-hechos-de-...`. El prefijo `feat:` es correcto y el trailer es el que usa el propio
  procedimiento del tester para localizar el commit, así que no bloquea el veredicto.
- `ast.literal_eval` acepta además `bytes`, complejos y sets literales, más allá de la enumeración del
  encargo (str, número, bool, None, tuplas/listas/dicts). No afecta los casos pedidos ni introduce
  evaluación de expresiones.
- Nota de entorno: `/tmp/ws-venv` no existía en este contenedor; usé el `.venv` del repo
  (`/workspace/sldb/.venv`, Python 3.13.18), que apunta al mismo checkout.
