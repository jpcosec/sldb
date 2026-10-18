---
id: python-sldb-sldb-sldb-cli-serve-health-_findings
system: sldb
module: sldb.sldb.cli.serve.health
qualname: _findings
kind: FunctionDef
source_path: sldb/cli/serve/health.py
source_span: '23:34'
source_sha256: cfacc306a5be70f7699f1f17325771fd971ff01579a2b4cabd8fd83dd0aa9432
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.cli.serve.health:_findings; contract-sha256:76994f799180ecc9fec35950342ed11fb8f243b269b81285393fb0a7179d7fc7
---

# _findings

## Signature

_findings(report: dict[str, Any])

## Docstring

The findings and the action — empty when the store is clean.

A finding that needs a decision outranks any safe command: the index holds the only record
of the value a reindex would overwrite, so it must not be offered as the next step.

## Imports

["__future__", "pathlib", "typing"]

## Purpose

Not documented.

## Architecture

Not documented.
