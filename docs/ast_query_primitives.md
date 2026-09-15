# Structural Queries Through the CLI

Verified against the working tree on 2026-09-13. The earlier `get_block`, `get_section`, `get_owner_section`, and `find_blocks` signatures were design sketches, not public Python functions. The current interface exposes an AST/IR plus field and section commands.

## Available Operations

Use a tracked document name in place of `guide`, and pass `--store /absolute/path/.sldb` and `--pythonpath /absolute/project/path` where needed.

| Earlier operation | Current CLI | Actual result |
|---|---|---|
| Read a field or list item | `sldb fields show docs/guide/benefits/0` | Typed value in a `value` envelope |
| Inspect a syntax block | `sldb ast show docs/guide` | Syntax tree at `document.ir.surface`; select nodes from the JSON |
| Locate a section | `sldb sections show guide --format json` | Heading paths, context, and heading spans |
| Inspect section hierarchy | `sldb ast show docs/guide` | Nested sections at `document.ir.structure` |
| Inspect field ownership | `sldb ast show docs/guide` | Fields at `document.ir.nodes`, including `field_path` and `owning_section` |
| List a section's fields | `sldb sections fields docs/guide/<section-path>` | Fields assigned to that exact section |
| Search section metadata | `sldb sections find "" --where 'title ~ "How"'` | Matching sections across the selected store |
| Search syntax nodes | `sldb ast show docs/guide` plus a JSON filter | Client-side traversal; no native block-query command |

## JSON Selection Examples

These filters use external `jq`; it is not an SLDB dependency. Add store/pythonpath flags to the SLDB command before the pipe.

```bash
# One top-level syntax block; its array position is not a stable address.
sldb ast show docs/guide | jq '.document.ir.surface[0]'

# All list-item nodes, including nested lists.
sldb ast show docs/guide | jq '.document.ir.surface[] | recurse(.children[]?) | select(.kind == "list_item")'

# Section context for an exact path returned by sections show.
sldb sections show guide --format json | jq '.sections[] | select(.path == "sldb-example-guide/how-it-works")'

# The section currently assigned to one field.
sldb ast show docs/guide | jq '.document.ir.nodes[] | select(.field_path == "how_it_works") | .owning_section'
```

## Limits That Matter

- Section paths include parent headings. Copy the returned path; a leaf slug alone may not match.
- Heading spans identify heading tokens, not the entire section body. Returning every body block up to the next same-or-higher-level heading requires traversing `surface` and computing that boundary.
- `structure` contains the section hierarchy; it does not contain every syntax block as a child of its section.
- Field ownership is a heuristic with a reproduced defect when template and rendered line positions differ. Do not treat it as guaranteed source provenance; see [the review findings](documentation-review.md#field-ownership-and-section-spans).
- Surface nodes expose `kind`, `text`, `span`, `children`, and tag metadata. They are not a lossless serialization of every parser attribute.
- `ast schema` describes the normalized graph vocabulary. For a document's concrete IR, inspect `ast show docs/<name>`.

See [addressability](addressability_model.md) for the existing address syntax and predicate grammar.
