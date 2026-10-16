DOCS_HELP = """sldb docs

Document lifecycle commands.

`docs create` renders a new Markdown file from a registered model plus inline YAML/JSON
or a YAML/JSON file, then tracks it. `docs track` validates and registers an existing
Markdown file. `docs update` re-renders an already tracked doc with new payload data.
`docs recover` resolves `[[links]]` and `[predicate:: [[links]]]`. Predicate axes come
from definitions registered in the selected store. Unregistered predicates use `CUSTOM`.
`docs compose` expands `![[transclusions]]`. `docs show` and `docs exists` take `alias:ref`
for a store linked directly as `alias` (`stores add --name`); `docs exists` reads indexes only
and exits 0 ok, 1 missing, 2 ambiguous, 5 link-missing or link-broken.

Examples:
  sldb docs create --model Book -o docs/book.md data.yaml
  sldb docs track docs/book.md --model Book
  sldb docs update my-book '{"title":"Updated"}'
  sldb docs show my-book
  sldb docs exists deskops:task-x --format json
  sldb docs recover my-book --store .sldb --format json
  sldb docs compose my-book -o -
  sldb docs explore compose --source all
"""

PREDICATES_HELP = """sldb predicates

Manage the predicate vocabulary used by `[predicate:: [[target]]]` links.

Definitions are persisted in the selected store. Each definition has a link name, a
semantic axis, and an optional description. New stores include editable defaults.
Unknown or removed predicates remain parseable and recover with axis `CUSTOM`.

Examples:
  sldb predicates add depends_on --axis DEPENDENCY --description "Declares a dependency." --store .sldb
  sldb predicates list --store .sldb
  sldb predicates show depends_on --store .sldb --format yaml
  sldb predicates validate --store .sldb
  sldb predicates validate depends_on --store .sldb --format json
  sldb predicates remove depends_on --store .sldb
  sldb docs recover doc.md --store .sldb --format json

Subcommands:
  add       Register a unique predicate name and axis
  list      List definitions in text, JSON, or YAML
  show      Show one definition
  validate  Validate one definition or the complete registry
  remove    Remove a definition; existing links then use `CUSTOM`
"""

MODELS_HELP = """sldb models

Model contract commands.

`models list` shows the registered model names in one store. `models add` expects a
Python import reference in the form `module:ClassName`. The class must be a
`StructuredNLDoc` subclass. Use `--pythonpath` when the module lives in your current
project instead of an installed package.

Examples:
  sldb models list --store .sldb
  sldb models add myapp.docs:Book --store .sldb --pythonpath src
  sldb models update Book --store .sldb --pythonpath src
  sldb models create Book --template book.md --fields fields.yaml --output myapp/models.py
"""
