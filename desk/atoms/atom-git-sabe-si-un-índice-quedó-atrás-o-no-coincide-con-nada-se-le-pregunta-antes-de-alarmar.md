---
id: atom-git-sabe-si-un-índice-quedó-atrás-o-no-coincide-con-nada-se-le-pregunta-antes-de-alarmar
title: 'Git sabe si un índice quedó atrás o no coincide con nada: se le pregunta antes
  de alarmar'
five_wh_one_plus: how
tags:
- system:sldb
---

# Git sabe si un índice quedó atrás o no coincide con nada: se le pregunta antes de alarmar

## Answer

Cuando el texto de un documento no coincide con su índice, buscar el hash indexado entre las versiones commiteadas del archivo (git log --follow, git show commit:path) separa lo pendiente del daño: si coincide con una versión anterior, el índice quedó atrás y basta stores update; si ninguna coincide, es una edición indexada sin commitear o daño, y vale mirarlo. No se puede llamar corrupto con certeza: un índice escrito desde el working tree sin commit tampoco está en la historia. Ver src/sldb/store/diagnostics_models/text_history.py.
