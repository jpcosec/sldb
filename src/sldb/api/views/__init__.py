"""Composed views (GD25): a `ViewDoc` with `sections` evaluated over a store.

`run_view` is the evaluation, `list_views` the catalogue (`docs/architecture/views.md`). There
is no extension point in Python: no view provider, no field derived by consumer code (DA1)."""

from sldb.api.views.list_views import list_views
from sldb.api.views.run_view import run_view

__all__ = ["list_views", "run_view"]
