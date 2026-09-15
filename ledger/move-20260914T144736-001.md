---
id: move-20260914T144736-001
at: '2026-09-14T14:47:36+00:00'
speaker: ''
outcome: unico
state_before: libre
state_after: libre
hash_before: 28ffb2d24d7afe126249cdfb4e4ca20719f88e5c31f67f5c34182199e3853f6e
hash_after: 28ffb2d24d7afe126249cdfb4e4ca20719f88e5c31f67f5c34182199e3853f6e
refers_to: ''
---

# move-20260914T144736-001

## Sentence

what python symbols references CommandRecord

## Record

```yaml
queries:
- pron graph python_symbol → 1
- kgdb edges_to(python:sldb.sldb.selfdoc.command:CommandRecord, references) → 0
writes: []
edges: []
interpretation:
  forma: read
  items:
  - wh('what')
  - word('python symbols'→source_model:PythonSymbol)
  - word('references'→field:TaskDoc.references,source_relation:references)
  - unknown('CommandRecord')
  parts:
  - 'read · source_relation:references · subject=all PythonSymbol [] · object=the
    PythonSymbol [] CommandRecord · payload={''asked'': ''subject''}'
  unknown: []
  notes: []
reads: []
trace:
- 'interpretation: read'
- pron graph python_symbol → 1
- kgdb edges_to(python:sldb.sldb.selfdoc.command:CommandRecord, references) → 0
```
