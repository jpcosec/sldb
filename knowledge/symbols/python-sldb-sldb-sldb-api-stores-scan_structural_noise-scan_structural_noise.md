---
id: python-sldb-sldb-sldb-api-stores-scan_structural_noise-scan_structural_noise
system: sldb
module: sldb.sldb.api.stores.scan_structural_noise
qualname: scan_structural_noise
kind: FunctionDef
source_path: sldb/api/stores/scan_structural_noise.py
source_span: '17:33'
source_sha256: 4fb76c8d1a457f198fca131fd919507328ceee7eedd4cdb1bc0d39179d13b2d2
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.api.stores.scan_structural_noise:scan_structural_noise;
  contract-sha256:ba7fb317a125abb0baa0a8a32ae07d8b450eea408599db2d05e5c26587569376
---

# scan_structural_noise

## Signature

scan_structural_noise(store_path: Path, project_root: Path, pythonpath: str | None=None)

## Docstring

Every tracked document carrying headings its model does not declare.

Args:
    store_path: The `.sldb` directory to scan.
    project_root: The root the documents' paths are relative to.
    pythonpath: Directory to import the model modules from.

Returns:
    One report per noisy document, in store order; empty when the store is clean.

## Imports

["__future__", "pathlib", "sldb.api.documents.structural_noise", "sldb.api.documents.structural_noise_report"]

## Purpose

Not documented.

## Architecture

Not documented.
