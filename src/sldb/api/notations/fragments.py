"""UML fragments: runs of consecutive links that share a `data.group`."""

from __future__ import annotations

from typing import Any

# UML fragment operators; a `group` starting with one declares it as `kind`
FRAGMENT_KINDS = ("alt", "loop", "opt", "par", "break", "critical", "neg", "ref", "seq", "strict")


def fragment_kind(group: str) -> tuple[str, str]:
    """`(kind, label)` of a `group`: `"loop for each spec"` -> `("loop", "for each spec")`."""
    head, _, rest = group.strip().partition(" ")
    if head.lower() in FRAGMENT_KINDS:
        return head.lower(), rest.strip()
    return "group", group.strip()


def _fragment(group: str, order: int) -> dict[str, Any]:
    """A new fragment opened by the link at `order`."""
    kind, label = fragment_kind(group)
    return {"label": label, "kind": kind, "group": group, "orders": [order]}


def _advance(out: list[dict[str, Any]], current: dict[str, Any] | None, link: dict[str, Any]) -> dict[str, Any] | None:
    """Extend the open fragment with `link`, or open a new one; returns the open fragment."""
    group = str(link.get("data", {}).get("group") or "")
    if group and current is not None and current["group"] == group:
        current["orders"].append(link["order"])
        return current
    current = _fragment(group, link["order"]) if group else None
    if current is not None:
        out.append(current)
    return current


def fragments_of(links: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """One fragment per consecutive run of links (by `order`) sharing the same `data.group`."""
    out: list[dict[str, Any]] = []
    current: dict[str, Any] | None = None
    for link in sorted((l for l in links if l.get("order")), key=lambda l: l["order"]):
        current = _advance(out, current, link)
    return out
