---
id: atom-el-desk-puede-afirmar-lo-contrario-del-repo-y-nada-falla
title: El desk puede afirmar lo contrario del repo y nada falla
five_wh_one_plus: how_not
tags:
- system:sldb
- system:deskops
- topic:drift
- topic:self-documentation
- topic:diagnostics
provenance: runs/subagents/reconcile-legacy-retirement-20260929/result-summary.md
---

# El desk puede afirmar lo contrario del repo y nada falla

## Answer

El estado de una task en desk/ y el estado real del repo son dos afirmaciones independientes, y nada las compara. Tres casos simultaneos, verificados en un mismo dia en sldb: tres tasks en status draft cuyo codigo ya estaba borrado y commiteado (d0df139, 6389d55, e17abfe); una task en current_node completed cuyo propio doc de salida (docs/composition_modes.md:42) dice que el trabajo 'were proposals, not advertised as supported operations in this checkout'; y el manual describiendo en secciones 13 y 14 tres limitaciones ya resueltas en el codigo. La causa no es olvido: el trabajo se hace y se commitea, pero mover el estado del desk es un paso separado que ningun gate exige. El costo no es cosmetico. Un lector del desk planifica trabajo ya hecho, y un lector del manual construye workarounds para problemas que no existen. La regla: si un artefacto del desk afirma algo verificable contra el repo, esa afirmacion necesita un chequeo ejecutable que falle, porque una afirmacion que nadie verifica deriva en silencio y es peor que no afirmar nada.
