from __future__ import annotations

import os
import threading
from pathlib import Path

from sldb.store.io.utils import StoreIOUtils


def test_atomic_write_closes_each_descriptor_exactly_once(tmp_path, monkeypatch):
    """A double close is a descriptor race: the number can be recycled between the two closes."""
    closed: list[int] = []
    real_close = os.close

    def tracked_close(fd):
        closed.append(fd)
        return real_close(fd)

    monkeypatch.setattr(os, "close", tracked_close)
    StoreIOUtils._atomic_write(tmp_path / "index.yaml", "a: 1\n")

    assert len(closed) == 1
    assert (tmp_path / "index.yaml").read_text() == "a: 1\n"


def test_atomic_write_survives_concurrent_writers(tmp_path):
    """Many writers of the same path must leave a valid file and no descriptor error."""
    target = tmp_path / "index.yaml"
    errors: list[BaseException] = []

    def write(value: int) -> None:
        try:
            for _ in range(50):
                StoreIOUtils._atomic_write(target, f"a: {value}\n")
        except BaseException as error:  # noqa: BLE001 - collected and asserted below
            errors.append(error)

    threads = [threading.Thread(target=write, args=(value,)) for value in range(4)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    assert errors == []
    assert target.read_text().startswith("a: ")
    assert list(Path(tmp_path).glob("*.tmp")) == []
