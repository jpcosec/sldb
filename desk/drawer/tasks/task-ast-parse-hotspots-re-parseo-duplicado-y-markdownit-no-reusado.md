# AST parse hotspots: re-parseo duplicado y MarkdownIt no reusado

ID: task-ast-parse-hotspots-re-parseo-duplicado-y-markdownit-no-reusado
Status: deferred
Priority: medium

## Goal

Triage and resolve the inbox message promoted from `desk/inbox/20260928-211441-suggestion-ast-parse-hotspots-re-parseo-duplicado-y-markdownit-no-reusado.md`.

## Scope

Hallazgo de una revisión sobre si convenía migrar el parser de markdown
(mdast/marko/mistune). Conclusión: el parser NO es el problema, pero el
pipeline tiene dos hotspots reales de re-parseo.

## Medición (corpus real: 200 docs, 553 KB, ~2.8 KB promedio)

```
parse only       : 483.2 ms
SyntaxTreeNode   :  56.5 ms  (12% del parseo)
full split_nodes : 561.3 ms
convert overhead :  21.6 ms  (4%)
line->char table :   1.9 ms  (0.3%)
```

El 86% del tiempo es parseo puro de markdown-it-py, que se pagaría con
cualquier parser. mistune v3 sobre el mismo corpus: 437 ms (solo 10% mejor,
a costa de compliance CommonMark). Migrar de parser ahorraría ~77 ms de
561 ms: ruido.

## Hotspots a arreglar

1. `runtime/validation.py:56` llama `ast.split_nodes()` dos veces por
   validación (una para el markdown, otra para el template). El template es
   estable por modelo: debería memoizarse.

2. `store/section_rebuild.py:18` instancia un `MarkdownIt("gfm-like")` nuevo
   en CADA llamada a `_parse_md_nodes`, en vez de reusar una instancia de
   módulo. Además re-parsea documentos que el pipeline ya parseó aguas
   arriba.

Ganancia esperada mayor que cualquier cambio de parser.

## Hallazgo secundario (AST empobrecido, no performance)

`core/ast/markdown_ast_handler.py::_convert` descarta campos que el token de
markdown-it-py SÍ trae: `info` (lang del fence), `markup` y `attrs`.
Verificado:

```
fence |tag code |info 'python' |map [2,5] |markup '```'
```

Propagarlos da ~90% de la "paridad mdast" sin migrar de parser. El 10%
restante son offsets de caracteres (mdast `position`, marko `source_span`),
que se obtienen con una tabla de prefijos línea->offset por documento: costo
medido 1.9 ms sobre 553 KB (0.3% del pipeline). No justifica migrar a marko.

## Source

- `desk/inbox/20260928-211441-suggestion-ast-parse-hotspots-re-parseo-duplicado-y-markdownit-no-reusado.md`

## Done When

- The message is resolved, answered, or promoted into active work.
