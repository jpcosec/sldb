## REFORMULACION

**Propósito:** trasladar a sldb, sin reescribir, los modelos de spec por tipo de diagrama que hoy viven en spec2viz, junto con su cargador, su validador y las excepciones que ambos usan, y alojarlos junto a SpecDoc en los modelos de notación de sldb.

**Resultado:** ocho modelos de tipo (clase, secuencia, estado, componente, actividad, despliegue, matriz, reflexión) más carga y validación, con los tests de spec2viz portados en verde (lista cerrada de doce archivos) y paridad de errores frente a las mismas entradas.

**Repo:** sldb (destino); spec2viz solo como origen de código y tests, y no se retira (gate IR13).

**Límites:** nada de compiladores ni renderers; no duplicar SpecDoc/SpecNodeDoc (los modelos de tipo validan contenido, SpecDoc guarda); migrar, no reescribir; dependencias nuevas en sldb solo si son imprescindibles.

## AMBIGUEDADES

1. "el de catálogo solo si no depende de los renderers": obliga a inspeccionar el modelo de catálogo de spec2viz y fijar un umbral de dependencia no definido → inventar criterio de inclusión.
2. "junto a SpecDoc en los modelos de notación de sldb": no se da ruta ni paquete destino → inventar ubicación de módulos.
3. "los ocho modelos" frente a la enumeración de nueve (con catálogo condicional): no se aclara si el octavo cuenta catálogo → inventar cardinalidad.
4. "mismos errores que spec2viz sobre las mismas entradas": no se especifica si "mismo error" es tipo de excepción, mensaje o ambos, ni el conjunto de entradas → inventar criterio de comparación.
5. "los modelos de spec son genéricos": genericidad no es condición observable → inventar qué la satisface.
6. "Origen: el paquete de modelos de spec2viz": sin ruta ni versión/commit → inventar procedencia.
7. "en lo que toquen solo modelos, carga y validación": recorte de tests discrecional → inventar qué se descarta.

## DRY-RUN

**Lecturas:** modelos, `loader`, `validator` y excepciones de spec2viz; los doce tests citados; SpecDoc/SpecNodeDoc y pyproject de sldb.

**Cambios previstos:** módulos de modelo por tipo, cargador, validador y excepciones en sldb; tests portados; dependencias declaradas si procede.

**Dependencias:** acceso al árbol de spec2viz; pydantic u otras, a confirmar.

**Validaciones futuras:** `TMPDIR=/dev/shm pytest -q` archivo a archivo, `tools/check.sh`, `sldb stores build --check`.

## FUTURO

El gate IR13 decide la retirada de spec2viz. Un humano resuelve las ambigüedades 1–7 antes de ejecutar; otro nodo puede declarar dependencias y confirmar la ruta destino.
