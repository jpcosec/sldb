# Lenguaje de reglas de sldb

Estado (2026-11-06): contrato de semántica del nodo GO02 del plan
`desk/drawer/plans/grafo-operable`, implementado por GO05. Fija la gramática, los caminos,
la semántica trivaluada, el formato de explicación, el hash de contrato y la firma de
evaluación del lenguaje único de predicados de sldb. Los ejemplos de este documento son los
tests de especificación de `tests/test_rules_language_spec.py` (verdes desde GO05); la
implementación, la API y la CLI se describen en la sección 9.

Este documento no describe la API de Python ni la CLI de las reglas (`RuleDoc`,
`rules check`, `rules explain`): eso es GO06. Aquí se fija qué significa un predicado y qué
devuelve evaluarlo. La tabla de equivalencia final conserva los nombres de los dos lenguajes
viejos porque es la tabla histórica que GO10 exime del retiro.

## 1. Gramática (a)

Un predicado es una expresión booleana. Las palabras `and`, `or`, `not`, `in`, `has`,
`nonempty`, `model`, `any`, `all`, `none`, `count` y `rel` son sintaxis del lenguaje; los
nombres de campo y de modelo son los del documento evaluado.

```
expr      := or
or        := and ("or" and)*
and       := not ("and" not)*
not       := "not" not | primary
primary   := "(" expr ")" | atom
atom      := quantifier
           | count_cmp
           | term "in" term
           | term "~" literal
           | term cmp term
           | "has(" campo ")"
           | "nonempty(" campo ")"
           | "model" "<=" nombre_modelo
quantifier:= ("any" | "all" | "none") "(" camino ":" expr ")"
count_cmp := "count(" camino ":" expr ")" cmp term
cmp       := "=" | "!=" | "<" | "<=" | ">" | ">="
term      := campo | literal | lista
lista     := "[" [literal ("," literal)*] "]"
literal   := cadena | número
```

Reglas de forma:

- **Precedencia:** `not` liga más que `and`, y `and` más que `or`. Los operadores binarios
  son asociativos a la izquierda. Los paréntesis agrupan.
- La **conjunción de nivel superior** es la cadena de `and` que queda en la raíz después de
  parsear con esa precedencia. Un `and` dentro de paréntesis, de un `not`, de un `or` o de
  un cuantificador no es de nivel superior.
- Las comparaciones son binarias y no encadenan: `a < b < c` no es una expresión válida.
- `"x" in f` prueba pertenencia si `f` es una lista y subcadena si `f` es un string; para
  cualquier otro tipo es `false`. `f in [ ... ]` prueba pertenencia de un escalar en una
  lista literal.
- `f ~ "patrón"` usa el sabor de expresiones regulares de Python (`re`) y la misma
  semántica de búsqueda que el `~` actual de `where_parse`: `re.search`, no anclaje
  implícito. Un patrón inválido es error de parseo: `WherePredicateError`, la excepción
  existente de `sldb.store.query_engine.where_parse`.
- `model <= X` es verdadero si el modelo del documento es `X` o hereda de `X` por
  `base_models` (la familia de `X`).
- `has(f)` es verdadero si el campo está presente y su valor no es `None` ni la cadena
  vacía. `nonempty(f)` es verdadero si el valor existe y, siendo string, lista, diccionario,
  tupla o conjunto, no está vacío.
- Los literales son cadenas entre comillas dobles (con los escapes de `where_literal`) y
  números. No hay literal de nulo ni de booleano; la ausencia se prueba con `has` y la
  negación.

Ejemplos con el documento `Task:a {note: "x"}` como sujeto:

| Construcción | Predicado | Resultado |
|---|---|---|
| `and` liga más que `or` | `has(status) and status = "open" or has(note)` | `true` |
| `not` liga más que `and` | `not has(status) and has(note)` | `true` |
| paréntesis | `not (has(a) or has(b))` con `Task:b {}` | `true` |
| agrupación a la izquierda | `(has(a) or has(b)) and has(c)` con `Task:c {a: 1, c: 2}` | `true` |
| agrupación a la izquierda | `(has(a) or has(b)) and has(c)` con `Task:d {b: 1}` | `false` |

Comparaciones sobre un documento con `status: "open"`, `priority: 2` (o el valor indicado):

