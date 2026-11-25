## REFORMULACION

Encargo: ampliar los facts que `sldb.code` extrae de Python (repo `/mnt/ssd/proyectos/SLDB_1`) sin conocimiento de frameworks, para que specIR derive después Django/DRF. Resultado: por clase, relación `extends` con cada base tal cual; por definición, `attrs.decorators` como lista `{name,args,kwargs}`; por función/método, relación `calls` con nombres calificados sin resolver tipos y línea; nuevo `kind assignment` para asignaciones de módulo/clase (incluida `Meta`) con `attrs.call {func,args,kwargs}`, `attrs.items` o `attrs.value`; nueva `kind call` para sentencias de módulo/clase que son solo llamada. Reglas: normalización con `py_norm`, `kwargs` dict, ids nuevos con `take_late`/`flush` tras los existentes, asignación aumentada con `attrs.op`, encadenada un fact por nombre. Fuera: interpretación Django/DRF, resolución de tipos/imports, TS/JS. Límites: respetar tests existentes, CHANGELOG y commit.

## AMBIGUEDADES

1. «attrs.calls con línea de cada llamada» frente a «relación calls desde cada función… hacia cada nombre llamado»: no queda claro si la línea va en la relación o en un `attrs` paralelo; obligaría a inventar el esquema del hecho.
2. «se sube y se dice en el CHANGELOG»: no se indica el número/valor de NORMALIZATION; obligaría a inventar la versión.
3. «El diff de los intentos anteriores … es el punto de partida»: no aclara si debe aplicarse el patch o solo leerse como referencia.
4. «por la regla de 80 líneas»: la regla no se define en el input; obligaría a inventar el umbral exacto.
5. «commit; aviso a IR»: no especifica formato de commit ni canal del aviso.

## DRY-RUN

Lecturas: `readers.py`, `scan.py`, `facts.py`, `fingerprints.py`, tests citados y el patch de referencia. Cambios previstos: módulos nuevos de readers, integración en `scan_file` para `.py`, fixture Django/DRF mínimo y tests en `test_treesitter_symbols.py`, CHANGELOG. Dependencias: `py_norm`, `Ids.take_late/flush`, orden de ids de HEAD. Validaciones futuras: los siete comandos de Validation y `tools/check.sh --fast`, más estado de anclas existentes. Sin ejecutar nada.

## FUTURO

Deciden o producen otros: el humano aprueba la versión de NORMALIZATION y el commit/aviso a IR; specIR interpreta los facts como rutas, campos y serializers; el nodo de validación confirma el paso de los tests.
