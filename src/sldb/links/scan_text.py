"""The text of a Markdown document that the link scan reads: everything but its code.

markdown-it decides what is code, with the parser of `sldb.core.ast` ("gfm-like" plus the
front matter plugin). Fenced (`fence`) and indented (`code_block`) blocks and inline code
(`code_inline`) give no text; the front matter gives its source lines, opening line included;
the rest of the document is kept in order, one block per line.
"""
from __future__ import annotations

import re

# Between two inline pieces cut by code: a `]` between NULs, so no [[...]] spans the code and
# the gap never closes one either.
CODE_GAP = "\x00]\x00"
# Inline tokens whose `markup` is their source text: escapes and entities (`text_special`,
# kept unjoined so `\[` stays `\[`) and the delimiters of emphasis and strikethrough.
MARKUP_TOKENS = frozenset({"text_special", "em_open", "em_close", "strong_open", "strong_close", "s_open", "s_close"})
BREAK_TOKENS = frozenset({"softbreak", "hardbreak"})
RAW_BLOCKS = frozenset({"html_block"})
# The line ends of markdown-it (`token.map` counts these), not those of str.splitlines.
LINE_END = re.compile(r"\r\n|\r|\n")

_PARSER = None


def _parser():
    """The markdown-it of `sldb.core.ast` (the surface axis owns that dependency) with two core
    rules off that only rewrite inline text: text_join (escapes stay as written) and linkify (a
    URL stays as written; it also halves the parse time). The blocks are the same."""
    global _PARSER
    if _PARSER is None:
        from sldb.core.ast.markdown_ast_handler import MarkdownASTHandler
        _PARSER = MarkdownASTHandler().md.disable(["text_join", "linkify"])
    return _PARSER


def _inline_piece(token) -> str:
    if token.type == "code_inline":
        return CODE_GAP
    if token.type in BREAK_TOKENS:
        return "\n"
    if token.type in MARKUP_TOKENS:
        return token.markup
    if token.children:
        return _inline_text(token.children)
    return token.content


def _inline_text(children) -> str:
    return "".join(_inline_piece(child) for child in children)


def _block_text(token, lines: list[str]) -> str | None:
    if token.type == "inline":
        return _inline_text(token.children or [])
    if token.type == "front_matter":
        # its source lines: `content` drops the opening line, and text after a `---` on line 0
        return "\n".join(lines[token.map[0]:token.map[1]])
    if token.type in RAW_BLOCKS:
        return token.content
    return None


def scannable_text(markdown: str) -> str:
    """The document without its code, for the link patterns of `sldb.links.parser`."""
    lines = LINE_END.split(markdown)
    blocks = (_block_text(token, lines) for token in _parser().parse(markdown))
    return "\n".join(text for text in blocks if text is not None)
