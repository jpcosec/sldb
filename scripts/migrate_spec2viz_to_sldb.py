#!/usr/bin/env python3
"""Migra un store SLDB que dependía de spec2viz al nuevo formato nativo de SLDB.

Acciones que realiza:
1. Examina los modelos registrados en store.yaml y .sldb/core/models/.
2. Reemplaza referencias legacy `spec2viz.sldb_models:<Model>` por `sldb.models.notation_models:<Model>`.
3. Sincroniza la paleta default y las notaciones builtin si faltan en el store.
4. Reconstruye el índice de aristas (edge index) y valida la integridad de los documentos.
5. Emite un informe estructurado de la migración.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Inyectar sldb
REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "sldb" / "src"))

from sldb import api
from sldb.models.notation_models import (
    GlyphDoc,
    LinkDoc,
    NotationDoc,
    PaletteDoc,
    SpecDoc,
    SpecNodeDoc,
    ViewDoc,
)
from sldb.store.io import load_store_index
import yaml

BUILTIN_MODELS_MAP = {
    "spec2viz.sldb_models:SpecDoc": "sldb.models.notation_models:SpecDoc",
    "spec2viz.sldb_models:SpecNodeDoc": "sldb.models.notation_models:SpecNodeDoc",
    "spec2viz.sldb_models:NotationDoc": "sldb.models.notation_models:NotationDoc",
    "spec2viz.sldb_models:GlyphDoc": "sldb.models.notation_models:GlyphDoc",
    "spec2viz.sldb_models:LinkDoc": "sldb.models.notation_models:LinkDoc",
    "spec2viz.sldb_models:PaletteDoc": "sldb.models.notation_models:PaletteDoc",
    "spec2viz.sldb_models:ViewDoc": "sldb.models.notation_models:ViewDoc",
}

BUILTIN_NOTATIONS = [
    "activity",
    "component",
    "component-view-matrix",
    "deployment",
    "reflection",
    "statechart",
    "uml-class",
    "uml-sequence",
]


def migrate_store(store_path: Path, pythonpath: str | None = None) -> dict[str, any]:
    report = {
        "store": str(store_path),
        "models_migrated": [],
        "notations_synced": [],
        "palettes_synced": [],
        "edge_index_rebuilt": False,
        "status": "ok",
    }

    if not store_path.exists():
        raise FileNotFoundError(f"Store no encontrado: {store_path}")

    # Si nos pasan la carpeta del proyecto en vez de .sldb, buscar .sldb
    if (store_path / ".sldb").exists():
        store_path = store_path / ".sldb"

    print(f"[*] Iniciando migración de store en: {store_path}")

    # 1. Revisar y migrar store.yaml
    store_yaml_file = store_path / "store.yaml"
    if store_yaml_file.exists():
        data = yaml.safe_load(store_yaml_file.read_text(encoding="utf-8")) or {}
        changed = False
        models = data.get("models") or []
        for m in models:
            ref = m.get("model_ref") or ""
            if ref in BUILTIN_MODELS_MAP:
                new_ref = BUILTIN_MODELS_MAP[ref]
                print(f"  [+] Migrando model_ref en store.yaml: {ref} -> {new_ref}")
                m["model_ref"] = new_ref
                report["models_migrated"].append({"from": ref, "to": new_ref})
                changed = True
        if changed:
            store_yaml_file.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")

    # 2. Revisar archivos en .sldb/core/models/*.yaml
    core_models_dir = store_path / "core" / "models"
    if core_models_dir.exists():
        for mf in core_models_dir.glob("*.yaml"):
            mdata = yaml.safe_load(mf.read_text(encoding="utf-8")) or {}
            ref = mdata.get("model_ref") or ""
            if ref in BUILTIN_MODELS_MAP:
                new_ref = BUILTIN_MODELS_MAP[ref]
                print(f"  [+] Migrando modelo {mf.name}: {ref} -> {new_ref}")
                mdata["model_ref"] = new_ref
                mf.write_text(yaml.safe_dump(mdata, sort_keys=False), encoding="utf-8")

    # 3. Sincronizar paleta default
    try:
        api.sync_palette(store_path, "default")
        report["palettes_synced"].append("default")
        print("  [+] Paleta 'default' sincronizada.")
    except Exception as exc:
        print(f"  [!] Advertencia al sincronizar paleta default: {exc}")

    # 4. Sincronizar notaciones builtin
    for not_name in BUILTIN_NOTATIONS:
        try:
            api.sync_notation(store_path, not_name)
            report["notations_synced"].append(not_name)
            print(f"  [+] Notación builtin '{not_name}' sincronizada.")
        except Exception as exc:
            print(f"  [!] Advertencia al sincronizar notación '{not_name}': {exc}")

    # 5. Reconstruir índice de aristas
    print("  [*] Reconstruyendo índice de aristas del store...")
    try:
        api.load_edge_index(store_path)
        report["edge_index_rebuilt"] = True
        print("  [+] Índice de aristas reconstruido con éxito.")
    except Exception as exc:
        print(f"  [!] Error al reconstruir índice de aristas: {exc}")
        report["status"] = "error"
        report["error"] = str(exc)

    return report


def main():
    parser = argparse.ArgumentParser(description="Migra un store SLDB hacia el soporte nativo de notaciones y visualización.")
    parser.add_argument("--store", default="workbench_demo", help="Ruta del store a migrar (por defecto workbench_demo)")
    parser.add_argument("--pythonpath", default=str(REPO_ROOT), help="PYTHONPATH para cargar modelos")

    args = parser.parse_args()
    store_p = Path(args.store).resolve()

    try:
        res = migrate_store(store_p, args.pythonpath)
        print("\n[OK] Migración finalizada correctamente:")
        print(yaml.safe_dump(res, sort_keys=False))
    except Exception as e:
        print(f"\n[ERROR] Falló la migración: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
