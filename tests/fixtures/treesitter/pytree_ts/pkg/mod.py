'''Module doc
   indented second line.
'''
from __future__ import annotations
import os, sys as system
import a.b.c
from .. import x
from ..rel import y as z
from pkg.sub import (a,
    b)

CONST = 1


def plain(a, b=1, *args, c: int = 2, d: "str" = "x", **kw) -> int:
    """Plain doc.

        Indented body.
    """
    def inner():
        class InnerCls:
            pass
    return 1  # trailing


@decorator
@other(arg=1)
async def decorated(x, /, y, *, z):
    r"""raw \d doc"""


class Outer(Base):
    "single quoted doc\n\tsecond"

    attr = 1

    def method(self): pass

    @staticmethod
    def sm(): return 1

    @property
    async def am(self):
        'implicit' " concat" \
        ' joined'

    class Nested:
        def deep(self):
            """deep"""
            # trailing comment inside

# comment after class


if True:
    def conditional(): pass

try:
    import json
except ImportError:
    def fallback(): pass


def plain(again):
    f"{x} not a doc"


def bytes_doc():
    b"bytes"


def not_first():
    x = 1
    """not doc"""


def unicode_é():
    """ünïcode ✓"""


def multi(
    a,
    b,   # comment
    c=[1,
       2],
):
    pass


lam = lambda q: q
