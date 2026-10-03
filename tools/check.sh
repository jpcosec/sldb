#!/usr/bin/env bash
# Todas las puertas, en orden de costo creciente.
#
# Es la única entrada: lo que corre acá es lo que decide si un cambio entra. Dos
# listas de comprobaciones en dos lugares divergen, y entonces deja de estar
# claro qué decide.
#
#   bash tools/check.sh            todas
#   bash tools/check.sh --fast     solo las de segundos, para antes de un commit
set -uo pipefail
cd "$(dirname "$0")/.."
export PYTHONPATH="${PYTHONPATH:-src}"

FAST=${1:-}
FAILED=()
SKIPPED=()

gate() {
  local name=$1; shift
  printf '\n\033[1m── %s ──\033[0m\n' "$name"
  "$@" || FAILED+=("$name")
}

# ── Rápidas: estructura. Segundos, aptas para un gancho pre-commit. ──────────

# S1 · el núcleo no arrastra la persistencia. Una línea en una excepción costaba
# 46 módulos; esta puerta existe para que no vuelva a costarlos en silencio.
gate "núcleo aislado" python3 - <<'PY'
import sys
import sldb.core.renderer  # noqa: F401
leaked = sorted({m.split(".")[1] for m in sys.modules
                 if m.startswith("sldb.") and m.split(".")[1] in {"store", "api", "cli"}})
if leaked:
    print(f"  ERROR  importar el núcleo arrastra: {', '.join(leaked)}")
    print(f"  ERROR  revisa src/sldb/core/exceptions/ — reexportar una excepción "
          f"de otra capa contamina todo el paquete")
print(f"{'FAIL' if leaked else 'PASS'}: núcleo aislado — "
      f"{len([m for m in sys.modules if m.startswith('sldb')])} módulos cargados")
raise SystemExit(1 if leaked else 0)
PY

# S2 · el grafo de paquetes respeta el orden declarado en contracts/layers.toml.
gate "capas" python3 tools/check_layers.py

# S5 · la frontera entre el producto y su autoaplicación, según contracts/identity.toml.
gate "identidad" python3 tools/check_identity.py

# El mapa de capacidades corresponde al código, según la sección [[axis]].
gate "ejes" python3 tools/check_axes.py

# S4 · lo que los consumidores del ecosistema importan está declarado.
# Se salta sola si los consumidores no están presentes, y lo dice.
gate "superficie" python3 tools/check_surface.py

# ── Lentas: comportamiento y verdad documental. ──────────────────────────────

if [ "$FAST" != "--fast" ]; then
  # S3* · lo que los documentos afirman sobre el código es cierto.
  gate "afirmaciones" python3 tools/check_claims.py

  # El comportamiento. La única puerta que ya existía antes de esta propuesta.
  gate "pruebas" python3 -m pytest tests -q

  # La referencia de la interfaz corresponde a la interfaz.
  gate "selfdoc" python3 -m sldb selfdoc check
else
  SKIPPED+=("afirmaciones" "pruebas" "selfdoc")
fi

printf '\n'
[ ${#SKIPPED[@]} -gt 0 ] && printf 'omitidas (--fast): %s\n' "${SKIPPED[*]}"
if [ ${#FAILED[@]} -eq 0 ]; then
  printf '\033[32mTODAS LAS PUERTAS PASAN\033[0m\n'
  exit 0
fi
printf '\033[31mFALLAN: %s\033[0m\n' "${FAILED[*]}"
exit 1
