---
clase: objeto
tipo: arista
nombre: arista links_to
estado: borrador
---

# Arista `links_to`

## Qué es

La arista que dice que un store enlaza a otro. Sale del nodo del store (`sldb://store`) y llega
al nodo del store enlazado (`sldb://store/<alias>`). Con ella el store lee los documentos del
otro y hereda sus modelos (`src/sldb/models/builtin_relation_types.py:17`). Es la base de la
federación (`docs/architecture/model-federation-on-the-graph.md:61`).

Es un enlace entre stores. No es la arista `has_model` con `origin_store`, que dice de qué
store viene un modelo heredado (`src/sldb/store/edge_index/store_contribution.py:33`).

## Cómo se nombra

Hoy se nombra por el alias del enlace: `stores add <ruta> --name <alias>` y `stores remove <alias>`
(`src/sldb/cli/parsers/stores.py:17`, `:24`). El alias debe cumplir `LINK_NAME` y no puede ser
`local` (`src/sldb/api/stores/link_store.py:64`). Dentro de los ids de documento aparece como
prefijo: `alias:Model:name`.

En el índice la arista no tiene id propio: es la terna `sldb://store` -[`links_to`]->
`sldb://store/<alias>`. Con la gramática propuesta (borrador) el prefijo `store:` de la
dirección sería el alias; la arista misma no cambia de nombre. Sin verificar: cómo se escribiría
el nodo del store enlazado, la gramática no lo define.

## Dónde se guarda

No hay una sola puerta. Dos archivos guardan el mismo hecho:

- `.sldb/core/store_index.yaml`, lista `stores` (`name`, `path`). Es lo que lee el índice de
  aristas y lo que escribe `stores add` (`src/sldb/api/stores/link_store.py:74`).
- `.sldb/store.yaml`, lista `links`. Es la declaración que `stores build` aplica al índice
  (`src/sldb/api/stores/apply_declaration.py:29`) y que `stores declare` imprime.

La ruta se guarda relativa a la raíz del proyecto, salvo que se escriba con `/`, `~` o `$`
(`src/sldb/api/stores/link_store.py:93`). La arista del índice es derivada: se reconstruye desde
`stores` en cada `edges rebuild` (`src/sldb/store/edge_index/store_contribution.py:25`).

## Los cuatro verbos

| Verbo | Hoy | Evidencia | Qué significa (propuesta) |
|---|---|---|---|
| Crear | `stores add PATH [--name] [--replace]` | `src/sldb/cli/commands/store_add.py:12`; `src/sldb/api/stores/link_store.py:20` | **Sin confirmar:** enlazar el store local con otro; crea la arista y deja el alias disponible en las direcciones. |
| Leer | `stores list [--format]`; `edges show sldb://store`; `graph get` | `src/sldb/cli/commands/stores.py:61`; `src/sldb/api/stores/store_links.py:16`; `src/sldb/cli/commands/edges.py:30` | **Sin confirmar:** dar los stores enlazados y el estado de cada ruta (ok, ausente). |
| Cambiar | `stores add --replace` (apunta el mismo alias a otra ruta). No hay `stores set` ni cambio de alias | `src/sldb/api/stores/link_store.py:44` | **Sin confirmar:** cambiar la ruta o el alias sin soltar la arista. |
| Borrar | `stores remove ALIAS` | `src/sldb/cli/commands/store_add.py:18`; `src/sldb/api/stores/unlink_store.py:18` | **Sin confirmar:** declarar que el enlace se retiró; queda dicho, y el store enlazado no se toca (corregido 2026-11-27 con los fundamentos). |

Restricciones que ya existen:

- `link_store` rechaza un destino que no es store y un store enlazado a sí mismo
  (`link_store.py:40`, `:41`).
- `stores remove` se niega mientras algún modelo local se herede de ese store
  (`unlink_store.py:33`). `--replace` es la salida que el propio mensaje indica.
- Si la carpeta del store enlazado desaparece, la arista sigue (se arma desde `stores`) y
  `stores list` lo marca `missing`. Borrar un store como tal no existe: `stores` no tiene
  `delete` ni `destroy` (`src/sldb/cli/parsers/stores.py:8`).

