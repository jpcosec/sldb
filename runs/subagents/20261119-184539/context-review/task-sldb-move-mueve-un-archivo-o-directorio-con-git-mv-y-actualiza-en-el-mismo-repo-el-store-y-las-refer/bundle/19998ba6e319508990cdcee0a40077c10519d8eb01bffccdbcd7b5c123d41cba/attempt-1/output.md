REFORMULACION
Nodo ejecutable (task.code), no agregado. Propósito: añadir `sldb move <origen> <destino>` que mueva archivo o directorio con `git mv` (o en disco si no está versionado) y reescriba a la vez las referencias del store y los links Markdown a la ruta vieja, todo en una Transaction. Resultado: comando CLI en src/sldb/cli/, API `move_path` en src/sldb/api/documents/ exportada en sldb.api, reescritores de campos y links, tests en tests/api y tests/cli, referencia selfdoc regenerada, docs y CHANGELOG. Repo: sldb. Límites: solo el store/repo propio (nada de repos o stores enlazados); no texto libre fuera de valores completos de campo o destinos de link; no tocar `move_document` salvo para usar git mv.

AMBIGUEDADES
1. "siguen trackeados con el mismo nombre": no aclara si "nombre" es basename o ruta relativa; al mover un directorio la ruta relativa cambia y obliga a inventar la identidad de tracking.
2. "todo valor de campo que sea exactamente la ruta vieja": no fija formato ni normalización (relativa al repo o al store, `./`, separadores); obliga a inventar la comparación.
3. "los links relativos e inline a la ruta vieja": no dice respecto a qué se resuelven (archivo contenedor o raíz) ni cubre imágenes o links por referencia; obliga a inventar la resolución.
4. "si algo falla, el árbol y el store quedan como estaban": tras aplicar `git mv`, no define el rollback del working tree; obliga a inventar el mecanismo (restore, reset, stash).
5. "--store S" y "--format text|json": no da formato por defecto ni aclara si `--store` cambia la base de rutas; obliga a inventar ambos.
6. "destino existente o fuera del proyecto: error" solo aparece en Implementation Path, no en Goal/Scope; obliga a decidir si es requisito y si mover un directorio sobre otro existente es error.

DRY-RUN
Lecturas: move_document.py, transaction.py, transaction_ops.py (paso move), save_document_payload/fields update, parser CLI, selfdoc. Cambios previstos: move_path reusando move_document por documento bajo el origen; reescritor de campos vía API; reescritor de links Markdown; comando y parser; tests (a–g); selfdoc sync; docs y CHANGELOG. Dependencias: git, Transaction y su paso move, `stores check`, selfdoc. Validaciones futuras: pytest de los dos archivos, selfdoc check, tools/check.sh --fast, stores check y suite completa. Nada se ejecuta aquí.

FUTURO
Un humano decide las semánticas de "mismo nombre", formato de rutas y rollback. Otro nodo ejecuta p1–p6; el integrador corre la suite deskops; closeout commitea con Task-Id y selfdoc produce la referencia.
