from __future__ import annotations
import argparse
from .stores import add_stores_group
from .models1 import add_models_group
from .predicates import add_predicates_group
from .docs1 import add_docs_group
from .fields import add_fields_group
from .sections import add_sections_group
from .edges import add_edges_group

def add_public_group_commands(s: argparse._SubParsersAction) -> None:
    add_stores_group(s)
    add_models_group(s)
    add_predicates_group(s)
    add_docs_group(s)
    add_fields_group(s)
    add_sections_group(s)
    add_edges_group(s)
