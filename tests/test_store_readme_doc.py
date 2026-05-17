from pathlib import Path
import sys

from pydantic import Field

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from docs.models import StoreReadmeDoc
from sldb import StructuredNLDoc
from sldb.runtime.validation import extract_model_data, render_model_markdown


class SectionedDoc(StructuredNLDoc):
    __template__ = """
# ⸢rev•title⸥

## First

⸢rev•first⸥

## Second

⸢rev•second⸥
""".strip()

    title: str = Field(description="Document title.")
    first: str = Field(description="First section body.")
    second: str = Field(description="Second section body.")


def test_store_readme_roundtrips_current_markdown() -> None:
    markdown = Path(".sldb/README.md").read_text(encoding="utf-8")

    payload = extract_model_data(StoreReadmeDoc, markdown)
    rendered = render_model_markdown(StoreReadmeDoc, payload)
    extracted_again = extract_model_data(StoreReadmeDoc, rendered)

    assert payload == extracted_again
    assert payload["title"] == "SLDB Store Workspace"
    assert payload["purpose"].startswith("`.sldb/` is the project-local SLDB workspace")
    assert "Commit `.sldb/core`" in payload["git_policy"]
    assert (
        "`python -m sldb models add <module:Model> --store .sldb --pythonpath .`"
        in payload["command_map"]
    )


def test_section_capture_extracts_full_markdown_sections() -> None:
    markdown = """# Example

## First

First paragraph.

- one
- two

## Second

Second paragraph.

```text
code block
```
"""

    payload = extract_model_data(SectionedDoc, markdown)
    rendered = render_model_markdown(SectionedDoc, payload)
    extracted_again = extract_model_data(SectionedDoc, rendered)

    assert payload == extracted_again
    assert payload["first"] == "First paragraph.\n\n- one\n- two"
    assert payload["second"] == "Second paragraph.\n\n```text\ncode block\n```"
