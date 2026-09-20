from sldb.core.exceptions.sldb_error import SLDBError


class SLDBGraphCycleError(SLDBError):
    """A relation asked to be ordered is not a DAG: the cycle is in `cycle`."""

    def __init__(self, cycle: list[str]) -> None:
        super().__init__("Relation is not acyclic: " + " -> ".join([*cycle, cycle[0]]))
        self.cycle = cycle
