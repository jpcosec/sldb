import sys
from typing import Any
from sldb.cli.commands.inbox_core import get_desk_root, print_payload
from sldb.cli.commands.inbox_parse import resolve_note, note_detail


def show_note(args: Any) -> int:
    note = resolve_note(get_desk_root(args), args.show)
    if note is None:
        print(f"Unknown inbox note: {args.show}", file=sys.stderr)
        return 1
    detail = note_detail(note)
    if args.format == "text":
        return print_note_detail_text(detail)
    print_payload(detail, args.format)
    return 0


def print_note_detail_text(detail: dict[str, str]) -> int:
    print(f"# {detail['title']}\n")
    for meta in ("kind", "author", "created_at", "status", "path"):
        if meta in detail:
            print(f"{meta}: {detail[meta]}")
    print(f"\n{detail.get('body', '')}")
    return 0
