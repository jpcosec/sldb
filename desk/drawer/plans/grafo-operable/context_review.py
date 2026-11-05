"""Cheap isolated context reviews for this plan, under ritual-context-review.

Governed copy of the driver used for the eight plan-level rounds of 2026-11-04 (it lived in
/tmp then; the owner asked for it to be governed here). It launches one fresh Pi process per
node and attempt and writes the evidence the ritual asks for under
runs/subagents/<run>/context-review/<node>/<input sha256>/attempt-N/ (input.md, manifest.json,
output.md, stderr.log, receipt.json). Dispositions are written by hand next to each output.

Modes:
  node [IDS...]            review plan nodes (dag.yaml contract + neighbours + gates)
  preflight TASKDOC NODE   TaskDoc-only preflight before dispatch (the TaskDoc is the whole input)
  bundle TASKDOC NODE      cold-bundle: TaskDoc + plan sources + node contract + files it names
  status                   compare current inputs with recorded reviews; no model call

Caps (owner, 2026-11-04: "8 rondas igual es excesivo"): a node is not reviewed again when its
input is unchanged; --max-attempts (default 2) refuses a third attempt on the same node unless
--force. Rounds beyond two at plan level are not run by this driver.
"""
from __future__ import annotations

import argparse
import concurrent.futures
import datetime
import hashlib
import json
import subprocess
import sys
from pathlib import Path

import yaml

B = Path(__file__).resolve().parent            # the plan directory
ROOT = B.parents[3]                            # the sldb repo root
PLAN = B.relative_to(ROOT)
RUN = ROOT / 'runs/subagents/20261104-grafo-operable-context-reviews/context-review'
TIMEOUT = 600
SYSTEM = (
    'Revisor barato aislado de un encargo de planificación. Trabajas solo con el input explícito: '
    'sin herramientas, historial ni otras fuentes. No ejecutas nada. Responde en español con estas '
    'secciones exactas: REFORMULACION (propósito, resultado, repo, límites), AMBIGUEDADES (numeradas, '
    'cada una con cita textual del input y qué obligaría a inventar; escribe "ninguna" si no hay), '
    'DRY-RUN (lecturas, cambios previstos, dependencias y validaciones futuras, sin ejecutar), '
    'FUTURO (lo que produce otro nodo o decide un humano, no ambigüedad). '
    'REFORMULACION describe el encargo del nodo, no esta revisión. DRY-RUN describe cómo lo ejecutaría '
    'un ejecutor futuro, hipotéticamente y sin ejecutar nada. Si el nodo es un agregado o paquete no '
    'ejecutable, dilo y además recorre cómo lo cumplen sus hijos, qué transfiere cada uno al siguiente '
    'y cómo se valida el resultado conjunto. Máximo 350 palabras.'
)
ARGV = ['pi', '--provider', 'deepseek', '--model', 'deepseek-flash', '--thinking', 'low', '--offline',
        '--no-session', '--no-context-files', '--no-skills', '--no-extensions', '--no-prompt-templates',
        '--no-tools', '--system-prompt', SYSTEM, '--print']
SELECTION = 'deepseek-flash: perfil barato verificado en esta máquina por ritual-context-review (D4)'
BASE = ['context-review-guide.md', 'brief.md', 'alcance.md', 'decisiones.md']
KEEP = ('id', 'title', 'kind', 'owner_repo', 'node_role', 'parent_id', 'children', 'scope', 'acceptance',
        'output_scope', 'depends_on', 'requires')

sha = lambda b: hashlib.sha256(b).hexdigest()
dump = lambda o: yaml.safe_dump(o, allow_unicode=True, sort_keys=False)


def load_dag() -> tuple[dict, dict]:
    d = yaml.safe_load((B / 'dag.yaml').read_text())
    nodes = {t['id']: t for t in d['tasks']}
    nodes.update({p['id']: p for p in d['hierarchy']['packages']})
    nodes[d['hierarchy']['root']['id']] = d['hierarchy']['root']
    return d, nodes


def contract(n: dict) -> dict:
    return {k: n[k] for k in KEEP if k in n}


