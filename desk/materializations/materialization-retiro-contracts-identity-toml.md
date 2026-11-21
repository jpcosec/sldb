---
sldb:
  by: agent
  at: '2026-11-21T07:29:50Z'
  authority: generated
  via: create_document
id: materialization-retiro-contracts-identity-toml
title: retiro contracts-identity-toml
source_atoms:
- atom-la-arquitectura-de-spec2viz-en-sldb-ya-no-nombra-a-spec2viz-como-consumidor-ni-lo-invoca
target_kind: config
target_identity: contracts/identity.toml
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/notations
tags:
- system:sldb
- topic:retiro
---

# retiro contracts-identity-toml

## Intent

materializa en contracts/identity.toml el atom atom-la-arquitectura-de-spec2viz-en-sldb-ya-no-nombra-a-spec2viz-como-consumidor-ni-lo-invoca
