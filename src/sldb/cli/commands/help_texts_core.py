TOP_LEVEL_HELP = """SLDB CLI

Run commands as `sldb ...` or `python -m sldb ...`, not `bash sldb ...`.

SLDB works with three core ideas: a model ref such as `myapp.docs:Book` names a
`StructuredNLDoc` contract, a tracked doc is one Markdown file registered under a
short store name such as `book` or `Book/book`, and a store is the optional `.sldb/`
workspace that keeps model registrations, tracked doc indexes, hashes, and semantic
artifacts without owning the Markdown files themselves. `physical` search means names,
paths, sections, and field addresses. `semantic` search means explicit tags and derived
document/section meaning.

The store is addressable: every field, subfield and list item of every tracked doc has
an address (`st.{Model}.doc.field.sub`, or `docs/doc/field/sub` on the `fields`
surface) and you read, filter and update it by that address. You never open the
Markdown by hand; SLDB re-renders it. See `sldb help legacy` and docs/addressability_model.md.

Common workflows:
  sldb stores init --path .
  sldb models add myapp.docs:Book --store .sldb --pythonpath src
  sldb models list --store .sldb
  sldb docs create --model Book -o docs/book.md data.yaml --store .sldb --pythonpath src
  sldb help docs
  sldb faq
  sldb faq store
  sldb find docs --in physical
  sldb find type.documentation.Readme --in semantic --global
  sldb ast show docs/book
  sldb explore store
  sldb inbox "The meaning of semantic vs physical is still unclear" --kind unclear
  sldb inbox --list
  sldb fields append docs/book/tasks '{"title":"Ship CLI","status":"open"}'
  sldb fields show docs/book/tasks/0/title
  sldb fields query status --global
  sldb find "" --type doc --where 'status = "open"'
  sldb legacy get 'st.{Book}.book.title' --format text
  sldb legacy find 'st.{Book+}' --where 'status = "open"'

Primary surfaces:
  help      Curated first-use guidance
  faq       Question-oriented onboarding answers
  inbox     Log unclear points or suggestions to the active project desk
  stores    Store lifecycle and federation
  models    Model contracts and code generation
  predicates Store-backed semantic link predicates
  docs      Tracked document workflows
  fields    Field inspection and mutation
  sections  Section context and navigation
  ast       Normalized store/model/document graph
  find      Unified semantic + physical retrieval
  explore   Deep markdown docs and docstring search

Advanced:
  legacy    Raw address surface: ls/get/glob/find over st.{Model}.doc.field, se.tag, gse.tag

Use `sldb help <topic>` for focused help on: stores, models, predicates, docs, fields, sections, ast, find, faq, inbox, explore, legacy.
"""

SHORT_ARGPARSE_HELP = """SLDB CLI

Run commands as `sldb ...` or `python -m sldb ...`, not `bash sldb ...`.

SLDB's main workflow is:
  1. `stores init` to create a project workspace when you need tracked docs
  2. `models add module:Class` to register a `StructuredNLDoc` contract
  3. `models list` to inspect what the store already knows
  4. `docs create` or `docs track` to bring Markdown into the store
  5. `fields`, `sections`, `find`, and `ast` to inspect or mutate tracked data

Primary surfaces:
  help      Curated first-use guidance
  faq       Question-oriented onboarding answers
  stores    Store lifecycle and federation
  models    Model contracts and code generation
  predicates Store-backed semantic link predicates
  docs      Tracked document workflows
  fields    Field inspection and mutation
  sections  Section context and navigation
  find      Unified semantic + physical retrieval
  ast       Normalized store/model/document graph
  explore   Deep markdown docs and docstring search
  inbox     Log unclear points or suggestions to desk/inbox/

Other commands:
  extract, render, validate   Direct model-first operations without a store
  init, example               Bootstrapping helpers
  legacy                      Address surface: ls/get/glob/find over st.{Model}.doc.field

Use `sldb help` for the full onboarding help, `sldb find --help` for query examples,
and `sldb docs --help` for document lifecycle details.
"""
