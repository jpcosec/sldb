---
id: python-sldb-sldb-selfdoc-report-documentationreport
system: sldb
module: sldb.selfdoc.report
qualname: DocumentationReport
kind: ClassDef
source_path: sldb/selfdoc/report.py
source_span: '17:49'
source_sha256: de02f24e9af7f6087fc62441c20ddc2346f536fd82b859fd51c26518c5873b89
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.selfdoc.report:DocumentationReport; contract-sha256:eb2517eacb61804480430537c0c40beca7b42f70286a1082bda1190dd50048e0
---

# DocumentationReport

## Signature

Not applicable.

## Docstring

---
id: sldb.selfdoc.report.DocumentationReport
kind: core
tags: [type:code.symbol]

---
Report drift between parser-derived plans, files, and store tracking.

``inspect_documents`` fills the findings and the CLI prints them as JSON;
``ok`` controls CLI check/sync exit status, but the Python variants currently
return zero even when the JSON reports false. Removed documents are retained;
rename candidates are heuristic hints without a uniqueness guarantee.
``ok`` means none of the checked freshness findings were populated. It ignores
``semantic_gaps``, which counts authored placeholders, and does not establish
semantic completeness, docstring quality, or complete removal detection.

## Imports

["__future__", "pydantic"]

## Purpose

Not documented.

## Architecture

Not documented.
