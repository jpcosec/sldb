"""Python symbols read with tree-sitter, and a fingerprint per node of each definition.

Ported from kimun's `treesitter_symbols.py` adapter (MIT, same author; the only thing brought
over from kimun, by the owner's authorization), Python only, split to sldb's size rules.
tree-sitter and its grammar are the optional extra `[code]`
(`pip install 'structuredLanguageDB[code]'`): without them `runtime()` raises
`TreeSitterUnavailable`, which the anchoring reports as the error `unavailable`.
The fingerprints are sldb's (docs/architecture/code-anchoring.md §3): the adapter emits the
signature and the docstring; the normalized body is new here.
"""