def neighbours(d: dict, nodes: dict, n: dict) -> tuple[list, dict]:
    tasks = {t['id']: t for t in d['tasks']}
    pks = {p['id'] for p in d['hierarchy']['packages']}
    nid = n['id']
    if nid == 'ROOT':
        ids = list(n['children'])
    elif nid in pks:
        ids = list(n['children']); inside = set(ids)
        for c in ids[:]:
            ids += [x for x in tasks[c]['depends_on'] if x not in inside]
    else:
        ids = list(n['depends_on']) + [t['id'] for t in d['tasks'] if nid in t['depends_on']] + [n['parent_id']]
    ids = list(dict.fromkeys(i for i in ids if i != nid))
    gids = list(n.get('requires', [])) + [g for g, v in d['gates'].items() if v.get('produced_by') == nid]
    gids += [g for g in d['gates'] if g in str(contract(n))]
    return [nodes[i] for i in ids], {g: d['gates'][g] for g in dict.fromkeys(gids)}


class Bundle:
    def __init__(self) -> None:
        self.parts: list[str] = []
        self.records: list[dict] = []

    def add(self, label: str, text: str, projection: str) -> None:
        self.parts.append(f'FILE:{label}\n{text.rstrip()}\n')
        self.records.append({'path': label, 'sha256': sha(text.encode()), 'projection': projection})

    def close(self, instruction: str) -> bytes:
        self.parts.append(f'FILE:instruccion\n{instruction}\n')
        return ''.join(p + '\n' for p in self.parts).encode()


def node_bundle(d: dict, nodes: dict, n: dict) -> tuple[bytes, list]:
    b = Bundle()
    for rel in BASE:
        b.add(str(PLAN / rel), (B / rel).read_text(), 'whole_file')
    neigh, gates = neighbours(d, nodes, n)
    b.add(str(PLAN / 'dag.yaml') + f'#node:{n["id"]}', dump(contract(n)), 'node_contract')
    for m in neigh:
        b.add(str(PLAN / 'dag.yaml') + f'#edge:{m["id"]}', dump(contract(m)), 'edge_contract')
    if gates:
        b.add(str(PLAN / 'dag.yaml') + '#gates', dump(gates), 'gate_contracts')
    agg = n['id'] == 'ROOT' or n['id'].startswith('PK')
    text = (f'Revisa el nodo {n["id"]} siguiendo context-review-guide.md. '
            + ('Es un agregado: reformula el resultado sustantivo del paquete y da un DRY-RUN hipotético de sus hijos en orden, con entradas y salidas entre ellos y la validación conjunta. ' if agg else '')
            + 'Los bloques edge son contratos de vecinos; no los revises. No ejecutes nada.')
    return b.close(text), b.records


def preflight_bundle(taskdoc: Path, nid: str) -> tuple[bytes, list]:
    b = Bundle()
    b.add(str(taskdoc.resolve().relative_to(ROOT)), taskdoc.read_text(), 'whole_file')
    return b.close(f'Preflight solo-TaskDoc del nodo {nid}: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita y da el DRY-RUN. No ejecutes nada.'), b.records


def cold_bundle(d: dict, nodes: dict, taskdoc: Path, nid: str) -> tuple[bytes, list]:
    b = Bundle()
    b.add(str(taskdoc.resolve().relative_to(ROOT)), taskdoc.read_text(), 'whole_file')
    for rel in BASE:
        b.add(str(PLAN / rel), (B / rel).read_text(), 'whole_file')
    n = nodes[nid]
    b.add(str(PLAN / 'dag.yaml') + f'#node:{nid}', dump(contract(n)), 'node_contract')
    _, gates = neighbours(d, nodes, n)
    if gates:
        b.add(str(PLAN / 'dag.yaml') + '#gates', dump(gates), 'gate_contracts')
    payload = yaml.safe_load(taskdoc.read_text().split('---')[1]) if taskdoc.read_text().startswith('---') else {}
    for rel in (payload or {}).get('files') or []:
        f = ROOT / rel
        if f.is_file() and f.stat().st_size < 60_000:
            b.add(rel, f.read_text(errors='replace'), 'whole_file')
    return b.close(f'Cold-bundle del nodo {nid}: con el TaskDoc, las fuentes del plan, el contrato del nodo y los archivos que el TaskDoc nombra, reformula, lista ambigüedades con cita y da el DRY-RUN. No ejecutes nada.'), b.records


