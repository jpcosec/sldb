#!/bin/bash
# usage: bench.sh <sldb src dir> [label]
export PATH="/tmp/ws-venv/bin:$PATH" TMPDIR=/dev/shm; unset VIRTUAL_ENV
H=/dev/shm/h11b; export PYTHONPATH=$H/deskops:${1:-$H/sldb/src} XDG_CACHE_HOME=$H/xdg
cd $H/deskops
t(){ local s=$(date +%s.%N); python -m sldb views run board --store .sldb >/dev/null 2>&1; echo "$(date +%s.%N) - $s" | bc; }
med(){ sort -n | awk '{a[NR]=$1} END{print a[int((NR+1)/2)]}'; }
python -m sldb views run board --store .sldb >/dev/null 2>&1   # prime
hot=(); for i in 1 2 3 4 5; do hot+=($(t)); done
echo "$2 hot: ${hot[*]} median $(printf '%s\n' "${hot[@]}" | med) | $(uptime | sed 's/.*load/load/')"