| Construcción | Predicado | Resultado |
|---|---|---|
| igualdad | `status = "open"` | `true` |
| desigualdad | `status != "open"` con `status: "closed"` | `true` |
| menor | `priority < 3` con `priority: 2` | `true` |
| menor o igual | `priority <= 3` con `priority: 3` | `true` |
| mayor | `priority > 3` con `priority: 4` | `true` |
| mayor o igual | `priority >= 3` con `priority: 3` | `true` |

Pertenencia y expresiones regulares:

| Construcción | Predicado | Datos | Resultado |
|---|---|---|---|
| `in` en lista | `"draft" in statuses` | `statuses: ["draft", "open"]` | `true` |
| `in` como subcadena | `"raf" in title` | `title: "draft spec"` | `true` |
| `in` sobre otro tipo | `"x" in priority` | `priority: 5` | `false` |
| escalar en lista literal | `status in ["open", "draft"]` | `status: "draft"` | `true` |
| `~` busca, no ancla | `title ~ "beta"` | `title: "alpha beta"` | `true` |
| regex inválida | `title ~ "("` | — | `WherePredicateError` al parsear |

`model <=`, `has` y `nonempty`:

| Construcción | Predicado | Datos | Resultado |
|---|---|---|---|
| familia de modelo | `model <= BaseDoc` | modelo `ChildDoc`, con `ChildDoc < BaseDoc` | `true` |
| campo presente y no vacío | `has(status)` | `status: "open"` | `true` |
| campo presente pero vacío | `has(status)` | `status: ""` | `false` |
| colección no vacía | `nonempty(tags)` | `tags: ["x"]` | `true` |
| colección vacía | `nonempty(tags)` | `tags: []` | `false` |

## 2. Caminos y cuantificadores (b)

Un **camino** es una secuencia de uno o más pasos. Cada paso se escribe de una de estas
formas:

- `campo` sigue las aristas `references` que ese campo declara. Si el modelo del documento
  actual no declara ese campo como referencia, el conjunto alcanzado es el vacío, no un
  error.
- `rel:<tipo>` sigue las aristas de ese tipo de relación (por ejemplo
  `rel:task_activates`).
- `^campo` es la inversa: los documentos cuyo campo `campo` apunta al documento actual
  (por ejemplo `^subject` son los documentos cuyo `subject` es el actual).

El signo `+` pegado a un paso (`depends_on+`, `rel:tipo+`, `^subject+`) aplica la **clausura
transitiva**: sigue ese paso repetidamente en la misma dirección. El origen queda excluido,
el resultado es un conjunto sin duplicados y la evaluación termina aunque haya ciclos.

Un cuantificador recorre los elementos alcanzados por el camino y evalúa un predicado sobre
cada uno. Los dos puntos separan el camino del predicado: `any(camino: predicado)` es
sintaxis, no una glosa.

- `any(camino: p)` = or del predicado sobre los elementos.
- `all(camino: p)` = and del predicado sobre los elementos.
- `none(camino: p)` = `not any(camino: p)`.

`count(camino: p)` es un entero que solo puede aparecer como un operando de una comparación,
por ejemplo `count(depends_on: status = "open") = 0`.

La sustitución `{campo}` toma el valor del payload del sujeto. Se reconoce únicamente fuera
de literales entre comillas, no admite escapes y usa la sintaxis de `where_subject`. Un
campo ausente o no escalar hace que el predicado no se cumpla.

Ejemplos. La notación `A --depends_on--> B` es una arista `references` del campo
`depends_on`; `A --rel:task_activates--> B` es una arista del tipo de relación indicado.

