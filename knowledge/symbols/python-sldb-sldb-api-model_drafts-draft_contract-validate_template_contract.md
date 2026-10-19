---
id: python-sldb-sldb-api-model_drafts-draft_contract-validate_template_contract
system: sldb
module: sldb.api.model_drafts.draft_contract
qualname: validate_template_contract
kind: FunctionDef
source_path: sldb/api/model_drafts/draft_contract.py
source_span: '14:25'
source_sha256: cdfab3afe477742eb73f4741b037686a43244112b11cdb81e61cfea80ef74714
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.api.model_drafts.draft_contract:validate_template_contract;
  contract-sha256:57e8dd18d243807d297b6da4af8481fc9a121766851b3d9047571ea04e135033
---

# validate_template_contract

## Signature

validate_template_contract(model_type: Any)

## Docstring

Refuse a model whose template markers name fields the model does not declare.

Raises:
    SLDBModelEditError: Listing the unknown field names.

## Imports

["__future__", "sldb.core.exceptions", "sldb.runtime.validation", "typing"]

## Purpose

Refuse a model whose template markers name fields the model does not declare.

## Architecture

Not documented.
