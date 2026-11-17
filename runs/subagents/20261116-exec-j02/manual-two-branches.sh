#!/usr/bin/env bash
# Prueba a mano: dos ramas que tocan documentos distintos, merge con y sin el driver.
set -u
SLDB="uv run --project /mnt/ssd/proyectos/SLDB_1/sldb --frozen --extra code --extra dev sldb"
W=/dev/shm/j02/repo-$1; rm -rf "$W"; mkdir -p "$W/notes"; cd "$W"
git init -q -b main; git config user.email t@t; git config user.name t
cat > notes/models.py <<'PY'
from pydantic import Field
from sldb import StructuredNLDoc
class Note(StructuredNLDoc):
    __template__ = '# ⸢rev•title⸥'
    title: str = Field(description='Title')
PY
touch notes/__init__.py
echo "notes/__pycache__/" > .gitignore
$SLDB stores init --path . >/dev/null
$SLDB models add notes.models:Note --store .sldb --pythonpath . >/dev/null
$SLDB docs create --model Note -o docs/n0.md --name n0 '{"title":"zero"}' --store .sldb --pythonpath . >/dev/null
$SLDB stores declare --store .sldb --write >/dev/null
[ "$1" = driver ] && { echo '$ sldb stores merge-driver --install'; $SLDB stores merge-driver --install; echo '$ (otra vez)'; $SLDB stores merge-driver --install; cat .gitattributes; }
git add -A; git commit -qm base
git checkout -qb rama-a
$SLDB docs create --model Note -o docs/a.md --name a '{"title":"desde a"}' --store .sldb --pythonpath . >/dev/null
$SLDB stores declare --store .sldb --write >/dev/null; git add -A; git commit -qm a
git checkout -q main; git checkout -qb rama-b
$SLDB docs create --model Note -o docs/b.md --name b '{"title":"desde b"}' --store .sldb --pythonpath . >/dev/null
$SLDB stores declare --store .sldb --write >/dev/null; git add -A; git commit -qm b
echo '$ git merge rama-a'; git merge --no-edit rama-a; echo "rc=$?"
git status --short
echo '$ sldb stores check'; $SLDB stores check --store .sldb --quiet; echo "rc=$?"
echo '$ sldb stores rebuild-index'; $SLDB stores rebuild-index --store .sldb; echo "rc=$?"
echo '$ sldb stores check'; $SLDB stores check --store .sldb --quiet; echo "rc=$?"
echo '$ grep include store.yaml'; sed -n '/^include:/,$p' .sldb/store.yaml
cp -r .sldb /dev/shm/j02/merged-$1-sldb