| Construcción | Predicado | Grafo y datos | Resultado |
|---|---|---|---|
| paso por campo | `any(depends_on: status = "open")` | `A --depends_on--> B`, `B.status: "open"` | `true` |
| cuantificador `all` | `all(depends_on: status = "closed")` | `A --depends_on--> B` y `A --depends_on--> C`, `B.status` y `C.status`: `"closed"` | `true` |
| cuantificador `none` | `none(depends_on: status = "open")` | `A --depends_on--> B` y `A --depends_on--> C`, `B.status` y `C.status`: `"closed"` | `true` |
| campo no declarado como referencia | `any(no_declarado: status = "open")` | `A` sin ese campo de referencia | `false` |
| campo no declarado como referencia | `all(no_declarado: status = "open")` | conjunto vacío | `true` |
| `rel:<tipo>` | `any(rel:task_activates: status = "active")` | `A --rel:task_activates--> B`, `B.status: "active"` | `true` |
| `^campo` | `any(^subject: verdict = "accepted")` | `Review:r --subject--> Task:a`, `r.verdict: "accepted"` | `true` |
| clausura por campo | `all(depends_on+: status = "closed")` | `A --> B --> C`, `B` y `C` con `status: "closed"` | `true` |
| clausura con ciclo | `count(depends_on+: has(status)) = 2` | `A --> B --> C --> A`, con `status` en todos | `true` (termina; origen excluido; sin duplicados) |
| clausura por tipo de relación | `any(rel:task_activates+: status = "done")` | `A --> B --> C`, `C.status: "done"` | `true` |
| clausura inversa | `any(^subject+: verdict = "accepted")` | `Task:a <--subject-- Review:r1 <--subject-- Review:r2`, `r2.verdict: "accepted"` | `true` |
| `count` dentro de comparación | `count(depends_on: status = "open") = 0` | `A --> B`, `B.status: "closed"` | `true` |
| sustitución `{campo}` | `capacity >= {party_size}` | sujeto `{capacity: 6, party_size: 4}` | `true` |
| sustitución con campo ausente | `capacity >= {party_size}` | sujeto `{capacity: 6}` | `false` |
| sustitución con campo no escalar | `capacity >= {party_size}` | sujeto `{capacity: 6, party_size: [4]}` | `false` |
| llaves dentro de un literal | `label = "{party_size}"` | sujeto `{label: "{party_size}", party_size: 4}` | `true` (no se sustituye) |
| referencia a documento inexistente | `count(depends_on: has(status)) = 0` | `A --depends_on--> DocumentoQueNoExiste` | `true` (la referencia se omite) |
| referencia a store enlazado no disponible | `any(rel:external_link: status = "open")` | arista hacia un documento de un store que no se puede abrir | `incomplete` |
| `count` con elemento incomplete | `count(rel:external_link: status = "open") = 0` | igual que la fila anterior | `incomplete` |

## 3. Semántica (c)

Dentro de un store, el lenguaje es bivaluado y de mundo cerrado: lo que no está en el store
no existe. Es un subconjunto de Datalog estratificado, sin funciones salvo las comparaciones
y con negación solo estratificada. El evaluador no inventa hechos ni persiste resultados.

Hay dos ausencias que no se confunden:

- **Documento inexistente dentro de un store disponible:** la referencia no produce
  elemento. El documento se omite del conjunto alcanzado por el camino. Por eso `all` sobre
  el conjunto vacío es `true`, `any` es `false` y `count` vale `0`.
- **Referencia que cae en un store enlazado que no se puede abrir al evaluar:** el elemento
  no se conoce. El resultado es `incomplete`, no `false`.

`incomplete` se combina con la lógica trivaluada de Kleene fuerte. Los valores son `true`
(T), `false` (F) e `incomplete` (I).

| `p` | `q` | `p and q` | `p or q` |
|---|---|---|---|
| T | T | T | T |
| T | F | F | T |
| T | I | I | T |
| F | T | F | T |
| F | F | F | F |
| F | I | F | I |
| I | T | I | T |
| I | F | F | I |
| I | I | I | I |

| `p` | `not p` |
|---|---|
| T | F |
| F | T |
| I | I |

Los cuantificadores son generalizaciones de `or` y `and`. Las columnas son excluyentes:
«algún I, sin T» significa elementos I y F, sin ningún T; «algún I, sin F» significa
elementos I y T, sin ningún F; «algún I con T y F» significa que hay de los tres valores; «todos I» significa que todos los elementos alcanzados son I.

| Forma | Conjunto vacío | Todos T | Todos F | Mezcla de T y F | Todos I | Algún I, sin T | Algún I, sin F | Algún I con T y F |
|---|---|---|---|---|---|---|---|---|
| `any(c: p)` | F | T | F | T | I | I | T | T |
| `all(c: p)` | T | T | F | F | I | F | I | F |
| `none(c: p)` = `not any(c: p)` | T | F | T | F | I | I | F | F |

La comparación con `count` también es trivaluada:

| Elementos alcanzados por el camino | `count(c: p)` | `count(c: p) cmp n` |
|---|---|---|
| Ningún elemento I | entero `k`: número de elementos con `p = T` | T si `k cmp n`; F si no |
| Algún elemento I | I | I |

