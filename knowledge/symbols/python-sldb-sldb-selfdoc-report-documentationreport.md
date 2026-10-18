---
id: python-sldb-sldb-selfdoc-report-documentationreport
system: sldb
module: sldb.selfdoc.report
qualname: DocumentationReport
kind: ClassDef
source_path: sldb/selfdoc/report.py
source_span: '17:54'
source_sha256: eae33ef265d0d143767e30db35cf9ca0fcecaee519a93ae001af8591a70d15b3
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.selfdoc.report:DocumentationReport; contract-sha256:039d101228847073aad2dc19de78b9cfb84d2d4bb0398eb55a6d13eeaba9975a
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

Report drift between parser-derived plans, files, and store tracking.

## Architecture

Not documented.
