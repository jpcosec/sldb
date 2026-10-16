import os

import pytest


def pytest_configure():
    os.environ.setdefault("SLDB_SUPPRESS_DEPRECATION", "1")


@pytest.fixture(autouse=True)
def _private_user_cache(tmp_path_factory, monkeypatch):
    """Each test gets its own `$XDG_CACHE_HOME`: the derived caches are keyed by store path, and
    pytest reuses tmp paths across runs, so a shared `~/.cache/sldb` let one run read another's
    entries (test_cache_identity failed on some machines and passed on others)."""
    monkeypatch.setenv("XDG_CACHE_HOME", str(tmp_path_factory.mktemp("xdg-cache")))
