# Current CLI Tree

Verified from `src/sldb/cli/parsers/` on 2026-09-13. This lists public command paths; use `sldb <command> --help` for arguments and defaults.

```text
sldb
├── help [topic]
├── faq [question]
├── extract / render / validate
├── init / example
├── stores
│   └── init / add / check / update / semantic-map / semantic-export / list
├── models
│   ├── add / update / list / show / validate / create
│   ├── template show / edit
│   └── fields add / remove
├── predicates
│   └── add / list / show / validate / remove
├── docs
│   └── create / track / update / untrack / delete / show / recover / list / compose / explore
├── fields
│   └── show / query / create / update / remove / append / clean
├── sections
│   └── show / find / fields
├── find
├── ast
│   └── show / schema
├── explore / inbox / lint
├── serve
├── selfdoc
│   └── scan / sync / check
└── legacy
    └── ls / get / glob / find
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

The HTTP implementation exposes `GET /health`, `/schema`, `/graph`, `/kgdb/snapshot`, and `POST /save`; it does not expose every CLI command as an HTTP route.
