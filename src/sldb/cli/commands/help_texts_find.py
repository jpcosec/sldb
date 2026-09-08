FIND_HELP = """sldb find

Unified retrieval over the SLDB graph.

Use `--in physical` when you know a file name, tracked doc name, field path, or section
title. Use `--in semantic` when you know a tag or concept such as
`type.documentation.Readme`. Use `--in both` when you want SLDB to search both layers.

Examples:
  sldb find docs --in physical
  sldb find models
  sldb find status --in both --where 'value = "open"'
  sldb find Readme --in semantic --global
  sldb find auth --in physical --regex
  sldb find tasks --type section --where '"Tasks" in about'
  sldb find tasks --type section --where '"Roadmap" in breadcrumbs'

Flags:
  --in semantic|physical|both   Search mode, default both
  --global                      Include linked stores
  --regex                       Treat the term as a regex
  --fuzzy                       Use fuzzy matching
  --type                        Restrict to store|model|doc|section|field
  --where                       Filter docs/fields/sections using one predicate

Document --where predicates (--type doc):
  has(field)                    Field present and not empty
  "x" in field                  Item of a list field, or substring of a string field
  field ~ "regex"               Regex on the value; doc ~ "regex" matches the doc name
  field = "v" | field != "v"    String equality
  field >= n | field <= n       Numeric comparison
  model <= Base                 Model is Base or a subclass (family filter)

Field --where predicates (--type field):
  value = "v" | value != "v"    The field's value
  doc = "name" | model = "M"    Owner document / model
  has(value)                    Non-empty value

Section --where predicates (--type section):
  title ~ "pattern"             Regex match on section title
  "term" in about               Term in derived about vocabulary
  "term" in breadcrumbs         Term in hierarchical breadcrumbs
  "tag" in semantic_tags        Tag in document-level semantic tags
  path = "..."                  Exact section path match

One predicate per --where. To read or write a single field by address, see
`sldb help fields` and `sldb help legacy` (docs/addressability_model.md).
"""

AST_HELP = """sldb ast

Return the normalized AST/graph that SLDB defines.

Use this when you want to inspect how SLDB sees a tracked resource, including sections,
field ownership, context index, and the semantic/physical edges that power navigation.

Examples:
  sldb ast show
  sldb ast show models/Book
  sldb ast show docs/my-book
  sldb ast show fields/status
  sldb ast schema
"""

FIELDS_HELP = """sldb fields

CRUD plus append/clean operations over model-shaped document fields.

Use fields commands when you want to read or mutate data values without hand-editing the
whole Markdown file. Targets always point into either a registered model schema or a
tracked document payload.

Examples:
  sldb fields show models/Book
  sldb fields show docs/my-book/title
  sldb fields update docs/my-book/title 'Updated title'
  sldb fields append docs/my-book/tasks '{"title":"Fix bug","status":"open"}'
  sldb fields clean docs/my-book/tasks --dedupe --drop-empty

Target forms:
  models/<Model>
  models/<Model>/<field.path>
  docs/<DocName>/<field.path>
  docs/<Model>/<DocName>/<field.path>

Field paths reach into subfields: a key of a dict field (`docs/book/metadata/author`)
or a list item / table row by position (`docs/book/tasks/0/status`). `update` and
`show` accept any depth; `append` and `clean` target the list itself.
"""
