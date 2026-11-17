"""The keys and column attributes of one statement, from pglast's tree (Postgres' own parse) and its tokens.

From a `CREATE TABLE`: each column (`ColumnDef`) with `type` (the tokens written between its name and
its first constraint, whitespace collapsed, comments out), the marks `primary_key`, `unique` and `identity` (`GENERATED
... AS IDENTITY`) when written in the column, and `references {table, columns}` for its own
`REFERENCES`; and each table key (`Constraint` `PRIMARY KEY`, `FOREIGN KEY`, `UNIQUE`). From an
`ALTER TABLE` (of a table): each `ADD [CONSTRAINT name] {PRIMARY KEY|FOREIGN KEY|UNIQUE}`, named or not.
A key has `name` (None when unnamed; `short` is `pk`, `fk`, `unique`), `constraint_type`, `columns`
and, a foreign key, `references {table, columns}` (`columns: []` is the referenced primary key). Names
are spelled as written (`sql_pg_tokens`), the referenced table with its schema when written. Not keys:
`CHECK`, `EXCLUDE`, `NOT NULL`; nor the keys of an `ALTER TABLE ... ADD COLUMN`. Spans are byte ranges in the file.
"""

from __future__ import annotations

from typing import Any

from sldb.code.sql_names import unquote
from sldb.code.sql_pg import is_table, to_byte
from sldb.code.sql_pg_tokens import element_end, index_at, paren_list, tok_text, written

_KEYS = {"CONSTR_PRIMARY": ("primary_key", "pk"), "CONSTR_FOREIGN": ("foreign_key", "fk"), "CONSTR_UNIQUE": ("unique", "unique")}
_MARKS = {"CONSTR_PRIMARY": "primary_key", "CONSTR_UNIQUE": "unique", "CONSTR_IDENTITY": "identity"}


def create_parts(stmt: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]] | None:
    """`(columns, keys)` of a parsed `CREATE TABLE`, or None when the statement is not one or did not parse."""
    if type(stmt["node"]).__name__ != "CreateStmt":
        return None
    elts = stmt["node"].tableElts or ()
    keys = [_key(e, stmt) for e in elts if type(e).__name__ == "Constraint" and e.contype.name in _KEYS]
    return [_column(e, stmt) for e in elts if type(e).__name__ == "ColumnDef"], keys


def alter_parts(stmt: dict[str, Any]) -> tuple[str, list[dict[str, Any]] | None] | None:
    """`(table as written, keys)` of an `ALTER TABLE`; keys None when Postgres rejects it; None when it is no `ALTER TABLE`."""
    node, toks, text = stmt["node"], stmt["tokens"], stmt["text"]
    if node is None:
        names = [t.name for t in toks[:2]]
        return (written(toks, _after_head(toks), text)[0], None) if names == ["ALTER", "TABLE"] else None
    if type(node).__name__ != "AlterTableStmt" or not is_table(node):
        return None
    defs = [c.def_ for c in node.cmds if c.subtype.name == "AT_AddConstraint" and c.def_.contype.name in _KEYS]
    return written(toks, index_at(toks, node.relation.location), text)[0], [_key(d, stmt) for d in defs]


def _key(con: Any, stmt: dict[str, Any]) -> dict[str, Any]:
    toks, text = stmt["tokens"], stmt["text"]
    i = index_at(toks, con.location)
    named, (ctype, short) = toks[i].name == "CONSTRAINT", _KEYS[con.contype.name]
    key = {"name": unquote(tok_text(toks[i + 1], text)) if named else None, "short": short, "constraint_type": ctype,
           "columns": paren_list(toks, i, text) if (con.keys or con.fk_attrs) else [], "span": _span(stmt, i, i + 1 if named else i)}
    return {**key, "references": _refs(con, stmt)} if ctype == "foreign_key" else key


def _refs(con: Any, stmt: dict[str, Any]) -> dict[str, Any]:
    toks, text = stmt["tokens"], stmt["text"]
    table, after = written(toks, index_at(toks, con.pktable.location), text)
    return {"table": table, "columns": paren_list(toks, after, text) if con.pk_attrs else []}


def _column(col: Any, stmt: dict[str, Any]) -> dict[str, Any]:
    toks, text, cons = stmt["tokens"], stmt["text"], col.constraints or ()
    i = index_at(toks, col.location)
    stops = [c.location for c in cons] + ([col.collClause.location] if col.collClause else [])
    stop = min(stops + [toks[element_end(toks, i) - 1].end + 1])
    last = max((t.end + 1 for t in toks if col.typeName.location <= t.start < stop), default=col.typeName.location)
    attrs = {"type": " ".join(text[col.typeName.location:last].split()) or None, **{_MARKS[c.contype.name]: True for c in cons if c.contype.name in _MARKS}}
    refs = [_refs(c, stmt) for c in cons if c.contype.name == "CONSTR_FOREIGN"]
    return {"name": unquote(tok_text(toks[i], text)), "attrs": {**attrs, **({"references": refs[0]} if refs else {})}, "span": _span(stmt, i, i)}


def _span(stmt: dict[str, Any], first: int, name: int) -> dict[str, int]:
    """Bytes of the element starting at token `first` and of its name token."""
    toks = stmt["tokens"]
    end = toks[element_end(toks, first) - 1].end + 1
    return {"start": to_byte(stmt, toks[first].start), "end": to_byte(stmt, end), "name_start": to_byte(stmt, toks[name].start), "name_end": to_byte(stmt, toks[name].end + 1)}


def _after_head(toks: list[Any]) -> int:
    """The index of the table name in `ALTER TABLE [IF EXISTS] [ONLY] name`."""
    i = 2
    while i < len(toks) and toks[i].name in ("IF_P", "EXISTS", "ONLY"):
        i += 1
    return i
