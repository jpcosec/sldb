# Pills

Pills are the reusable context documents of the desk routine.

They are temporary in the workspace but durable in git history.

## Base Shape

Pills currently use the base `PillDoc` model in `desk/models/pill.py`.

Required fields:

- `title`
- `id`
- `what`
- `why`
- `when`
- `where`
- `how`
- `how_not`
- `tags`

## Notes

- Task-to-pill binding lives in task documents, not in pills.
- The semantic cue that might later become a dedicated model kind lives in the title for now, for example `ADR: ...` or `Pattern: ...`.
- Tags go at the end and should use namespaced forms such as `language:python`, `library:pydantic`, or `system:sldb`.
- `where` may be either a general applicability description or a reference to already existing code or docs.
- A pill can be deleted once it is no longer needed in the active workspace; reuse remains available through git history.
