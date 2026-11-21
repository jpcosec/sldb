# Current CLI Tree

Verified from `src/sldb/cli/parsers/` on 2026-09-13. This lists public command paths; use `sldb <command> --help` for arguments and defaults.

```text
sldb
├── help [topic]
├── faq [question]
├── extract / render / validate
├── init / example
├── stores
│   └── init / add / check / update / semantic-map / semantic-export / list / build / declare / merge-driver / migrate-hashes / migrate-layout / rebuild-index / reconcile / remove / scaffold
├── models
│   ├── add / update / list / show / validate / create / check / inherit / remove
│   ├── metadata edit
│   ├── template show / edit
│   └── fields add / remove
├── predicates
│   └── add / list / show / validate / remove / export / sync
├── docs
│   └── create / track / update / untrack / delete / show / recover / list / compose / explore / exists / history / replace / select
├── fields
│   └── show / query / create / update / remove / append / clean
├── sections
│   └── show / find / fields
├── find
├── ast
│   └── show / schema
├── explore / inbox / lint
├── serve
├── anchors
│   └── check / record
├── bench
├── edges
│   └── init / rebuild / check / show / referrers / rewrite / unresolved
├── graph
│   ├── list / get / query / similar / central / components / cycles / neighborhood / order / path / ingest-sldb
│   ├── project edges / nodes / missing
│   └── snapshot save / load
├── journal
│   └── show / verify
├── mcp
├── move
├── notations
│   └── list / resolve / sync / validate / view / from-graph
├── rules
│   └── check / explain
├── semantic
│   ├── show
│   ├── equivalent add
│   └── parent add / remove
├── tags
│   └── check / namespaces / tree
├── views
│   └── list / run
├── selfdoc
│   └── scan / sync / check / python-scan / python-sync / python-check
└── legacy
    └── ls / get / glob / find / compose / recover
```

## Command Groups

- Direct model workflows: `extract`, `render`, `validate`; no store required.
- Store workflows: `stores`, `models`, `predicates`, `docs`, `fields`, `sections`, `find`, `ast show`.
- Structural inspection: [AST/IR CLI queries](../ast_query_primitives.md).
- HTTP access: `serve --store PATH --pythonpath PATH`, default `127.0.0.1:8787`; optional `--cors`.
- Onboarding and source search: `help`, `faq`, `explore`. FAQ and explore paths are working-directory-relative, not store-anchored.
- Bootstrap and maintenance: `init`, `example`, `inbox`, `lint`.
- Code-derived CLI reference: `selfdoc scan|sync|check`; see [self-documentation](../self-documentation.md).
- Raw address queries: `legacy`; see [addressability](../addressability_model.md).

Singular aliases and old top-level address commands remain compatibility entry points. They are not the recommended surface, and there is no confirmed future removal release for this frozen checkout.

The HTTP implementation exposes `GET /health`, `/schema`, `/graph`, `/semantic-export`, and `POST /save`; it does not expose every CLI command as an HTTP route.
