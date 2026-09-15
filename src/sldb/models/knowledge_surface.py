"""Public knowledge-document model exports.

The selfdoc adapter derives interface facts from argparse and preserves authored
explanations. These import references remain stable for existing store models.
"""
from __future__ import annotations

from .anchor_doc import AnchorDoc
from .cli_command_doc import CliCommandDoc
from .knowledge_tag import KnowledgeTag
from .surface_doc import SurfaceDoc
from .python_symbol_doc import PythonSymbolDoc

__all__ = ["AnchorDoc", "CliCommandDoc", "KnowledgeTag", "PythonSymbolDoc", "SurfaceDoc"]
