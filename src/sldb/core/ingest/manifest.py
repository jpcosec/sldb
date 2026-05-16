"""
Manages the raw source manifest system for tracking file provenance.
"""

from __future__ import annotations

import csv
import hashlib
from datetime import datetime
from pathlib import Path

from .contracts import RawSourceEntry


def compute_content_hash(path: Path) -> str:
    """Computes a SHA-256 hash of a file's content."""
    sha256 = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(8192):
            sha256.update(chunk)
    return sha256.hexdigest()


def load_manifest(manifest_path: Path) -> list[RawSourceEntry]:
    """Loads entries from the CSV manifest file."""
    if not manifest_path.exists():
        return []
    
    entries: list[RawSourceEntry] = []
    with open(manifest_path, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            entries.append(RawSourceEntry.model_validate(row))
    return entries


def save_manifest(manifest_path: Path, entries: list[RawSourceEntry]) -> None:
    """Saves entries to the CSV manifest file."""
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    
    fieldnames = [
        "filename", "path", "file_kind", "content_hash", 
        "status", "created", "notes"
    ]
    
    with open(manifest_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for entry in entries:
            writer.writerow(entry.model_dump())


def add_to_manifest(
    project_root: Path,
    manifest_path: Path,
    source_path: Path,
    notes: str = ""
) -> RawSourceEntry:
    """Registers a new raw source file in the manifest."""
    if not source_path.exists():
        raise FileNotFoundError(f"Source file not found: {source_path}")
    
    rel_path = source_path.relative_to(project_root).as_posix()
    content_hash = compute_content_hash(source_path)
    
    entries = load_manifest(manifest_path)
    
    # Check for existing entry by path
    for entry in entries:
        if entry.path == rel_path:
            # Update hash and timestamp? Or just skip? 
            # For now, let's update if hash changed.
            if entry.content_hash != content_hash:
                entry.content_hash = content_hash
                entry.created = datetime.now().isoformat()
                entry.notes = notes or entry.notes
            save_manifest(manifest_path, entries)
            return entry
    
    new_entry = RawSourceEntry(
        filename=source_path.name,
        path=rel_path,
        file_kind=source_path.suffix.lstrip(".").lower() or "unknown",
        content_hash=content_hash,
        status="new",
        created=datetime.now().isoformat(),
        notes=notes
    )
    
    entries.append(new_entry)
    save_manifest(manifest_path, entries)
    return new_entry