Cualquier comparación u operador con un operando `incomplete` es
`incomplete`, y un predicado evaluado sobre un elemento `incomplete` es `incomplete`.

Una regla de severidad `error` cuyo resultado es `incomplete` falla con explicación
`"incomplete"`; una regla `alert` lo reporta como alerta.

## 4. Formato de explicación (d)

La evaluación produce findings con cuatro claves:

- `node`: el documento evaluado (su `Model:name`).
- `holds`: `true`, `false` o `incomplete`.
- `clause`: la cláusula textual que decidió el resultado.
- `seen`: mapa `campo → valor leído` de las hojas de esa cláusula.

Ejemplo de una hoja falsa sobre `Task:a {status: "closed"}` evaluando
`status = "open"`:

```json
{
  "node": "TaskDoc:a",
  "holds": "false",
  "clause": "status = \"open\"",
  "seen": {"status": "closed"}
}
```

Regla de `seen` (p4):

- En un `and`, las hojas de la primera rama falsa.
- En un `or`, las hojas de la primera rama verdadera.
- En un `not`, la hoja negada.
- En un cuantificador, las hojas del elemento testigo: el primero que falsa un `all` o el
  primero que cumple un `any` (para `none`, el primero que cumple su `any` interno).

Una hoja `incomplete` aporta el valor `{"incomplete": "<referencia no resuelta>"}`. El
finding (`node`, `holds`, `clause`, `seen`) viaja en el envelope de la CLI. El comando
concreto y la clave exacta del envelope son de GO06 (hipótesis H10), no de este contrato.

## 5. Hash de contrato (e)

Un modelo declara el subconjunto de campos que forman su contrato con el atributo de clase
`__contract__`, una lista de nombres.

- `__contract__` **ausente** (el atributo no está definido): todos los campos del payload del
  documento sujeto.
- `__contract__ = []` (definido y vacío): error al cargar el modelo.
- Un campo listado que falta en el payload aporta la línea `<campo>=` con hash vacío.

El hash de contrato es el `sha256` hexadecimal de las líneas `"<campo>=<field_hash>"`,
ordenadas por los **bytes UTF-8 del nombre del campo**, unidas por `\n` y sin salto final,
codificadas en UTF-8. `field_hash` es el hash de ese campo ya guardado en
`DocumentEntry.field_hashes`.

Por ejemplo, con el contrato `["title", "goal"]` y los hashes `title=t` y `goal=g`, el texto
canónico es:

```
goal=g
title=t
```

y su `sha256` es el hash de contrato. Si `goal` falta del payload, el texto canónico es:

```
goal=
title=t
```

## 6. Firma de evaluación (f)

GO03 implementa y GO05 completa:

```
eval(predicado_parseado, sujeto_opcional) -> lista de findings
```

Cada finding tiene `node`, `holds`, `clause` y `seen`, como en la sección 4.

- **Con sujeto:** un único finding, el de ese sujeto.
- **Sin sujeto:** un finding por cada documento del dominio. El dominio son todos los
  documentos del store, salvo que el predicado sea una conjunción de nivel superior que
  contenga `model <= X`; en ese caso el dominio son los documentos de la familia de `X`.
  Un `model <= X` anidado bajo `not`, `or`, un cuantificador o un camino no restringe el
  dominio.
- Dos `model <=` en la conjunción de nivel superior restringen el dominio a la
  **intersección** de sus familias (p5).
- Una referencia a un documento inexistente se omite del conjunto alcanzado por un camino
  (sección 3): `all` sobre vacío es `true`, `any` es `false` y `count` es `0`.
- Una referencia a un store enlazado no disponible produce `incomplete` en la hoja y se
  propaga con Kleene.

## 7. Tabla de equivalencia

La columna «nuevo» es la construcción del lenguaje de este documento. Ninguna de esas
construcciones usa `eq`, `ne`, `gt`, `lt`, `contains`, `starts_with`, `is_null` ni
`is_not_null` como nombres de operador.

