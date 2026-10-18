# Archived branches

The old branches were deleted on 2026-10-18 after their content was checked against main.
None of them held code that main lacks and still wants; each one with commits of its own is
kept as an `archive/*` tag (on origin too), so nothing is lost:

```bash
git show archive/refactor-target:docs/v2/02-sustrato-computacional.md
git log --oneline main..archive/refactor-target
```

| Tag | Was | What it holds | Why it is not in main |
|---|---|---|---|
| `archive/refactor-target` | `refactor-target` (0dc8c04; `origin/refactor-target` is its ancestor) | A rewrite of sldb, first in Rust/PyO3, then as a Clojure/Babashka kernel ("v2 SMG node pool": content-addressed nodes, trees, revisions, CAS heads) under `src/sldb/kernel`, plus its specs in `docs/v2/` | Another product direction in another language; main is the Python package |
| `archive/refactor-target-rustflavor` | `refactor-target-rustflavor` (323295c) | The Rust kernel PoC (a Lisp/EDN evaluator over `petgraph`) and `WHY_NOT_RUST.md`; its other 44 commits are in `archive/refactor-target` | Abandoned by its author (below) |
| `archive/fix-composition-anchoring` | `fix/composition-anchoring` (b3f5cc4) | WIP: composition refs anchored to the project root, and `composition_issues` reporting broken children | Anchoring landed in main another way (`ref_root`, 8264b8a); the reporting did not |
| (none) | `iso-lab/sldb` (b731803) | A progress note on the store-extraction task | Brought into the task itself (`desk/drawer/tasks/task-extract-store-into-generic-typed-document-engine-document-codec-plugins.md`), re-checked against main |
| (none) | `origin/fix/transclusion-frontmatter-anchors`, `origin/refactor` | — | Already merged |

## Worth reading before revisiting an idea

- **The v2 substrate.** `docs/v2/02-sustrato-computacional.md` (the node pool, revisions and
  replay-verified open), `04-superficie-markdown.md` (a language-agnostic spec of the Markdown
  surface: CST, AST, escapes, plan, report), `05-estado.md` (inventory and decisions) and
  `tests/promises.md` (promise-to-test traceability), all in `archive/refactor-target`.
- **Why not Rust** (`WHY_NOT_RUST.md` in `archive/refactor-target-rustflavor`): rebuilding
  immutable maps, EDN, STM, Datalog and macros in Rust would cost months before adding value,
  and Clojure has them natively; Babashka removes the JVM start-up cost for a CLI. The kernel
  was to pivot to Clojure/Babashka + DataScript. Main later stayed with Python.
- **Broken composition children are still silent.** A composed field whose child is missing,
  does not extract, or does not fit the item template renders as empty text, and nothing
  reports it. The archived WIP collected them in `composition_issues`; its code predates
  `ref_root` and would need rewriting.
