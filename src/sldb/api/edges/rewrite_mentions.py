"""Mentions of the target in prose (GD22): where the project graph of GD21 located them
(`mention_hits`, one per path and line) and how a line is rewritten (`rewritten_line`): only
the text a configured `MentionPattern` captured and that names the target, and only where it
is a whole token of `[A-Za-z0-9_:./-]` (the character before and after are outside that set,
or the line's ends), so `card:card-a` never touches `card:card-ab` nor `card:card-a.b`; dots
that end the token and are followed by a space or the end of the line are sentence punctuation,
not part of it (`card:card-a.` is rewritten and keeps its dot). The new text keeps the
form the mention named the target in: the node id, its identity, its path, the document's name
or export id; a replacement that is neither a document nor a node is written as given. Prose
is never deleted: without a replacement the mention is reported as skipped.
"""

from __future__ import annotations

import re
from typing import TYPE_CHECKING, Any

from sldb.api.edges.project_graph.mention_pattern import MentionPattern
from sldb.api.edges.project_graph.project_graph import ProjectGraph
from sldb.api.edges.project_graph.project_graph_config import ProjectGraphConfig
from sldb.api.edges.referrer import Referrer

if TYPE_CHECKING:
    from sldb.api.edges.referrers import Target

TOKEN = r"[A-Za-z0-9_:./-]"
#: What may follow a whole token: sentence-ending dots then a space or the line's end, or a non-token character.
AFTER = r"(?=\.*(?:\s|$)|[^A-Za-z0-9_:./-])"


def mention_hits(graph: ProjectGraph, node_id: str) -> list[tuple[Referrer, None]]:
    """One referrer per (path, line) of the project edges reaching `node_id` that a line mention declared."""
    found: dict[tuple[str, int], Referrer] = {}
    for edge in graph.edges_to(node_id):
        line = line_of(edge.provenance_locator)
        if line is not None:
            found.setdefault((edge.provenance_path, line), Referrer(source=edge.provenance_path, location=f"{edge.provenance_path}:{line}", origin="mention"))
    return [(found[key], None) for key in sorted(found)]


def line_of(locator: str) -> int | None:
    """The line number of a `line:N:<label>` locator; None for `frontmatter` and the like."""
    parts = locator.split(":", 2)
    return int(parts[1]) if parts[0] == "line" and len(parts) > 1 and parts[1].isdigit() else None


def rewritten_line(line: str, graph: ProjectGraph, target: Target, replacement: Target | None, referrer: Referrer) -> tuple[str, list[dict[str, Any]], list[dict[str, Any]]]:
    """`line` with every captured text naming the target replaced; the changes and the skips."""
    texts = captured(graph, line, target.node_id or "")
    if not texts:
        return line, [], [{"source": referrer.source, "location": referrer.location, "reason": f"no mention of {target.given} is left on that line"}]
    if replacement is None:
        return line, [], [{"source": referrer.source, "location": referrer.location, "reason": "a mention in prose is kept: text is never deleted"}]
    changes, skips = [], []
    for text in texts:
        line = _replaced(line, text, mention_form(text, target, replacement, graph), referrer, changes, skips)
    return line, changes, skips


def rewritten_text(text: str, graph: ProjectGraph | None, path: str, hits: list[tuple[Referrer, Any]], target: Target, replacement: Target | None) -> tuple[str, list[dict[str, Any]], list[dict[str, Any]]]:
    """(new text, changes, skips) of one mentioning file's text, each hit's line rewritten."""
    lines, changes, skips = text.split("\n"), [], []
    for referrer, _ in hits:
        number = int((referrer.location or ":0").rsplit(":", 1)[1])
        lines[number - 1], made, left = rewritten_line(lines[number - 1], graph, target, replacement, referrer) if 0 < number <= len(lines) and graph else (lines[number - 1], [], [{"source": path, "location": referrer.location, "reason": "the line is gone"}])
        changes, skips = changes + made, skips + left
    return "\n".join(lines), changes, skips


def _replaced(line: str, text: str, new: str, referrer: Referrer, changes: list, skips: list) -> str:
    rewritten = re.sub(rf"(?<!{TOKEN}){re.escape(text)}{AFTER}", lambda _: new, line)
    if rewritten == line:
        skips.append({"source": referrer.source, "location": referrer.location, "reason": f"{text!r} is not a whole token on that line"})
    else:
        changes.append({"source": referrer.source, "field": None, "index": None, "location": referrer.location, "before": text, "after": new})
    return rewritten


def captured(graph: ProjectGraph, line: str, node_id: str) -> list[str]:
    """The texts the configured patterns capture on `line` that resolve to `node_id`, each once."""
    found: list[str] = []
    for pattern in patterns(graph.config):
        for match in pattern.compiled.finditer(line):
            named = graph.nodes.lookup.target_id(pattern.target.format(match.group(0), **match.groupdict()))
            if named == node_id and match.group(0) not in found:
                found.append(match.group(0))
    return found


def patterns(config: ProjectGraphConfig) -> list[MentionPattern]:
    """Every mention pattern of the configuration, section rules first."""
    return [pattern for rule in (*config.section_mentions, *config.line_mentions) for pattern in rule.patterns]


def mention_form(text: str, target: Target, replacement: Target, graph: ProjectGraph) -> str:
    """The replacement in the form `text` named the target; as given when no form matches."""
    lookup = graph.nodes.lookup
    node, new_node = lookup.by_id.get(target.node_id or ""), lookup.by_id.get(replacement.node_id or "")
    forms: dict[str | None, str | None] = {}
    if node is not None and new_node is not None:
        forms.update({node.id: new_node.id, node.identity: new_node.identity, node.path: new_node.path})
    if target.model and replacement.model:
        forms.update({target.name: replacement.name, target.export_id: replacement.export_id, target.path: replacement.path})
    return str(forms.get(text) or replacement.given)
