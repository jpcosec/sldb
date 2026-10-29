---
# unclear | suggestion
kind: unclear
# e.g., other_repo
sender_project: deskops
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-10-21T03:36:35'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# Linked store path references cannot resolve despite tracked targets

_Describe the incoming message with enough evidence to triage._

While resolving MEPU reports in deskops, reproduced sldb edges unresolved showing the 11 Board pills/ritual paths as unknown_path only through a linked store. All targets exist and are tracked; local edges unresolved is empty. Root cause: declared_resolution._resolve only uses owners when store is None; composition_targets._owners_by_path excludes linked docs. Expected: resolve relative paths within the source store namespace, preserving isolation when consumer/provider paths collide. Reproduction without MEPU: compose deskops .sldb as linked alias deskops and inspect source deskops:BoardDoc:Board. Deskops will use existing supported bare tracked document names for its Board pills/rituals, with federation regression tests; no SLDB runtime workaround planned.
