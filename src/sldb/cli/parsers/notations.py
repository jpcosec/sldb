"""`sldb notations`: Visual notations, palettes, views, and resolving from the command line."""

from __future__ import annotations

import argparse


def _store_args(p: argparse.ArgumentParser) -> None:
    p.add_argument("--store", help="Store path")
    p.add_argument("--pythonpath", help="Project path")


def _add_list(sub: argparse._SubParsersAction) -> None:
    p_list = sub.add_parser("list", help="List notations or projection views in the store or builtins.")
    p_list.add_argument("--views", action="store_true", help="List projection views instead of notations")
    _store_args(p_list)


def _add_sync(sub: argparse._SubParsersAction) -> None:
    p_sync = sub.add_parser("sync", help="Synchronize a notation, a palette, diagram specs or a vistas.yml catalog into the store.")
    p_sync.add_argument("--notation", help="Notation name or YAML file to sync; with --spec, the notation the specs are drawn with (`none` for none)")
    p_sync.add_argument("--palette", help="Palette name or YAML file to sync")
    p_sync.add_argument("--spec", action="append", default=[], help="Diagram spec YAML to reconcile (SpecDoc, SpecNodeDoc, RelationDoc); repeatable")
    p_sync.add_argument("--catalog", help="vistas.yml whose specs are synced with their notation and catalog metadata")
    p_sync.add_argument("--check", action="store_true", help="With --catalog: only validate it (paths, specs, notations); write nothing")
    p_sync.add_argument("--prune", action="store_true", help="With --catalog: delete the catalog SpecDocs the vistas.yml no longer lists")
    p_sync.add_argument("--strict", action="store_true", help="With --spec/--catalog: exit 1 when a ref does not exist or the edge index reports errors")
    p_sync.add_argument("--json", action="store_true", help="With --spec/--catalog: print the list of reports as JSON")
    _store_args(p_sync)


def _add_validate(sub: argparse._SubParsersAction) -> None:
    p = sub.add_parser("validate", help="Validate a notation, a palette or a spec by name or path; print findings.")
    p.add_argument("target", help="Builtin or store name, or a YAML/JSON file (palette, spec or notation)")
    p.add_argument("--json", action="store_true", help="Print the findings as JSON")
    _store_args(p)


def _add_view(sub: argparse._SubParsersAction) -> None:
    p_view = sub.add_parser("view", help="Resolve a SpecDoc or projection view.")
    p_view.add_argument("spec", help="SpecDoc reference (e.g. SpecDoc:arch or arch) or ViewDoc reference")
    p_view.add_argument("--projection", action="store_true", help="Evaluate as projection view instead of SpecDoc")
    _store_args(p_view)


def _add_resolve(sub: argparse._SubParsersAction) -> None:
    p_resolve = sub.add_parser("resolve", help="Resolve documents under a notation without a SpecDoc.")
    p_resolve.add_argument("--notation", required=True, help="NotationDoc reference (e.g. NotationDoc:uml-class or uml-class)")
    p_resolve.add_argument("--docs", nargs="+", required=True, help="Document references to style (Model:name)")
    p_resolve.add_argument("--relations", nargs="*", help="Optional RelationDoc references to style")
    _store_args(p_resolve)


def _add_from_graph(sub: argparse._SubParsersAction) -> None:
    p = sub.add_parser("from-graph", help="Compile an sldb graph (snapshot JSON or store index) or a Python tree into a component spec.")
    source = p.add_mutually_exclusive_group(required=True)
    source.add_argument("--snapshot", help="Node-link JSON (`sldb graph snapshot save`, or the Python source graph of `sldb selfdoc python-sync`)")
    source.add_argument("--store", help="Read the edge index of this .sldb (or project) dir via sldb.api")
    source.add_argument("--python", help="Directory of .py files, scanned with sldb.code (extra [code]); nodes module/class/external")
    _from_graph_filters(p)
    p.add_argument("--id", dest="spec_id", help="Spec id. Defaults to the file stem, 'sldb-graph', or the parent dir of --python")
    p.add_argument("--title", help="Spec title. Defaults to '<id> graph' ('<id> AST Architecture' with --python)")
    p.add_argument("--output", help="Write the YAML spec here instead of stdout")


def _from_graph_filters(p: argparse.ArgumentParser) -> None:
    p.add_argument("--node-type", dest="node_types", action="append", default=[], help="Node type to keep (document, model, semantic_tag, ...); repeatable. Default: document, model")
    p.add_argument("--model", dest="models", action="append", default=[], help="Keep only documents of this model (e.g. AtomDoc); repeatable")
    p.add_argument("--relation", dest="relations", action="append", default=[], help="Keep only these relations; repeatable. Overrides the default exclusions")
    p.add_argument("--exclude-relation", dest="exclude_relations", action="append", default=[], help="Drop this relation; repeatable. Default: structural relations")
    p.add_argument("--drop-isolated", action="store_true", help="Drop nodes left without edges after filtering")
    p.add_argument("--label-field", help="Payload field that gives each document node its label (default: the document id). Needs --store; a --snapshot has no payload, only the id and the model")
    p.add_argument("--kind-field", help="Payload field, or tag:<namespace> (the first tag '<namespace>:x' gives 'x'), that gives each document node its kind (default: the model). Needs --store")
    p.add_argument("--group-field", help="Payload field or tag:<namespace>: documents with the same value go into one container node (kind 'group') with contains edges. Needs --store")
    p.add_argument("--module-prefix", dest="module_prefixes", action="append", default=[], help="Keep only Python nodes of this module or below; repeatable. With --python, the one root package")


def add_notations_group(s: argparse._SubParsersAction) -> None:
    """Register `notations list|sync|validate|view|resolve|from-graph`."""
    p = s.add_parser("notations", help="Visual notations, palettes, views and diagram resolver.")
    sub = p.add_subparsers(dest="notations_command", required=True)
    for add in (_add_list, _add_sync, _add_validate, _add_view, _add_resolve, _add_from_graph):
        add(sub)
