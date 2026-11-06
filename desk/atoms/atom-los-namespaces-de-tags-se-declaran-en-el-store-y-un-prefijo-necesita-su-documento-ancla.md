---
id: atom-los-namespaces-de-tags-se-declaran-en-el-store-y-un-prefijo-necesita-su-documento-ancla
title: Los namespaces de tags se declaran en el store y un prefijo necesita su documento
  ancla
five_wh_one_plus: what
tags:
- system:sldb
- topic:tags
- topic:rules
provenance: docs/architecture/tags.md
---

# Los namespaces de tags se declaran en el store y un prefijo necesita su documento ancla

## Answer

Un store de sldb declara sus namespaces de tags en store.yaml (tag_namespaces: name, hierarchical, folder_axis y anchored_by {model, field}). En un namespace jerárquico con anchored_by, cada prefijo a.b de un tag usado necesita un documento ancla del modelo declarado cuyo campo vale ese prefijo. Esa invariante cruza documentos, así que no es un validador de un modelo: corre como una familia de reglas incorporada (builtin:tag_namespace:<name>) dentro de la evaluación de reglas de sldb (on_write en save, transaction.update, apply_batch, /save y replace_text; stores check; rules check y rules explain), con los mismos findings que una RuleDoc. sldb.api da tag_tree, tag_folder, tag_check y tag_namespaces, y la CLI sldb tags namespaces|tree|check. sldb.api.replace_text y sldb docs replace reemplazan texto con conteo exacto dentro de una transacción. Implementado en GD27 (plan generalizar-desde-deskops).
