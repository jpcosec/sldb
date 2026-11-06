from __future__ import annotations
from typing import Any
from sldb.cli.graph_ops import iter_search_records, search_records, SearchRecord
from sldb.api.where import where_records
from sldb.cli.commands.find_format import FindFormatter
from sldb.store.graph.language.predicate_parser import parse_predicate

class FindCLI:
    """Unified semantic + physical retrieval; `--where` is the predicate language (GO05)."""

    def run(self, args: Any) -> int:
        """Run the find command; `--explain` adds a finding per evaluated document."""
        if args.where: parse_predicate(args.where)  # once per query: unparseable predicates raise
        matched, findings = self._get_matches(args), None
        if args.where:
            matched, findings = where_records(matched, args.where, args.store, args.pythonpath, args.global_scope)
        return FindFormatter().format_output(matched, args, findings if getattr(args, "explain", False) else None)

    def _get_matches(self, args: Any) -> list[SearchRecord]:
        rebuild = getattr(args, "rebuild", False)
        records = iter_search_records(args.store, args.pythonpath, include_linked=args.global_scope, rebuild=rebuild)
        kinds = {args.type} if args.type != "all" else None
        return search_records(records, args.term, search_in=args.search_in, regex=args.regex, fuzzy=args.fuzzy, kinds=kinds)