def attempt_dir(key: str, isha: str, max_attempts: int, force: bool) -> Path | None:
    base = RUN / key / isha
    if base.exists() and any(p.name.startswith('attempt-') for p in base.iterdir()):
        return None  # unchanged input: already reviewed
    done = sum(1 for p in (RUN / key).glob('*/attempt-*')) if (RUN / key).exists() else 0
    if done >= max_attempts and not force:
        raise SystemExit(f'{key}: {done} intentos ya; tope --max-attempts {max_attempts} (usa --force si el input cambió de verdad)')
    out = base / 'attempt-1'
    out.mkdir(parents=True)
    return out


def review(key: str, data: bytes, records: list, max_attempts: int, force: bool) -> tuple:
    isha = sha(data)
    out = attempt_dir(key, isha, max_attempts, force)
    if out is None:
        return key, 'unchanged', isha[:12]
    (out / 'input.md').write_bytes(data)
    start = datetime.datetime.now(datetime.timezone.utc).isoformat()
    p = subprocess.run(ARGV + [f'@{out / "input.md"}'], capture_output=True, text=True, timeout=TIMEOUT)
    (out / 'output.md').write_text(p.stdout)
    (out / 'stderr.log').write_text(p.stderr)
    (out / 'manifest.json').write_text(json.dumps({
        'key': key, 'input_sha256': isha, 'sources': records,
        'argv': ARGV[:-1] + ['--print', '@input.md'], 'model': 'deepseek/deepseek-flash',
        'profile': 'thinking low, offline, no tools/session/context/skills/extensions/prompt-templates',
        'selection_reason': SELECTION, 'started': start,
        'finished': datetime.datetime.now(datetime.timezone.utc).isoformat()}, indent=2, ensure_ascii=False))
    (out / 'receipt.json').write_text(json.dumps({
        'key': key, 'exit': p.returncode,
        'technical_ok': p.returncode == 0 and 'REFORMULACION' in p.stdout,
        'disposition': 'pending'}, indent=2))
    return key, p.returncode, len(p.stdout)


def status(d: dict, nodes: dict) -> None:
    for nid, n in nodes.items():
        isha = sha(node_bundle(d, nodes, n)[0])
        base = RUN / nid / isha
        state = 'reviewed' if base.exists() else 'stale_or_pending'
        att = sorted((RUN / nid).glob('*/attempt-*'), key=lambda p: p.stat().st_mtime) if (RUN / nid).exists() else []
        disp = ''
        if att:
            r = att[-1] / 'receipt.json'
            disp = json.loads(r.read_text()).get('disposition', '') if r.exists() else ''
        print(f'{nid:6} {state:18} attempts={len(att)} last_disposition={disp}')


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('mode', choices=['node', 'preflight', 'bundle', 'status'])
    ap.add_argument('args', nargs='*')
    ap.add_argument('--jobs', type=int, default=4)
    ap.add_argument('--max-attempts', type=int, default=2)
    ap.add_argument('--force', action='store_true')
    a = ap.parse_args()
    d, nodes = load_dag()
    if a.mode == 'status':
        return status(d, nodes)
    if a.mode == 'node':
        ids = a.args or list(nodes)
        jobs = [(nid, *node_bundle(d, nodes, nodes[nid])) for nid in ids]
    else:
        taskdoc, nid = Path(a.args[0]), a.args[1]
        data, recs = (preflight_bundle(taskdoc, nid) if a.mode == 'preflight' else cold_bundle(d, nodes, taskdoc, nid))
        jobs = [(f'{nid}-{a.mode}', data, recs)]
    with concurrent.futures.ThreadPoolExecutor(max_workers=a.jobs) as ex:
        for r in ex.map(lambda j: review(j[0], j[1], j[2], a.max_attempts, a.force), jobs):
            print(*r, flush=True)


if __name__ == '__main__':
    sys.exit(main())
