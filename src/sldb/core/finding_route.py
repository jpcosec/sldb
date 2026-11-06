"""Where findings raised below the CLI go: the listeners the application installed (GO08).

The library reports what it finds while it works (an `on_write` rule's alerts, for one) by
`route(findings)`; it cannot import the CLI. The CLI installs `sldb.cli.alert_sink` as a
listener when it starts, so those findings print and reach the envelope's `warnings`. With no
listener (an embedding program that installed none) `route` does nothing.
"""

from __future__ import annotations

from typing import Callable

from sldb.core.finding import Finding

_LISTENERS: list[Callable[[list[Finding]], None]] = []


def listen(listener: Callable[[list[Finding]], None]) -> None:
    """Add `listener`, once: installing it again is a no-op."""
    if listener not in _LISTENERS:
        _LISTENERS.append(listener)


def route(findings: list[Finding]) -> None:
    """Hand `findings` to every listener; nothing to hand, nothing called."""
    for listener in list(_LISTENERS) if findings else []:
        listener(findings)
