"""El payload de átomos por título: `clave -> {title, aliases, atoms: {pregunta -> átomo}}`.

Migrado de `spec2viz.deskops` (`parse_atoms` y `SldbAtomResolver._merge_atom`). Un archivo que
no se puede leer deja un finding `matching/atom-parse-failed` en vez de imprimir.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import yaml

from sldb.api.matching.atom_keys import alias_candidates, normalize_key
from sldb.api.matching.matching_findings import finding
from sldb.core.finding import Finding


def merge_atom(payload: dict[str, dict], atom: dict, doc_path: Path, store_path: Path) -> None:
    """Agrega un `AtomDoc` del store bajo la clave de su título (sin título, pregunta o cuerpo, nada)."""
    title, question = str(atom.get("title") or "").strip(), str(atom.get("five_wh_one_plus") or "").strip().lower()
    body = str(atom.get("answer") or "").strip()
    title_norm = normalize_key(title)
    if not title or not question or not body or not title_norm:
        return
    tags = atom.get("tags") or []
    entry = payload.setdefault(title_norm, {"title": title, "atoms": {}, "aliases": alias_candidates(title, tags)})
    entry["aliases"] = alias_candidates(title, tags)
    entry["atoms"][question] = {"id": atom.get("id") or doc_path.stem, "body": body, "path": str(doc_path), "store": str(store_path), "tags": tags, "provenance": atom.get("provenance")}


def atoms_from_documents(docs: list[dict]) -> dict[str, dict]:
    """El payload de los `AtomDoc` entre los documentos de un store (`store_documents`)."""
    payload: dict[str, dict] = {}
    for doc in docs:
        if doc["model"] == "AtomDoc":
            merge_atom(payload, doc["payload"], Path(doc["path"]), Path(doc["store"]))
    return payload


def _add_file_atom(atoms_db: dict, md_file: Path, fm: dict, body: str) -> None:
    """Agrega el átomo de un archivo con front matter, si trae título y pregunta."""
    title, question = fm.get("title"), fm.get("five_wh_one_plus")
    if not (title and question):
        return
    title_norm, tags = normalize_key(title), fm.get("tags") or []
    if title_norm not in atoms_db:
        atoms_db[title_norm] = {"title": title.strip(), "aliases": alias_candidates(title, tags), "atoms": {}}
    atoms_db[title_norm]["atoms"][question.strip().lower()] = {"id": fm.get("id", md_file.stem), "body": body, "tags": tags}


def _parse_file(atoms_db: dict, md_file: Path, content: str) -> None:
    parts = re.split(r'^---\s*$', content, maxsplit=2, flags=re.MULTILINE)
    if len(parts) >= 3:
        _add_file_atom(atoms_db, md_file, yaml.safe_load(parts[1]), parts[2].strip())


def _parse_into(atoms_db: dict, md_file: Path, findings: list[Finding] | None) -> None:
    content = md_file.read_text(encoding="utf-8")
    try:
        _parse_file(atoms_db, md_file, content)
    except Exception as exc:
        if findings is not None:
            findings.append(finding("atom-parse-failed", str(md_file), f"Failed to parse atom {md_file}: {exc}", "corregir el front matter del átomo"))


def parse_atoms(atoms_dir: Path, findings: list[Finding] | None = None) -> str:
    """El payload (JSON) de los átomos `*.md` de una carpeta; los que fallan van a `findings`."""
    if not atoms_dir or not atoms_dir.exists():
        return "{}"
    atoms_db: dict[str, dict] = {}
    for md_file in atoms_dir.glob("*.md"):
        _parse_into(atoms_db, md_file, findings)
    return json.dumps(atoms_db)
