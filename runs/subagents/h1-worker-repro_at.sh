#!/bin/bash
# repro_at.sh <sldb-rev>: H2 of note 3895e9f7 with deskops' task models, on sldb <rev>.
REV=$1; export PATH=$HOME/proyectos/SLDB_1/.venv/bin:$PATH TMPDIR=/dev/shm
S=/dev/shm/h1w-src-$REV; rm -rf $S; mkdir -p $S
git -C /mnt/ssd/proyectos/SLDB_1/sldb-wt-h1 archive $REV src | tar -x -C $S
export PYTHONPATH=/dev/shm/deskops-main:$S/src XDG_CACHE_HOME=/dev/shm/h1w-xdg-$REV
R=/dev/shm/h1w-repro-$REV; rm -rf $R $XDG_CACHE_HOME; mkdir -p $R; cd $R; git init -q; git commit -q --allow-empty -m seed
python -c "import sldb,deskops;print(sldb.__file__)"
python -m deskops init . > /dev/null 2>&1
for n in uno dos tres; do python -m deskops add task "{\"title\":\"Repro $n\",\"why\":\"w\",\"goal\":\"g\",\"scope\":\"s\",\"implementation_path\":\"i\",\"done_when\":\"d\",\"validation\":[\"v\"],\"task_type\":\"task.code\"}" --root . > /dev/null 2>&1; done
for f in desk/tasks/task-repro-uno.md desk/tasks/task-repro-dos.md; do
  python - "$f" <<'PY'
import sys,re
p=sys.argv[1]; t=open(p,encoding="utf-8").read()
t=re.sub(r"^status: .*$","status: draft",t,count=1,flags=re.M)
t=re.sub(r"^history: \[\]$","history:\n- task_activates\n- task_hands_to_closeout",t,count=1,flags=re.M)
open(p,"w",encoding="utf-8").write(t)
PY
done
git add -A >/dev/null 2>&1; git commit -q -m invalid
for cold in warm cold; do
  [ $cold = cold ] && rm -rf .sldb_cache $XDG_CACHE_HOME
  echo "### $cold: sldb docs untrack tres"; timeout 300 python -m sldb docs untrack task-repro-tres --store .sldb 2>&1 | grep -v "^Sections" | tail -2 | cut -c1-200; echo "rc=${PIPESTATUS[0]}"; git status --short | head -5; git checkout -q -- . ; git clean -qfd -e .sldb_cache
  echo "### $cold: sldb docs untrack uno"; timeout 300 python -m sldb docs untrack task-repro-uno --store .sldb 2>&1 | grep -v "^Sections" | tail -2 | cut -c1-200; git status --short | head -5; git checkout -q -- . ; git clean -qfd -e .sldb_cache
done
rm -rf $R $S $XDG_CACHE_HOME