## Aristas que le llegan y que salen

- Sale de `sldb://store` y llega a `sldb://store/<alias>`; ambos nodos son `sldb_store`
  (`store_contribution.py:23`, `:25`). El tipo es `many_to_many` (`builtin_relation_types.py:17`).
- Aristas de otro tipo que dependen de ella: `has_model` con `origin_store`, y las aristas que
  un store enlazado aporta al índice compuesto con `from_store` en el metadato
  (`src/sldb/store/edge_index/federation.py:47`).
- La crea solo quien corre `stores add` o `stores build`.

## Qué lo mantiene correcto

- Las comprobaciones de `link_store` y `unlink_store` de arriba.
- `stores build` avisa de un enlace declarado cuyo store no está (alerta `build/link-missing`,
  `src/sldb/cli/commands/stores_build.py:67`); `stores list` marca `missing` o `not-a-store`
  (`src/sldb/api/stores/store_links.py:41`). Sin verificar: si `stores check` revisa los enlaces.
- `edges check` valida la arista contra su `RelationTypeDoc` builtin (`links_to`, `sldb_store` a
  `sldb_store`) (`src/sldb/store/edge_index/validation.py:81`).
- Hash: el `store_hash` cubre el índice del store, donde viven los `stores`. Sin verificar si un
  cambio de enlace mueve ese hash.

## Abierto

- ¿Es correcto que el hecho esté en dos archivos (`store_index.yaml` y `store.yaml`), o la
  declaración manda y el índice se deriva siempre?
- ¿El alias es el nombre de la arista (se puede renombrar) o un atributo del store enlazado?
- Un enlace entre stores, ¿es una arista como las demás o es el único caso que no admite
  atributos propios (condición, tipo)?

## Desde los fundamentos

**Qué es.** Una relación entre dos redes: un sistema que dice que otro existe y que puede usar
lo que él declaró. Los nodos extremos son sistemas (un adentro cada uno), no archivos.

**De qué principio cuelga.** 1, El valor sale de las relaciones. Y 3: cada red es un adentro con
su borde, y se toca con otra por un punto preciso.

**Qué contradice los niveles 1 y 2.**
- (a) Borrar: "`stores remove ALIAS` ... quitar la arista". Adentro no se borra: se declara que el
  enlace se retiró y queda dicho.
- (f) "Dos archivos guardan el mismo hecho" (`store_index.yaml` y `store.yaml`): lo que alguien
  declara vive adentro, no en un archivo que se reescribe. Que el hecho esté duplicado es un
  síntoma de eso.
- (h) "el store lee los documentos del otro y hereda sus modelos": lo que se comparte son nodos,
  relaciones y modelos que salieron de lo que entró, no solo documentos.
- (b) El alias como "nombre de la arista" y prefijo de dirección: el nombre no da identidad; la
  da la relación.

**Qué queda igual.** El enlace es una arista con extremos que son stores. Es base de la
federación. `stores remove` que se niega mientras un modelo local dependa del store es
consecuencia que baja por las relaciones. Que la carpeta enlazada desaparezca se nota por su
sensor y no rompe la arista.

## Cómo se absorbe en la lógica de kimun

Lectura del agente, sin confirmar, salvo lo marcado (JP). Ver
`../decisiones/el-kernel-sigue-la-logica-de-kimun.md`.

Es una relación tipada entre grafos.

## Fuentes

`src/sldb/api/stores/link_store.py`, `unlink_store.py`, `store_links.py`, `apply_declaration.py`;
`src/sldb/cli/commands/store_add.py`, `stores.py`, `stores_build.py`; `src/sldb/cli/parsers/stores.py`;
`src/sldb/store/edge_index/store_contribution.py`, `federation.py`; `src/sldb/models/builtin_relation_types.py`;
`.sldb/store.yaml`, `.sldb/core/store_index.yaml`; `docs/architecture/model-federation-on-the-graph.md`;
ayuda `sldb stores --help`.
