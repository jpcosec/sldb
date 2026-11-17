"""The closed catalog of signal classes: what a request can ask for that does not exist."""

from __future__ import annotations

UNKNOWN_TOOL = "unknown_tool"
UNKNOWN_ARGUMENT = "unknown_argument"
NOT_IMPLEMENTED = "not_implemented"

CLASSES = (UNKNOWN_TOOL, "unknown_model", "unknown_document", "unknown_field", "unknown_relation", "unknown_view", UNKNOWN_ARGUMENT, NOT_IMPLEMENTED)

#: Tools that are declared but not served yet, and what they wait for. Calling one is a signal.
PENDING_TOOLS: dict[str, str] = {}

#: How many suggestions an answer carries.
SUGGESTIONS = 5
