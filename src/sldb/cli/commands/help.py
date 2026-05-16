from __future__ import annotations

from typing import Any


TOP_LEVEL_HELP = """SLDB CLI

Treat SLDB as a graph of stores -> models -> fields and docs -> sections -> values.

Common workflows:
  sldb stores init --path .
  sldb models add myapp.docs:Book --store .sldb --pythonpath src
  sldb docs create --model Book -o docs/book.md data.yaml --store .sldb --pythonpath src
  sldb find docs --in physical
  sldb find type.documentation.Readme --in semantic --global
  sldb ast show docs/book
  sldb fields append docs/book/tasks '{"title":"Ship CLI","status":"open"}'

Primary surfaces:
  stores    Store lifecycle and federation
  models    Model contracts and code generation
  docs      Tracked document workflows
  fields    Field inspection and mutation
  sections  Section context and navigation
  ast       Normalized store/model/document graph
  find      Unified semantic + physical retrieval

Advanced:
  legacy    Raw query and link commands from the pre-redesign CLI

Use `sldb help <topic>` for focused help on: stores, models, docs, fields, sections, ast, find, legacy.
"""


TOPIC_HELP = {
    "find": """sldb find

Unified retrieval over the SLDB graph.

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
  --where                       Filter docs/fields/sections using a predicate

Section --where predicates:
  title ~ "pattern"             Regex match on section title
  "term" in about               Term in derived about vocabulary
  "term" in breadcrumbs         Term in hierarchical breadcrumbs
  "tag" in semantic_tags        Tag in document-level semantic tags
  path = "..."                  Exact section path match
""",
    "ast": """sldb ast

Return the normalized AST/graph that SLDB defines.

Examples:
  sldb ast show
  sldb ast show models/Book
  sldb ast show docs/my-book
  sldb ast show fields/status
  sldb ast schema
""",
    "fields": """sldb fields

CRUD plus append/clean operations over model-shaped document fields.

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
""",
    "docs": """sldb docs

Document lifecycle commands.

Examples:
  sldb docs create --model Book -o docs/book.md data.yaml
  sldb docs track docs/book.md --model Book
  sldb docs show my-book
  sldb docs recover my-book
  sldb docs compose my-book -o -
""",
    "models": """sldb models

Model contract commands.

Examples:
  sldb models add myapp.docs:Book --store .sldb --pythonpath src
  sldb models update Book --store .sldb --pythonpath src
  sldb models create Book --template book.md --fields fields.yaml --output myapp/models.py
""",
    "sections": """sldb sections

Section context and navigation.

Examples:
  sldb sections show docs/roadmap
  sldb sections find tasks --in semantic
  sldb sections find tasks --where '"Roadmap" in breadcrumbs'
  sldb sections fields docs/roadmap/roadmap
  sldb sections fields docs/roadmap/roadmap/tasks

Subcommands:
  show    List sections in a document with context
  find    Search sections by term or section context predicate
  fields  Show fields owned by a section path
""",
    "stores": """sldb stores

Store lifecycle commands.

Examples:
  sldb stores init --path .
  sldb stores add ~/.sldb/shared --name shared
  sldb stores check --store .sldb
  sldb stores update --store .sldb --pythonpath src
""",
    "legacy": """sldb legacy

Compatibility surface for the raw query/link commands.

Examples:
  sldb legacy ls st
  sldb legacy get 'st.{Book}.my-book.title'
  sldb legacy find 'st.{Book}' --where 'status = "accepted"'
  sldb legacy recover my-book
""",
}


class HelpCLI:
    """Curated help for the redesigned CLI surface."""

    def run(self, args: Any) -> int:
        topic = (args.topic or "").strip().lower()
        if not topic:
            print(TOP_LEVEL_HELP)
            return 0
        print(TOPIC_HELP.get(topic, f"Unknown help topic: {args.topic}"))
        return 0 if topic in TOPIC_HELP else 1
