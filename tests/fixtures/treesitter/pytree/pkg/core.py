"""Core module: classes, methods, nested functions."""
from __future__ import annotations

import os
import os
from collections import OrderedDict


def plain(a, b=2):
    return a + b


def configured(
    first: int,
    second: str = "x",
    *args,
    flag: bool = False,
    **kwargs,
) -> dict:
    """Multi-line signature with defaults, annotations, *args and **kwargs.

    Second paragraph.
    """

    def inner(x):
        """Nested function."""

        def deepest():
            return x

        return deepest

    return {"inner": inner}


async def fetch(url: str, *, timeout: float = 1.5) -> bytes:
    """Async function."""
    return b""


def decorated_once(fn):
    return fn


@decorated_once
@staticmethod
def decorated(x):
    """Decorated function: lineno is the def line, not the decorator."""
    return x


class Engine:
    """An engine."""

    limit = 3

    def __init__(self, name):
        self.name = name

    def start(self, speed: int = 1) -> None:
        """Start it."""

    async def stop(self):
        pass

    @property
    def label(self):
        return self.name

    @label.setter
    def label(self, value):
        self.name = value

    class Inner:
        def method(self):
            """Method of a nested class."""


class _Hidden:
    def _private(self):
        pass


if os.name == "nt":

    def windows_only():
        """Defined under an if: not walked."""


try:
    import tomllib
except ImportError:
    tomllib = None

lam = lambda x: x