| # | Operador viejo | Origen | Construcción nueva | Nota |
|---|---|---|---|---|
| 1 | `has(f)` | `where_parse` | `has(f)` | presente y no `None`/`""` |
| 2 | `nonempty(f)` | `where_parse` | `nonempty(f)` | rechaza colecciones vacías |
| 3 | `"x" in f` | `where_parse` | `"x" in f` | lista: pertenencia; string: subcadena |
| 4 | `f ~ "pat"` | `where_parse` | `f ~ "pat"` | `re.search`; inválida = `WherePredicateError` |
| 5 | `model <= X` | `where_parse` | `model <= X` | familia por `base_models` |
| 6 | `f = v` | `where_parse` | `f = v` | comparación |
| 7 | `f != v` | `where_parse` | `f != v` | comparación |
| 8 | — | nuevo | `f < v` | no existía en `where_parse` |
| 9 | `f <= v` | `where_parse` | `f <= v` | comparación |
| 10 | — | nuevo | `f > v` | no existía en `where_parse` |
| 11 | `f >= v` | `where_parse` | `f >= v` | comparación |
| 12 | `eq` | `FieldCondition` | `f = v` | mismo valor esperado |
| 13 | `ne` | `FieldCondition` | `f != v` | mismo valor esperado |
| 14 | `gt` | `FieldCondition` | `f > v` | mismo valor esperado |
| 15 | `lt` | `FieldCondition` | `f < v` | mismo valor esperado |
| 16 | `contains` | `FieldCondition` | `"x" in f` | en el viejo, solo listas; en el nuevo, también subcadena |
| 17 | `starts_with` | `FieldCondition` | `f ~ "^x"` | escapar los metacaracteres de `x` |
| 18 | `is_null` | `FieldCondition` | `not has(f)` | aproximación: `has` también rechaza `""` |
| 19 | `is_not_null` | `FieldCondition` | `has(f)` | aproximación: `has` también rechaza `""` |

Las filas 18 y 19 son la equivalencia fijada por el contrato; `has` no distingue `None` de
`""`, así que para datos donde esa diferencia importe hay que consultar el valor y no usar
solo la presencia.

## 8. Hipótesis

Lo que el contrato de GO02 no fija y este documento resuelve de forma provisional. GO05
puede ajustarlo sin cambiar la semántica de las secciones anteriores.

- **H1. Nombres de la API de spec.** Los tests de especificación llaman a un módulo
  `sldb.store.query_engine.rules` con `parse_predicate(texto)`, `eval_predicate(ast, grafo,
  sujeto=None)` y `contract_hash(modelo, field_hashes)`. El contrato fija `eval(predicado
  parseado, sujeto opcional)`, no la ruta del módulo ni la forma de pasar el grafo.
- **H2. Grafo de los tests.** Los tests representan el store como un diccionario
  `{"nodes": {id: {"model": ..., "payload": ..., "base_models"?: [...]}}, "edges": [{"source",
  "type", "target", "field"?, "unavailable"?}]}`. La familia de `model <= X` sale de
  `base_models` del nodo (GO05 p9). El objeto real es el índice compuesto / `GraphBackend`
  de GO03: allí la familia sale de `base_models` de los nodos de modelo, transitivamente.
- **H3. Sujeto de `eval`.** Los tests pasan como sujeto el identificador `Model:name` del
  nodo. GO03 admite además el payload y el `export_id` con proyección.
- **H4. `incomplete` por store no disponible.** Los tests marcan la arista con
  `"unavailable": True`; en el índice real la marca es `metadata.unavailable` de la arista.
  Hoy `compose_edge_index` descarta las aristas hacia nodos que no existen, así que una
  referencia a un store enlazado que no se pudo abrir se lee como documento inexistente
  hasta que el índice la marque.
- **H5. Separación de pasos.** El contrato no fija cómo se concatenan varios pasos de un
  camino. Se propone `.` (`depends_on.rel:tipo`), sin afectar los ejemplos de un solo paso.
- **H6. `^` sobre relaciones.** Se interpreta que `^` también invierte un paso `rel:<tipo>`,
  aunque los ejemplos fijados usan `^campo`.
- **H7. Literales.** Los literales escalares son cadenas entre comillas dobles y números; no
  hay sintaxis de `true`, `false` ni `null`. Las listas literales son de escalares, sin
  anidamiento.
- **H8. Mayúsculas y espacios.** Las palabras clave son minúsculas y sensibles a mayúsculas;
  el espacio en blanco entre tokens no es significativo.
