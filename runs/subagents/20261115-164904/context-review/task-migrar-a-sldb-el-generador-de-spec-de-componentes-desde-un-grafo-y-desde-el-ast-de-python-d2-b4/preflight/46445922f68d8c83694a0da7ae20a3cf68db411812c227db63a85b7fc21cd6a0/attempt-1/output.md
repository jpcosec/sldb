## REFORMULACION

**Propósito:** migrar a sldb, sin reescribir, la generación de spec de componentes que hoy vive en spec2viz: `component_spec_from_graph` (graph_import) y el generador `python_ast`. **Resultado:** una función de `sldb.api` que devuelve el spec de componentes —según el modelo de la tarea de modelos de spec— desde un grafo, un snapshot node-link o un árbol de Python, reutilizando la proyección de grafo, el inventario `sldb.code` y el cargador de snapshot existentes; tests de paridad portados y un informe de comparación. **Repo:** sldb; spec2viz solo como fuente de comparación y no se retira. **Límites:** no duplicar el escaneo AST de `sldb.code`; no reescribir lo ya cubierto; no retirar spec2viz (IR13).

## AMBIGUEDADES

1. «modelo de componente de la tarea de modelos de spec»: no define interfaz ni campos; obliga a inventar el contrato de retorno.
2. «una función de sldb.api»: sin nombre, firma ni módulo; obliga a inventar la API pública.
3. «sin duplicar el escaneo AST de sldb.code»: no delimita qué cuenta como duplicación; obliga a inventar el criterio.
4. «si sldb ya la cubre, se reutiliza»: sin criterio de cobertura; obliga a inventar el umbral y el formato del informe.
5. «desde un grafo, un snapshot o un árbol de Python»: «árbol» y «AST» se usan indistintamente; no aclara si son la misma entrada.
6. «gate IR13»: no definido; obliga a inventar su efecto sobre el cierre.
7. «Cubre B4 del brief»: brief no incluido; no verificable.
8. «D2»: sin definir.
9. «registrar la comparación en el cierre»: formato de cierre no especificado.

## DRY-RUN

**Lecturas:** TaskDoc dependiente; módulos sldb de proyección, `sldb.code`, cargador node-link; `graph_import` y `python_ast` de spec2viz y sus tests. **Cambios previstos:** módulo/función en `sldb.api`; adaptadores de reutilización; tests portados; informe de comparación. **Dependencias:** modelo de componente de la tarea previa, disponibilidad de spec2viz, gate IR13. **Validaciones futuras:** `TMPDIR=/dev/shm pytest -q` archivo por archivo, `tools/check.sh`, `sldb stores build --check`.

## FUTURO

La tarea dependiente entrega el modelo de componente y su interfaz; un humano o el gate IR13 decide la retirada de spec2viz; el brief define B4 y D2; el revisor acepta el informe de comparación y los tests portados.
