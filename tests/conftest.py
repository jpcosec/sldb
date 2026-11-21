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


@pytest.fixture(autouse=True)
def _no_machine_catalog(tmp_path_factory, monkeypatch):
    """Links resolve by name through the machine's catalog (the global store) when their path is
    not there. A test must not see the stores of whoever runs it: without this, a link named like
    one of the developer's own stores resolved to it and the absent-link tests passed or failed
    by machine."""
    nowhere = tmp_path_factory.mktemp("no-catalog") / ".sldb"
    monkeypatch.setattr("sldb.store.catalog._catalog_path", lambda: nowhere)
