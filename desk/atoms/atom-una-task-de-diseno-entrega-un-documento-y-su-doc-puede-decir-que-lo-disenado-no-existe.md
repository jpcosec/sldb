---
id: atom-una-task-de-diseno-entrega-un-documento-y-su-doc-puede-decir-que-lo-disenado-no-existe
title: Una task de diseno entrega un documento, y su doc puede decir que lo disenado
  no existe
five_wh_one_plus: how_not
tags:
- system:sldb
- system:deskops
- topic:workflow
- topic:drift
- topic:documentation
provenance: docs/composition_modes.md
---

# Una task de diseno entrega un documento, y su doc puede decir que lo disenado no existe

## Answer

Leer 'task completed' junto a su doc de salida diciendo 'were proposals … not advertised as supported operations in this checkout' parece una contradiccion de estado, pero no lo es: la task era de diseno y su entregable ERA el documento de diseno, no la implementacion. El commit 9411866 'Implement task-expand-sldb-composition-modes' agrego docs/composition_modes.md con cuatro modos propuestos; un mes despues, otro commit (1b04515e) reescribio el encabezado de ese mismo archivo para distinguir lo implementado de lo propuesto. El archivo terminó conteniendo dos capas de tiempo sin marcarlas. El error de lectura es tratar el nombre del commit ('Implement task-X') como evidencia de que X quedo implementado, cuando solo dice que la task se ejecuto. Para una task de diseño, ejecutarla significa producir el diseño. La regla: antes de concluir que el desk miente, verificar que tipo de entregable prometia la task. Un doc de diseño que describe lo no-implementado esta cumpliendo su contrato, no contradiciendolo — pero necesita decir explicitamente cual de sus secciones es propuesta y cual es estado, o el proximo lector va a repetir la confusion.
