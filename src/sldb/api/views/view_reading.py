"""What one `run_view` evaluation reads, loaded once and shared by every section and row (H11:
the calling store's edge index, widened to the linked stores only when the view needs them)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from sldb.api.edges.edge_reading import load_edge_index
from sldb.api.edges.project_graph.store_project_graph import project_graph
from sldb.api.rules.rule_graph import rule_graph
from sldb.api.rules.rules_on_transition import has_rules
from sldb.api.stores.store_declaration import load_declaration
from sldb.api.views.list_views import load_view
from sldb.api.views.view_rules import SharedRules
from sldb.core.exceptions import SLDBDocumentTargetError


class ViewReading:
    """What one evaluation reads, loaded once and shared by every section and row."""

    def __init__(self, store_path: Path) -> None:
        self.store_path = store_path
        self.index = load_edge_index(store_path, include_linked=False)
        self.linked = False
        self.rows: set[str] = set()
        self.rule_ids: list[str] = []
        self._rules: SharedRules | None = None
        self._transitions: tuple | None = None
        self._project: Any = None
        self._project_read = False

    def widen(self) -> None:
        """Read the linked stores too, from here on (H11: a view that names none never does)."""
        if not self.linked:
            self.index, self.linked = load_edge_index(self.store_path, include_linked=True), True

    def view(self, name: str) -> tuple[Any, Any]:
        """The ViewDoc `name` and its node: the calling store's own, else (H9) a linked one's,
        which widens the index to the linked stores."""
        try:
            return load_view(name, self.index)
        except SLDBDocumentTargetError:
            if self.linked:
                raise
            self.widen()
            return load_view(name, self.index)

    def rules(self) -> SharedRules:
        if self._rules is None:
            self._rules = SharedRules(rule_graph(self.store_path))
        return self._rules

    def transition_rules(self) -> tuple | None:
        """`(rules, on_transition rules)`, or None in a store without RuleDoc (then no rule
        runs, as in `edges_holding`)."""
        if self._transitions is None and has_rules(self.store_path):
            self._transitions = (self.rules(), [r for r in self.rules().rules() if r.get("moment") == "on_transition"])
        return self._transitions

    def project(self) -> Any:
        """The declared project graph (GD21), or None when `store.yaml` is absent or declares none."""
        if not self._project_read:
            self._project_read = True
            self._project = project_graph(self.store_path) if declares_project_graph(self.store_path) else None
        return self._project


def declares_project_graph(store_path: Path) -> bool:
    try:
        return load_declaration(store_path).project_graph is not None
    except FileNotFoundError:
        return False
