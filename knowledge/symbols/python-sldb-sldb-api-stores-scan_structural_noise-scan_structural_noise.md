---
id: python-sldb-sldb-api-stores-scan_structural_noise-scan_structural_noise
system: sldb
module: sldb.api.stores.scan_structural_noise
qualname: scan_structural_noise
kind: FunctionDef
source_path: sldb/api/stores/scan_structural_noise.py
source_span: '17:37'
source_sha256: c74b37a6c0124e40b4033277d492ecf173b51e9a2d53f7927388c7b5fac2af42
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.api.stores.scan_structural_noise:scan_structural_noise;
  contract-sha256:ae0e7131a809ba8d557b3f3286baa60cb7bd5cbaf0485d5e256f47e6ff2a974d
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

Every tracked document carrying headings its model does not declare.

## Architecture

Not documented.
