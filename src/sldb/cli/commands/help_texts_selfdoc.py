"""Focused help for parser-derived documentation."""

SELFDOC_HELP = """sldb selfdoc

Derive command and surface documents from an assembled argparse parser.

  sldb selfdoc scan
  sldb selfdoc sync
  sldb selfdoc check

sync/check use the nearest ancestor store, or --store PATH/ALIAS. The default
output is knowledge/ under that store's project root; --output changes it.

For another trusted application:
  sldb selfdoc scan --factory myapp.cli:build_parser --pythonpath src
  sldb selfdoc sync --factory myapp.cli:build_parser --system myapp --pythonpath src

The parser owns command names, synopsis, arguments, and contract provenance.
Authored purpose, how_it_works, usage examples, and tags survive regeneration.
Suppressed commands/options are omitted unless --include-hidden is specified.
Removed commands are reported and their documents retained for review.

check returns 0 when files and tracking are current, 1 for drift. It does not
write documents or indexes. scan constructs the trusted parser without running
command handlers; factory import/construction must itself be side-effect-free.

The provenance hash covers the parser contract, not the handler implementation.
See docs/self-documentation.md for the current scope and remaining work.
"""