- **H9. Campos anidados.** El contrato no fija campos con punto. Se conserva la resolución
  por ruta de `where_lookup` para un paso de campo: `tasks.0.title`, o la autoridad del
  bloque de procedencia `sldb` de un documento (`--where 'sldb.authority = "source_raw"'`,
  una ruta de campo y no un módulo de Python).
- **H10. Clave del envelope.** El contrato fija que la explicación viaja en el envelope,
  pero no el nombre exacto de la clave; GO06 lo fija al definir `rules explain`.
- **H11. Error por `__contract__` vacío.** Los tests esperan `ValueError`; el contrato solo
  dice «error al cargar el modelo».
- **H12. Separador y `rel` en caminos (GO05).** Un nombre con puntos dentro de un camino son
  varios pasos de campo (`depends_on.subject`); `rel:<tipo>` puede ir en cualquier posición
  (`depends_on.rel:task_activates`). Un campo de referencia llamado `rel` seguido de `:` se
  lee como paso de relación. `^` invierte solo el primer paso del grupo; `+` aplica al último.
- **H13. `doc ~ "re"`.** Como el `~` de `where_parse`, `doc ~` lee el nombre del documento
  (no un campo `doc`).
- **H14. Ausencia en comparaciones.** Un campo ausente no cumple ninguna comparación, `in`
  ni `~`, con literal de cadena o de número. `where_parse` dejaba cumplir `f != <número>`
  sobre un campo ausente y levantaba `TypeError` al ordenar `None` o tipos mezclados; el
  lenguaje devuelve `false` (tabla de equivalencia, golden de la fila 7).
- **H15. Sustitución.** `{campo}` lee el valor de primer nivel del sujeto, también dentro de un
  cuantificador; si alguno falta o no es escalar (cadena o número, no booleano), el predicado
  entero es `false` con `clause` = el predicado y `seen` = los valores leídos.
- **H16. Cláusula de `not` y de los cuantificadores.** `clause` es el texto del `not` o del
  cuantificador; `seen` sigue la sección 4. Un `any` falso, un `all` verdadero y un `count`
  no tienen testigo: `seen` es `{}`.

## 9. Implementación (GO05)

- **Lenguaje:** `src/sldb/store/graph/language/`: tokens, parser (`parse_predicate(texto) ->
  Predicate`, el tipo público parseado: `text` y `root`), átomos y términos, caminos
  (`predicate_paths`, `predicate_reach`), evaluador con Kleene fuerte (`predicate_eval`,
  `predicate_explain`) y la vista mínima de grafo (`predicate_view`: por nodo `model`,
  `base_models`, `payload`; aristas salientes y entrantes con `field`, `type` y
  `unavailable`). `sldb.store.query_engine.rules` es la fachada de los tests de spec
  (`parse_predicate`, `eval_predicate`, `contract_hash`).
- **API única:** `GraphBackend.eval` (sobre la vista del índice compuesto,
  `backend/index_view.py`), `sldb.api.where.where_matches` (un payload suelto),
  `sldb.api.where.where_findings` (un store, sin re-extraer: lee la proyección del índice),
  `sldb.api.where.where_records` (`sldb find --where`), `edges_holding` (la condición de cada
  arista) y `StructuredQuery` (cada `FieldCondition` se traduce por la tabla de la sección 7).
- **CLI:** `sldb find ... --where <expr>` usa el lenguaje: un documento cumple solo si `holds`
  es `true`; un camino recorre el índice del store. `--explain` agrega a `data` la clave
  `findings`, un finding por documento evaluado (cumpla o no). Los registros de campo y de
  sección conservan su lectura propia de `--where`. `sldb --envelope graph query` con filtros
  `FieldCondition` lleva en `warnings` un `{level: "warning", code:
  "deprecated/field-condition", subject: "graph query", what: <el predicado de reemplazo>}`.
- **Shims (GO10 los retira):** `where_parse.compile_where` y `where_parse.where_parse`
  delegan en el lenguaje y emiten `DeprecationWarning`; construir un `FieldCondition` también.
  `--where` nunca avisa.
- **Equivalencia:** `tests/fixtures/where_goldens/` guarda el resultado de cada fila de la
  sección 7 con el código anterior a GO05; `tests/store/test_predicate_language.py` compara.
  Diferencias declaradas: fila 7 con número sobre campo ausente (H14), fila 16 (`in` también
  es subcadena), filas 18 y 19 (`has` rechaza `""`).
