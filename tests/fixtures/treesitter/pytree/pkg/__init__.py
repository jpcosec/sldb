"""Demo package used as a shared adapter fixture."""
import os
import sys, json
from . import sibling
from .core import Engine
from typing import TYPE_CHECKING

VERSION = "1"


def version() -> str:
    """Return the package version."""
    return VERSION
