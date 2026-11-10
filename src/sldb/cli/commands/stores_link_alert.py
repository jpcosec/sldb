"""The alert `stores build` and `stores build --check` give for a declared link whose store is
absent (a sibling repository not checked out, as in a CI runner): it names the link and its
declared path, so a link that is really broken is not hidden."""

from __future__ import annotations

from sldb.core.finding import alert


def link_missing_what(link: dict[str, str]) -> str:
    """The alert text: it names the declared path."""
    return f"declared link path {link['path']} has no store; the build goes on without it"


def link_missing_alert(link: dict[str, str]) -> dict:
    """The `build/link-missing` finding for one absent link, as a dict."""
    return alert("build/link-missing", link["name"], link_missing_what(link), "check out the linked repository next to this one").as_dict()
