# The one-screen help `sldb -h` prints; the long onboarding text lives in help_texts_core.
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
  edges     Typed relations and the edge index
  graph     Graph queries: neighborhoods, scope, snapshots
  journal   Write history, chained by hash
  explore   Deep markdown docs and docstring search
  inbox     Log unclear points or suggestions to desk/inbox/

Other commands:
  extract, render, validate   Direct model-first operations without a store
  init, example               Bootstrapping helpers
  selfdoc                     Scan, sync, and check code-derived CLI reference
  legacy                      Address surface: ls/get/glob/find over st.{Model}.doc.field

Use `sldb help` for the full onboarding help, `sldb find --help` for query examples,
and `sldb docs --help` for document lifecycle details.
"""
