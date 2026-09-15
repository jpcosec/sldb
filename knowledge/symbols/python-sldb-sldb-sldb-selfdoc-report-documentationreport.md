---
id: python-sldb-sldb-sldb-selfdoc-report-documentationreport
system: sldb
module: sldb.sldb.selfdoc.report
qualname: DocumentationReport
kind: ClassDef
source_path: sldb/selfdoc/report.py
source_span: '17:49'
source_sha256: 5d8bd5eb6eff43620b77491acf873c4b69d6920bc69ad1f49d415ddf25209ec4
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.sldb.selfdoc.report:DocumentationReport; contract-sha256:90bb755c380b7dd39f3ec73b76102d2b768a2042a1585a4b32e31f66fb58bae2
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
