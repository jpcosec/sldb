# The store declaration: `.sldb/store.yaml`

`.sldb/store.yaml` is the part of a store that is source: what `sldb stores build` rebuilds
the derived indexes from (`docs/architecture/derived-store-boundary.md`). Its model is
`sldb.api.StoreDeclaration` (`src/sldb/api/stores/store_declaration.py`): `version`, `links`,
`models`, `predicates`, `generate`, `derived`, `include`, `graph_backend`, `policy`, and since
node GD26 of the plan `generalizar-desde-deskops`, `folders` and `seeds`. A declaration
without those two keys is read and written exactly as before: both are left out of the dump
when empty.

## `folders` and `seeds`

A consumer that keeps its working tree in a store (deskops keeps a desk) needs the tree to
exist before anything is tracked: a few directories and a few files that are there on the
first run and are not touched afterwards, or that are kept equal to a template. That is the
scaffold, and the declaration names it:

```yaml
folders:
  - inbox
  - notes/archive
seeds:
  - path: inbox/.keep
    mode: if_missing
    text: ""
  - path: README.md
    mode: managed
    file: readme.tpl                     # relative to the template root
  - path: GUIDE.md
    mode: managed
    file: pkg:consumer_package/templates/guide.md
  - path: notes/welcome.md
    mode: if_missing
    document: {model: NoteDoc, name: welcome, payload: {title: Welcome, body: Start here.}}
    track: true
```

- **`folders`**: directories, relative to the project root. Each is created with its parents.
  It has no mode: an existing directory is `present`, a path held by a file is a conflict.
- **`seeds`**: files, one `Seed` each (`sldb.api.Seed`, `src/sldb/api/stores/seed.py`):
  - `path`: relative to the project root (the same root `build` and `include` use); it must
    stay inside it.
  - `mode`: `if_missing` (the default) never overwrites: a file that exists is `present`, whatever
    it holds. `managed` compares the file's bytes with the source's and, when they differ,
    rewrites it.
  - exactly one source:
    - `text`: the literal, written in UTF-8 as is, with no newline added;
    - `file`: a template. A relative path is read from the **template root**: the store
      directory (`.sldb/`) by default, or what the caller passes as `template_root`.
      `pkg:module/path` is read with `importlib.resources.files("module").joinpath("path")` from the
      importable package, wherever it is installed; it resolves relative to nothing else;
    - `document`: `{model, name, payload}`, rendered through the model's template exactly as
      `sldb docs create` renders it, in UTF-8.
  - `track`: only for a `document` source, where it defaults to true: the written file is
    tracked under the declared model and name (`track_document_file`), which also lists it in
    `include` as any tracking does. `track: true` on a `text` or `file` seed is refused.

`Seed` carries `extra="forbid"`: an unknown key fails `load_declaration` with pydantic's
`ValidationError`, whose location names the key. The invariants (one source, the document's
three keys, `track` only with a document) are validators of the model, so a declaration that
breaks them is refused wherever it is loaded.

## `sldb.api.scaffold_store`

```python
scaffold_store(store, *, declaration=None, apply=False, template_root=None) -> ScaffoldReport
```

- `store`: the `.sldb` directory or its project, or `None` for the nearest declared store.
- `declaration`: a `StoreDeclaration` (its `folders` and `seeds`) given in process, used
  **instead of** `store.yaml`'s keys and never written to it. A consumer can declare its seeds
  in its own package and keep its `store.yaml` as it is; a relative `file:` then needs
  `template_root` to point at the package's templates (or uses `pkg:`).
- `apply`: without it nothing is written and the report says what a run with it would do.

`ScaffoldReport` (`src/sldb/api/stores/scaffold_report.py`) has four lists of project-relative
paths, folders first and then seeds in declaration order, plus `applied`:

| list | without `apply` | with `apply` |
|---|---|---|
| `created` | missing, would be created | created |
| `rewritten` | a `managed` file whose bytes differ, would be restored | restored |
| `present` | exists as declared (`if_missing`: exists at all) | the same |
| `conflicts` | a folder path held by a file, a file path held by a directory, or a path under an ancestor that is a file | the same, never touched |

A `managed` document seed that is rewritten and tracked is untracked and tracked again, so its
entry follows the new bytes. The scaffold is idempotent: a second run with `apply` over the
same declaration changes nothing and reports everything as `present`.

The writes happen inside `sldb.api.transaction` (`docs/architecture/transactions.md`):
`write_file` for every seed and `track` for a tracked document, so a failure halfway (a
template that cannot be read, a name already tracked) leaves every file written before it as it
was. Folders are created with `mkdir(parents=True)` before the seeds that need them; a
directory created in a run that then rolls back stays, empty.

## `sldb.api.build_store`

```python
build_store(store, *, apply=True, generate=None) -> dict
```

`sldb stores build` was `cli/commands/stores_build.py`'s function; it is now an API function
(`src/sldb/api/stores/build_store.py`) with `root = project_root` of `declared_store(store)`.
With `apply=True` it is exactly the build of before (links, models, predicates, the declared
files, the generators, the files they wrote, the indexes, `undeclared` and `missing`) followed
by `scaffold_store(apply=True)`, in one report whose only new key is `scaffold`: the dump of
the four lists, without `applied` (a build always applies). The generators are sldb commands
run by the CLI, and `sldb.api` does not import `sldb.cli`, so the CLI hands them in as
`generate(store, root, declaration) -> list[str]` (`run_generators`); with `generate=None`
no generator runs and `generated` is `[]`.

With `apply=False` nothing is written: `links`, `models`, `tracked` and `generated` come back
empty and `predicates_changed` false, while `scaffold` (not applied), `undeclared` and
`missing` say what is pending.

## CLI

- `sldb stores scaffold [--store PATH] [--apply] [--format text|json|yaml]`: the report above;
  text form `scaffolded: created: n, rewritten: n, present: n, conflicts: n` (or `scaffold
  pending: ...` without `--apply`), listing the conflicts. Exit 1 when there is a conflict.
  With `--envelope`, the report is the envelope's `data`.
- `sldb stores build`: unchanged in its keys, text summary and exit code; its JSON and YAML
  output gains the `scaffold` section, always present, `{created: [], rewritten: [], present: [],
  conflicts: []}` when the declaration has no folders or seeds.
