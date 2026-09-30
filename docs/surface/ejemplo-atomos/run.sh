#!/usr/bin/env bash
# Reproduce el ejemplo de OPERACIONALIZACION-VISTAS.md en un directorio temporal.
# Uso: bash run.sh   (desde cualquier lado; usa el sldb de este worktree)
set -e
HERE="$(cd "$(dirname "$0")" && pwd)"
export PYTHONPATH="$HERE/../../../src:$HERE"
W="$(mktemp -d)"; cd "$W"; mkdir docs data; cp "$HERE/models.py" .
S="--store .sldb --pythonpath ."
sl() { python -m sldb "$@"; }

BODY='Se decidió reemplazar el lote nocturno por una cola de eventos. Tomás queda a cargo de la migración. Riesgo principal: si la cola se satura en los cierres de mes, los documentos podrían volver a acumularse.'
python - "$BODY" <<'P'
import sys, yaml
body = sys.argv[1]
yaml.safe_dump({"title": "Acta 2026-09-14", "body": body}, open("data/acta.yaml", "w"), allow_unicode=True)
atoms = {"a3": ("decision", "Reemplazar el lote nocturno por una cola de eventos", "Se decidió reemplazar el lote nocturno por una cola de eventos", "confirmado"),
         "a4": ("hecho", "Tomás lidera la migración a la cola", "Tomás queda a cargo de la migración", "propuesto"),
         "a10": ("riesgo", "La cola podría saturarse en los cierres de mes", "si la cola se satura en los cierres de mes", "propuesto")}
for k, (kind, text, q, st) in atoms.items():
    i = body.index(q)
    yaml.safe_dump({"kind": kind, "status": st, "source": "ActaDoc:acta", "start": i, "end": i + len(q), "tags": ["infra.ingesta"], "text": text, "quote": q}, open(f"data/{k}.yaml", "w"), allow_unicode=True)
def rt(n, desc, card="many_to_many"):
    yaml.safe_dump({"title": n, "name": n, "direction": "directed", "cardinality": card, "axis": "WHY", "source_types": ["AtomDoc"], "target_types": ["AtomDoc"], "condition": "", "description": desc}, open(f"data/rt-{n}.yaml", "w"))
rt("motiva", "El origen explica la razon del destino."); rt("responsable_de", "Responde por la decision.", "many_to_one"); rt("afecta", "El riesgo afecta al destino.")
def rel(n, s, t, ty): yaml.safe_dump({"title": n, "source_id": s, "target_id": t, "relation_type": ty, "condition": "", "notes": ""}, open(f"data/r-{n}.yaml", "w"))
rel("r3", "AtomDoc:a4", "AtomDoc:a3", "responsable_de"); rel("r6", "AtomDoc:a10", "AtomDoc:a3", "afecta")
rel("rbad", "AtomDoc:a4", "ActaDoc:acta", "motiva")  # invalida a proposito: el destino no es un atomo
yaml.safe_dump({"title": "Informe de avance", "decisiones": ["docs/a3.md"]}, open("data/inf.yaml", "w"))
P

sl stores init --path . >/dev/null
for m in ActaDoc AtomDoc InformeDoc; do sl models add models:$m $S >/dev/null; done
sl edges init $S >/dev/null
sl docs create --model ActaDoc -o docs/acta.md data/acta.yaml $S >/dev/null
for a in a3 a4 a10; do sl docs create --model AtomDoc -o docs/$a.md data/$a.yaml $S >/dev/null; done
for n in motiva responsable_de afecta; do sl docs create --model RelationTypeDoc -o docs/rt-$n.md data/rt-$n.yaml $S >/dev/null; done
for n in r3 r6 rbad; do sl docs create --model RelationDoc -o docs/r-$n.md data/r-$n.yaml $S >/dev/null; done
sl docs create --model InformeDoc -o docs/inf.md data/inf.yaml $S >/dev/null

echo "== bandeja: atomos propuestos";   sl find "" --type doc --where 'status = "propuesto"' $S 2>/dev/null
echo "== confirmar a4";                 sl fields update docs/a4/status '"confirmado"' $S
echo "== relaciones validadas (la mala debe fallar)"; sl edges check --store .sldb || true
echo "== informe compuesto";            cat docs/inf.md
echo "workdir: $W"
