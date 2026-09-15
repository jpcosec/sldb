from __future__ import annotations

from sldb.store.catalog_reconcile import reconcile_catalog
from sldb.store.io import save_store_index, load_store_index
from sldb.store.models import StoreEntry, StoreIndex


def test_reconcile_reports_and_applies_only_when_requested(tmp_path):
    catalog, project = tmp_path / "catalog" / ".sldb", tmp_path / "projects" / "one" / ".sldb"
    save_store_index(catalog, StoreIndex(stores=[StoreEntry(name="gone", path=str(tmp_path / "gone" / ".sldb"))]))
    save_store_index(project, StoreIndex())
    report = reconcile_catalog(catalog, tmp_path / "projects", apply=False)
    assert report["missing"] == [str(project)] and report["stale"] == [str(tmp_path / "gone" / ".sldb")]
    reconcile_catalog(catalog, tmp_path / "projects", apply=True)
    assert [(entry.name, entry.path) for entry in load_store_index(catalog).stores] == [("one", str(project))]
