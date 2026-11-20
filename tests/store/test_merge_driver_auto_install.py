"""The merge driver is installed when a store is prepared inside git, and `stores check` says when it is missing."""
from __future__ import annotations

import subprocess

from sldb.api import build_store, check_store, init_store, scaffold_store
from sldb.api.stores.store_declaration import save_declaration
from sldb.api.stores.declare_store import declare_store

LINES = [".sldb/core/store_index.yaml merge=sldb", ".sldb/core/models/*.yaml merge=sldb", ".sldb/store.yaml merge=sldb"]


def _git(root, *args, check=True):
    return subprocess.run(["git", *args], cwd=root, capture_output=True, text=True, check=check).stdout


def _driver(root):
    return _git(root, "config", "--get", "merge.sldb.driver", check=False).strip()


def _uninstall(root):
    (root / ".gitattributes").unlink(missing_ok=True)
    _git(root, "config", "--unset", "merge.sldb.driver", check=False)
    _git(root, "config", "--unset", "merge.sldb.name", check=False)


def _repo(tmp_path):
    _git(tmp_path, "init", "-q", "-b", "main")
    return tmp_path


def _codes(root):
    report = check_store(root / ".sldb", root)
    return [f["code"] for f in report["alerts"] + report["errors"]], report


def test_init_installs_the_driver_in_a_git_repo(tmp_path):
    root = _repo(tmp_path)
    init_store(root)
    assert (root / ".gitattributes").read_text(encoding="utf-8").splitlines() == LINES
    assert _driver(root) == "sldb stores merge-driver %O %A %B %P"


def test_scaffold_apply_installs_the_driver(tmp_path):
    root = _repo(tmp_path)
    init_store(root)
    save_declaration(root / ".sldb", declare_store(root / ".sldb", root))
    _uninstall(root)
    scaffold_store(root / ".sldb", apply=True)
    assert (root / ".gitattributes").read_text(encoding="utf-8").splitlines() == LINES
    assert _driver(root)


def test_build_installs_the_driver_and_twice_does_not_duplicate(tmp_path):
    root = _repo(tmp_path)
    init_store(root)
    save_declaration(root / ".sldb", declare_store(root / ".sldb", root))
    _uninstall(root)
    build_store(root / ".sldb")
    build_store(root / ".sldb")
    init_store(root, force=True)
    assert (root / ".gitattributes").read_text(encoding="utf-8").splitlines() == LINES
    assert _driver(root)


def test_outside_git_init_and_build_work_and_write_no_gitattributes(tmp_path):
    init_store(tmp_path)
    save_declaration(tmp_path / ".sldb", declare_store(tmp_path / ".sldb", tmp_path))
    build_store(tmp_path / ".sldb")
    assert not (tmp_path / ".gitattributes").exists()
    codes, _ = _codes(tmp_path)
    assert "merge-driver-missing" not in codes


def test_check_reports_a_missing_driver_until_it_is_installed(tmp_path):
    root = _repo(tmp_path)
    init_store(root)
    assert "merge-driver-missing" not in _codes(root)[0]
    _uninstall(root)
    codes, report = _codes(root)
    assert "merge-driver-missing" in codes
    found = next(f for f in report["alerts"] if f["code"] == "merge-driver-missing")
    assert found["fix"] == "sldb stores merge-driver --install"
    assert report["ok"] is True
    from sldb.api.stores.merge_driver_install import install_merge_driver

    install_merge_driver(root / ".sldb")
    assert "merge-driver-missing" not in _codes(root)[0]


def test_a_git_failure_only_warns(tmp_path, capsys, monkeypatch):
    root = _repo(tmp_path)

    def boom(_store):
        raise RuntimeError("git exploded")

    monkeypatch.setattr("sldb.api.stores.ensure_merge_driver.install_merge_driver", boom)
    init_store(root)
    assert "could not install the sldb merge driver" in capsys.readouterr().err
    assert (root / ".sldb").is_dir()
