# Audit SLDB capabilities for desk and docs workflow

ID: task-002
Status: active

## Goal

Audit the current SLDB feature set needed for desk self-hosting and `docs/` onboarding, and record any missing capability as explicit follow-up tasks in `desk/tasks/`.

## Scope

In scope: model creation, doc creation, doc tracking, doc updates, validation, section access, semantic access, and composition/recovery-related commands. Out of scope: implementing all missing capabilities immediately.

## References

- `README.md`
- `src/sldb/cli/commands/`
- `desk/tasks/`

## Dependencies

- none

## Pills

- pill-001

## Files

- `README.md`
- `src/sldb/cli/commands/`
- `desk/tasks/`
- `desk/contexts/`

## Implementation Path

Review the documented and implemented CLI surfaces, compare them with the intended desk workflow, test the critical paths, and open new desk tasks for any gap or friction discovered.

## Validation

- verify command coverage against `README.md`
- note unsupported or unclear workflows as task docs
- exercise semantic, structural, and composition-oriented commands

## Done When

The missing-capability list has been converted into explicit desk tasks and the required SLDB surfaces for the next phase are understood well enough to execute them.

## Tags

- system:sldb
- workspace:desk
- topic:capability-audit
- topic:cli
