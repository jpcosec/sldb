"""One path step over a graph view: the elements it reaches, closure included.

A reference to a document the view does not hold is dropped (closed world, §3); an edge marked
`unavailable` (a linked store that cannot be opened) yields an incomplete element. Crossing a
field `F` of the origin whose payload carries `F__anchor_state` exposes, on each element
reached, that entry under the name `anchor_state` (element `i` of a list field reads entry `i`;
a scalar field reads the scalar). Crossing `^F` the entry is read from the element reached,
which is the one holding `F` (GO07: `any(^subject: anchor_state = "intact")`). Without the
entry `anchor_state` stays undefined.
"""

from __future__ import annotations

_NO_ALIAS = object()


def reach_step(view: dict, origin: dict, step: tuple) -> list[dict]:
    """The elements one step reaches from `origin`."""
    return _closure(view, origin, step) if step[3] else _once(view, origin, step)


def _once(view: dict, origin: dict, step: tuple) -> list[dict]:
    elements = (_element(view, origin, edge, step) for edge in _edges(view, origin["id"], step))
    return [element for element in elements if element is not None]


def _closure(view: dict, origin: dict, step: tuple) -> list[dict]:
    found, queue, visited = [], [origin], {origin["id"]}
    while queue:
        for element in _once(view, queue.pop(0), step):
            if element["id"] not in visited:
                visited.add(element["id"])
                found.append(element)
                queue += [] if element.get("incomplete") else [element]
    return found


def _edges(view: dict, node_id: str, step: tuple) -> list[dict]:
    kind, name, inverse, _ = step
    edges = view["in" if inverse else "out"](node_id)
    if kind == "rel":
        return [edge for edge in edges if edge["type"] == name]
    return [edge for edge in edges if edge["type"] == "references" and edge.get("field") == name]


def _element(view: dict, origin: dict, edge: dict, step: tuple) -> dict | None:
    target = edge["source"] if step[2] else edge["target"]
    if edge.get("unavailable"):
        return {"id": target, "incomplete": target}
    node = view["node"](target)
    alias = _alias(node if step[2] else origin, edge, step)
    if node is None or alias is _NO_ALIAS:
        return node
    return {**node, "payload": {**node["payload"], "anchor_state": alias}}


def _alias(holder: dict | None, edge: dict, step: tuple):
    """The entry of the document holding the field crossed: the origin, or the element reached by `^F`."""
    key = f"{step[1]}__anchor_state"
    if step[0] != "field" or holder is None or key not in holder["payload"]:
        return _NO_ALIAS
    states, values = holder["payload"][key], holder["payload"].get(step[1])
    if not isinstance(values, list):
        return states
    position = _position(values, edge)
    usable = isinstance(states, list) and position is not None and position < len(states)
    return states[position] if usable else _NO_ALIAS


def _position(values: list, edge: dict) -> int | None:
    for wanted in (edge.get("declared"), edge["target"]):
        if wanted in values:
            return values.index(wanted)
    return None
