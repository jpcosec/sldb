---
sldb:
  by: agent
  at: '2026-11-19T12:42:09Z'
  authority: generated
  via: create_document
id: atom-los-hallazgos-builtin-tag-namespace-traen-un-fix-accionable
title: Los hallazgos builtin tag_namespace traen un fix accionable
five_wh_one_plus: how
tags:
- system:sldb
- topic:tags
---

# Los hallazgos builtin tag_namespace traen un fix accionable

## Answer

Cada hallazgo de la familia builtin:tag_namespace:* (sldb rules check, sldb tags check) lleva en fix qué hacer. Si el namespace del tag no está declarado: declararlo en tag_namespaces de .sldb/store.yaml (name, hierarchical, folder_axis, anchored_by). Si está declarado y el tag no es válido: usar uno de los tags de ese namespace. Lo arma _finding en src/sldb/api/rules/builtin_tag_findings.py a partir del namespace del hallazgo.
