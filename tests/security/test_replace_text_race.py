"""SEGURIDAD resto 2, r3: the TOCTOU of `replace_text`. The file is checked by the read guard, then
read and written; a race that swaps it for a symlink out of the root after the check is neither
read nor written through (`O_NOFOLLOW`): it fails as `store/symlink-not-read` and the outside
file keeps its bytes."""

from __future__ import annotations

import pytest

from sldb import api
from sldb.api.documents import replace_text as replace_module
from sldb.core.exceptions import SLDBDocumentTargetError, SLDBStoreError
from sldb.store.source_read import refuse_unreadable

SECRET = "outside, B body. here\n"


def _racing(target, secret):
    def check_then_swap(root, path):
        refuse_unreadable(root, path)
        target.unlink()
        target.symlink_to(secret)
    return check_then_swap


def test_a_symlink_swapped_in_after_the_check_is_not_read_nor_written_through(tmp_path, monkeypatch):
    root = tmp_path / "world"
    root.mkdir()
    store = api.init_store(root).store_path
    target = root / "plain.md"
    target.write_text("B body.\n", encoding="utf-8")
    secret = tmp_path / "secret.md"
    secret.write_text(SECRET, encoding="utf-8")
    monkeypatch.setattr(replace_module, "refuse_unreadable", _racing(target, secret))
    with pytest.raises(SLDBDocumentTargetError, match="store/symlink-not-read"):
        api.replace_text(store, "plain.md", "B body.", "PWNED")
    assert secret.read_text(encoding="utf-8") == SECRET


def test_a_swap_after_the_read_is_not_written_through(tmp_path, monkeypatch):
    """The transaction's write resolves the path inside the root (`transaction_paths.inside`) and
    opens it with `O_NOFOLLOW`: a symlink out of the root put there after the read is refused."""
    root = tmp_path / "world"
    root.mkdir()
    store = api.init_store(root).store_path
    target = root / "plain.md"
    target.write_text("B body.\n", encoding="utf-8")
    secret = tmp_path / "secret.md"
    secret.write_text(SECRET, encoding="utf-8")
    replaced = replace_module._replaced

    def replaced_then_swap(*args):
        out = replaced(*args)
        target.unlink()
        target.symlink_to(secret)
        return out
    monkeypatch.setattr(replace_module, "_replaced", replaced_then_swap)
    with pytest.raises((SLDBDocumentTargetError, SLDBStoreError)):
        api.replace_text(store, "plain.md", "B body.", "PWNED")
    assert secret.read_text(encoding="utf-8") == SECRET
