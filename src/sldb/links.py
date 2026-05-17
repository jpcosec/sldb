from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from sldb.store.layout import project_root
from sldb.store.io import load_documents_index, load_models_index, load_store_index

LINK_PATTERN = re.compile(r"(!)?\[\[([^\]]+)\]\]")


@dataclass
class ParsedLink:
    raw: str
    target: str
    kind: str


@dataclass
class ResolvedLink:
    raw: str
    target: str
    kind: str
    resolved: bool
    path: str | None = None
    source: str | None = None


def parse_links(markdown: str) -> list[ParsedLink]:
    links: list[ParsedLink] = []
    for match in LINK_PATTERN.finditer(markdown):
        links.append(
            ParsedLink(
                raw=match.group(0),
                target=match.group(2).strip(),
                kind="transclusion" if match.group(1) else "link",
            )
        )
    return links


def _tracked_documents(store_path: Path) -> dict[str, str]:
    root = project_root(store_path)
    store_index = load_store_index(store_path)
    tracked: dict[str, str] = {}
    for model_entry in store_index.models:
        models_idx = load_models_index(root / model_entry.models_index)
        docs_idx = load_documents_index(root / models_idx.documents_index)
        for doc in docs_idx.documents:
            tracked[doc.name] = str((root / doc.path).resolve())
    return tracked


def resolve_document_input(doc_ref: str, store_path: Path | None) -> Path:
    candidate = Path(doc_ref)
    if candidate.exists():
        return candidate.resolve()
    if store_path:
        tracked = _tracked_documents(store_path)
        if doc_ref in tracked:
            return Path(tracked[doc_ref]).resolve()
    return candidate.resolve()


def resolve_link_target(
    target: str, current_doc: Path, store_path: Path | None
) -> ResolvedLink:
    current_doc = current_doc.resolve()
    tracked = _tracked_documents(store_path) if store_path else {}
    if target in tracked:
        return ResolvedLink(
            raw=f"[[{target}]]",
            target=target,
            kind="link",
            resolved=True,
            path=tracked[target],
            source="store",
        )

    candidate = (current_doc.parent / target).resolve()
    if candidate.exists():
        return ResolvedLink(
            raw=f"[[{target}]]",
            target=target,
            kind="link",
            resolved=True,
            path=str(candidate),
            source="path",
        )

    direct = Path(target)
    if direct.exists():
        return ResolvedLink(
            raw=f"[[{target}]]",
            target=target,
            kind="link",
            resolved=True,
            path=str(direct.resolve()),
            source="path",
        )

    return ResolvedLink(raw=f"[[{target}]]", target=target, kind="link", resolved=False)


def recover_links(
    doc_path: Path,
    store_path: Path | None,
    include_transclusions: bool = False,
    depth: int = 1,
    seen: set[Path] | None = None,
) -> dict:
    """
    Recover links from a document, optionally recursing to a specified depth.
    """
    doc_path = doc_path.resolve()
    seen = seen or set()
    if doc_path in seen or depth < 1:
        return {
            "root": doc_path.stem,
            "path": str(doc_path),
            "links": [],
            "unresolved": [],
        }
    seen.add(doc_path)

    markdown = doc_path.read_text(encoding="utf-8")
    recovered = []
    for link in parse_links(markdown):
        if link.kind == "transclusion" and not include_transclusions:
            resolved_result = resolve_link_target(link.target, doc_path, store_path)
            resolved_result.kind = link.kind
            resolved_result.raw = link.raw
            recovered.append(resolved_result)
            continue
        resolved = resolve_link_target(link.target, doc_path, store_path)
        resolved.kind = link.kind
        resolved.raw = link.raw
        recovered.append(resolved)

    links = [
        {
            "target": entry.target,
            "kind": entry.kind,
            "resolved": entry.resolved,
            "path": entry.path,
            "source": entry.source,
        }
        for entry in recovered
    ]

    # Recursive step
    if depth > 1:
        for entry in recovered:
            if entry.resolved and entry.path:
                nested = recover_links(
                    Path(entry.path), store_path, include_transclusions, depth - 1, seen
                )
                links.extend(nested["links"])

    # Deduplicate links by target and kind
    unique_links = []
    seen_links = set()
    for item in links:
        key = (item["target"], item["kind"])
        if key not in seen_links:
            unique_links.append(item)
            seen_links.add(key)

    return {
        "root": doc_path.stem,
        "path": str(doc_path),
        "links": unique_links,
        "unresolved": [item["target"] for item in unique_links if not item["resolved"]],
    }


def compose_document(
    doc_path: Path, store_path: Path | None, seen: set[Path] | None = None
) -> dict:
    doc_path = doc_path.resolve()
    seen = seen or set()
    if doc_path in seen:
        return {
            "markdown": doc_path.read_text(encoding="utf-8"),
            "transclusions": [],
            "unresolved": [],
        }
    seen.add(doc_path)
    markdown = doc_path.read_text(encoding="utf-8")
    transclusions = []
    unresolved = []

    def _replace(match: re.Match[str]) -> str:
        bang, target = match.groups()
        if not bang:
            return match.group(0)
        resolved = resolve_link_target(target.strip(), doc_path, store_path)
        if not resolved.resolved or not resolved.path:
            unresolved.append(target.strip())
            return match.group(0)
        transclusions.append(target.strip())
        nested = compose_document(Path(resolved.path), store_path, seen)
        unresolved.extend(nested["unresolved"])
        transclusions.extend(nested["transclusions"])
        return nested["markdown"].rstrip()

    composed = LINK_PATTERN.sub(_replace, markdown)
    return {
        "root": doc_path.stem,
        "path": str(doc_path),
        "markdown": composed,
        "transclusions": sorted(dict.fromkeys(transclusions)),
        "unresolved": sorted(dict.fromkeys(unresolved)),
    }
