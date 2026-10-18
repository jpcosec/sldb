---
id: python-sldb-sldb-selfdoc-report-documentationreport
system: sldb
module: sldb.selfdoc.report
qualname: DocumentationReport
kind: ClassDef
source_path: sldb/selfdoc/report.py
source_span: '17:50'
source_sha256: 5e38a8833913c59f78b7c4623a6642d7c1362582b5f128050fccd513449aaca3
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.selfdoc.report:DocumentationReport; contract-sha256:4d9ba8b2704fd2dab16ef37bae6af4dd5fa7872dc84db368a77b42ab582dd5f6
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
