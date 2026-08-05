---
layer: shell
id: git-orchestration-in-python
title: Git orchestration in Python
five_wh_one_plus: why
tags:
- system:sldb
- domain:implementation-python-cli
provenance: source docs/architecture/target-system-overview.md
---

# Git orchestration in Python

Python remains responsible for the Git tracking logic (`GitIntegration` component inside `PythonCLI`). The `python_cli_layer` communicates directly with the `project_repo` to manage tracked documents, while deferring core parsing and store logic to Rust.

## Related atoms

### Implements
- [implements:: [[python-cli-orchestration-layer]]]

### Constrains
- [constrains:: [[graph-store]]]
