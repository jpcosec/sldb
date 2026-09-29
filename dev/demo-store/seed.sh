set -e
S="--store .sldb --pythonpath ."
sldb stores init --path . >/dev/null
for m in NotaDoc DecisionDoc AcuerdosDoc; do sldb models add models:$m $S >/dev/null; done
mkdir -p data
cat > data/sap.yaml <<'Y'
status: aceptada
owner: Patricia
title: "MEPU: integración vía archivos planos, sin conexión directa a SAP"
system: MEPU
context: El área de seguridad TI del cliente no permite una conexión directa a SAP.
decision: |-
  La integración se hace con **archivos planos** depositados en un directorio compartido.

  - SAP los recoge en su ciclo batch.
  - Los PDFs quedan en carpetas `aceptadas/` y `rechazadas/`.
tags: [constraint:it-security, system:sap]
alternatives:
  - {opcion: API directa, motivo: Bloqueada por seguridad TI}
  - {opcion: Middleware externo, motivo: Costo de licencia}
Y
cat > data/semaforo.yaml <<'Y'
status: propuesta
owner: Patricia
review: "2026-10-12"
title: Semáforo de vencimiento a 3 días
system: MEPU
context: En la reunión del 12 se habló de un semáforo para órdenes por vencer.
decision: Una orden pasa a **amarillo** 3 días hábiles antes de su vencimiento y a *rojo* el día del vencimiento.
tags: [rule:sla]
alternatives: []
Y
cat > data/acuerdos.yaml <<'Y'
title: Acuerdos y decisiones MEPU
intro: Documento compuesto a partir de decisiones individuales. Editar una decisión la cambia aquí y en todo documento que la cite.
decisiones: [docs/decisiones/sap.md, docs/decisiones/semaforo.md]
Y
cat > data/nota.yaml <<'Y'
body: |-
  # Notas de la reunión del 12

  Hablamos del **semáforo de vencimiento**. Quedó en 3 días, pero hay que confirmarlo con Patricia.

  - Revisar stock antes de aceptar.
  - Pendiente: formato de los archivos planos.
Y
sldb docs create --model DecisionDoc -o docs/decisiones/sap.md data/sap.yaml $S
sldb docs create --model DecisionDoc -o docs/decisiones/semaforo.md data/semaforo.yaml $S
sldb docs create --model AcuerdosDoc -o docs/acuerdos.md data/acuerdos.yaml $S
sldb docs create --model NotaDoc -o docs/notas/reunion-12.md data/nota.yaml $S
