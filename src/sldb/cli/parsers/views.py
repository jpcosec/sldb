"""`sldb views run|list`: the composed views of a store (docs/architecture/views.md)."""

from __future__ import annotations

import argparse

from sldb.cli.output_format import add_format


class ParamAction(argparse.Action):
    """`--param k=v`, repeatable, collected into a mapping; a malformed or repeated key is a usage error."""

    def __call__(self, parser, namespace, value, option_string=None) -> None:
        key, sep, text = value.partition("=")
        if not sep or not key:
            parser.error(f"argument --param: expected key=value, got {value!r}")
        given = dict(getattr(namespace, self.dest) or {})
        if key in given:
            parser.error(f"argument --param: key {key!r} given more than once")
        given[key] = text
        setattr(namespace, self.dest, given)


def add_views_group(s: argparse._SubParsersAction) -> None:
    """Register `views`: run one composed view, list them."""
    p = s.add_parser("views", help="Composed views (ViewDoc with sections): run one with its params, or list them.")
    sub = p.add_subparsers(dest="views_command", required=True)
    _run(sub)
    _list(sub)


def _run(s) -> None:
    r = s.add_parser("run", formatter_class=argparse.RawDescriptionHelpFormatter, help="Evaluate a composed view: {view, params, revision, sections}.",
                     epilog="Example:\n  sldb views run tablero --param owner=ana --format json")
    r.add_argument("name", help="The view's name (ViewDoc:<name>)")
    r.add_argument("--param", action=ParamAction, default={}, metavar="KEY=VALUE", help="A param value (repeatable); every value is a string")
    _common(r)


def _list(s) -> None:
    l = s.add_parser("list", help="The composed views: name, title, params and section keys.")
    _common(l)


def _common(p: argparse.ArgumentParser) -> None:
    p.add_argument("--store", help="Store path")
    p.add_argument("--pythonpath", help="Directory to import models from")
    add_format(p)
