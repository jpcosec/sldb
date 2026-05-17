# Pattern: test the real CLI surfaces while shaping the workflow

ID: pill-002

## What

Use the documented and implemented SLDB CLI surfaces directly while shaping desk and docs workflows, instead of assuming the behavior from model design alone.

## Why

Desk is supposed to become a real SLDB routine, so hidden mismatches only show up when the actual commands are used for create, track, update, validate, composition, and retrieval flows.

## When

Apply this pill during capability audits, docs modeling, and any workflow experiment meant to prove that SLDB can operate on its own scaffolding.

## Where

Applies to `README.md`, `src/sldb/cli/commands/`, `desk/tasks/`, and the future `docs/` modeling work.

## How

Prefer exercising the CLI end to end: add models, create or track documents, update them, validate them, and query them through structural, section, semantic, and composition-oriented commands.

## How Not

Do not stop at static model design. Do not assume a command is usable just because it exists in code or docs.

## Tags

- system:sldb
- workspace:desk
- topic:cli
- topic:validation
