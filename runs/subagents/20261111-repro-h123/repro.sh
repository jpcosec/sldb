#!/bin/bash
# Reproducción H1-H3 (nota sldb 3895e9f7) sobre sldb main actual y deskops main.
export PATH=$HOME/proyectos/SLDB_1/.venv/bin:$PATH TMPDIR=/dev/shm
S=/dev/shm/sldb-h123-src; rm -rf $S; mkdir -p $S
git -C /mnt/ssd/proyectos/SLDB_1/sldb-desk-tmp archive origin/main src | tar -x -C $S
echo "### sldb $(git -C /mnt/ssd/proyectos/SLDB_1/sldb-desk-tmp rev-parse --short origin/main), deskops $(git -C /dev/shm/deskops-main rev-parse --short HEAD)"
export PYTHONPATH=/dev/shm/deskops-main:$S/src
R=/dev/shm/repro-h123; rm -rf $R; mkdir -p $R; cd $R; git init -q; git commit -q --allow-empty -m seed
python -m deskops init . > /dev/null 2>&1
for n in uno dos tres; do python -m deskops add task "{\"title\":\"Repro $n\",\"why\":\"w\",\"goal\":\"g\",\"scope\":\"s\",\"implementation_path\":\"i\",\"done_when\":\"d\",\"validation\":[\"v\"],\"task_type\":\"task.code\"}" --root . > /dev/null 2>&1; done
ls desk/tasks
# dos tareas pasan a un estado que el modelo rechaza: draft con history [task_activates, task_hands_to_closeout]
for f in desk/tasks/task-repro-uno.md desk/tasks/task-repro-dos.md; do
  python - "$f" <<'PY'
import sys,re
p=sys.argv[1]; t=open(p,encoding="utf-8").read()
t=re.sub(r"^status: .*$","status: draft",t,count=1,flags=re.M)
t=re.sub(r"^history: \[\]$","history:\n- task_activates\n- task_hands_to_closeout",t,count=1,flags=re.M)
open(p,"w",encoding="utf-8").write(t)
PY
done
grep -A3 "^status\|^history" desk/tasks/task-repro-uno.md | head -6
git add -u >/dev/null 2>&1; git commit -q -m invalid
echo "### H1: sldb stores check"
timeout 600 python -m sldb stores check --store .sldb > /dev/shm/h1.log 2>&1; echo "rc=$?"; grep -v "^Sections rebuild" /dev/shm/h1.log | grep -E "Unexpected|FAIL|PASS|invalid|ValidationError" | head -5 | cut -c1-250
echo "### H2/H3: sldb docs update (escritura) de la tercera tarea, válida"
timeout 600 python -m deskops edit task task-repro-tres summary "otro" --root . > /dev/shm/h2.log 2>&1; echo "rc=$?"; grep -v "^Sections rebuild" /dev/shm/h2.log | tail -4 | cut -c1-300
echo "### git status tras la escritura fallida (H3: lo que quedó escrito)"
git status --short | head -10
