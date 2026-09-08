EXPLORE_HELP = """sldb explore

Deep search over markdown docs and Python docstrings.

Use this when curated help is not enough and you want to inspect the written knowledge in
`docs/`, `README.md`, `.sldb/README.md`, or Python docstrings across `src/`.

Examples:
  sldb explore store
  sldb explore StructuredNLDoc --source docstrings
  sldb explore compose --source docs
  sldb explore 'semantic.*physical' --regex --source all

Flags:
  --source all|docs|docstrings  Restrict where SLDB searches
  --regex                       Treat the term as a regex
  --docs-root PATH              Docs directory to scan, default `docs`
  --code-root PATH              Python source directory to scan, default `src`
  --max-results N               Limit result count, default 20
"""

LEGACY_HELP = """sldb legacy

The raw address surface: read the store by address without opening Markdown.
Same engine as `fields` and `find`, spelled as addresses.

Address spaces:
  st                            the store: lists every st.{Model}
  st.{Model}                    one model: lists its tracked doc names
  st.{Model+}                   a family: the model and every subclass (base need not be registered)
  st.{Model}.<doc>              one document: ls = fields with descriptions, get = payload
  st.{Model}.<doc>.<field>      one field: get = value (dots reach into dict fields)
  se.<tag>                      semantic: ls = child tags, get = docs carrying the tag
  se.<a>.*.<b> / se.**          glob: * one segment, ** any depth
  gse.<tag>                     global semantic across linked stores (via equivalences)

Commands:
  ls <address>                  List children
  get <address> [--format text|json|yaml]
  glob <pattern>                Expand wildcards on doc and field segments
  find <scope> --where <pred>   Filter docs in an st.{…} or se.… scope (see `sldb help find`)
  recover <doc> | compose <doc> Link recovery and transclusion (also under `docs`)

Examples:
  sldb legacy ls st
  sldb legacy ls 'st.{Book}.my-book'
  sldb legacy get 'st.{Book}.my-book.title' --format text
  sldb legacy glob 'st.{Book}.*.status'
  sldb legacy find 'st.{Note+}' --where 'status = "open"'
  sldb legacy get 'se.type.documentation.atom'

Writes go through `sldb fields update|create|append|clean docs/<doc>/<field>`; SLDB
re-renders the Markdown, validates the roundtrip and updates the hash cascade.
The singular aliases (`ls`, `get`, `glob`, `raw-find`) are deprecated spellings of the same commands.
"""
