#!/bin/bash
# H11: wall time of `deskops view board` and `sldb views run board` in a NEW process each time,
# on the real deskops desk with its linked stores, cold (no disk cache) and hot (after stores build).
# Usage: h11_bench_run_view.sh <layout dir under /dev/shm> <sldb source dir> [runs=3]
# Builds the layout (worktrees of the sibling repos at origin tip, SHAs printed); the sldb link stays unbuilt (its symbol documents are generated, not tracked). Prints medians.
set -u
H=${1:?layout dir}; SLDB_SRC=${2:?sldb checkout}; RUNS=${3:-3}
P=/mnt/ssd/proyectos/SLDB_1; export PATH=$HOME/proyectos/SLDB_1/.venv/bin:$PATH TMPDIR=/dev/shm
mkdir -p "$H"
tip() { git -C "$P/$1" fetch -q origin 2>/dev/null; git -C "$P/$1" worktree add -q --detach "$H/$2" "origin/$3" 2>&1 | tail -1; }
tip deskops deskops main; tip spec2viz spec2viz master; tip pron pron master; tip scion scion main
git -C "$SLDB_SRC" worktree add -q --detach "$H/sldb" HEAD 2>&1 | tail -1
echo "### uptime: $(uptime)"
for r in deskops sldb spec2viz pron scion; do echo "### $r $(git -C "$H/$r" rev-parse --short HEAD)"; done
export PYTHONPATH=$H/deskops:$H/sldb/src XDG_CACHE_HOME=$H/xdg
wipe() { for r in deskops sldb spec2viz pron scion; do rm -rf "$H/$r/.sldb_cache"; done; rm -rf "$XDG_CACHE_HOME"; mkdir -p "$XDG_CACHE_HOME"; }
t() { local s=$(date +%s.%N); "$@" > /dev/null 2>&1; echo "$(date +%s.%N) - $s" | bc; }
median() { sort -n | awk '{a[NR]=$1} END{print a[int((NR+1)/2)]}'; }
build() { for r in spec2viz scion deskops; do (cd "$H/$r" && python -m sldb stores build --store .sldb >> "$H/build.log" 2>&1; echo "### stores build $r rc $?"); done; }
cd "$H/deskops"
wipe; : > "$H/build.log"; build
for cmd in "deskops view board --root ." "sldb views run board --store .sldb"; do
  c=(python -m $cmd); cold=(); hot=()
  for i in $(seq "$RUNS"); do
    for r in deskops sldb spec2viz pron scion; do rm -rf "$H/$r/.sldb_cache"; done; rm -rf "$XDG_CACHE_HOME"; mkdir -p "$XDG_CACHE_HOME"
    cold+=("$(t "${c[@]}")")
  done
  build >/dev/null
  for i in $(seq "$RUNS"); do hot+=("$(t "${c[@]}")"); done
  echo "$cmd | cold: ${cold[*]} median $(printf '%s\n' "${cold[@]}" | median) | hot: ${hot[*]} median $(printf '%s\n' "${hot[@]}" | median)"
done
