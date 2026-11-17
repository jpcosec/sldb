"""Pruebas propias del tester deskops-t-80f4da96f310 (no van al repo)."""
from __future__ import annotations
import importlib.util, sys
from pathlib import Path
from typing import Any

MCP = Path("/mnt/ssd/proyectos/SLDB_1/sldb/tests/mcp")
sys.path.insert(0, str(MCP))
spec = importlib.util.spec_from_file_location("mcp_conftest", MCP / "conftest.py")
mc = importlib.util.module_from_spec(spec); spec.loader.exec_module(mc)
built_world = mc.built_world
write_copy = mc.write_copy

from mcp_helpers import an_item, files, valid_edge, tracked  # noqa
from mcp_session import WRITER, served, tree_digest  # noqa


def apply(s, changes):
    return s.call("apply_changes", proposal=s.call("propose_changes", changes=changes)["proposal"])

def applied(s, changes):
    a = apply(s, changes); assert a["applied"] is True, a; return a

def retitled(item, title):
    return [{"action": "update", "model": item["model"], "name": item["name"], "fields": {"title": title}}]

def srv(root, level="2"):
    return served(root, "--level", level, "--actor", WRITER)


def test_e2e_two_batches_undo2_is_byte_identical(write_copy):
    with srv(write_copy) as s:
        item = an_item(s, write_copy); other = an_item(s, write_copy, with_dependency=False)
        victim = files(write_copy, "item")[-1]
        vdoc = tracked(s, write_copy, victim)
        before = tree_digest(write_copy)
        snap = {k: Path(k).read_bytes() for k in before}
        name = "tester-created"
        # lote 1: create + update ; lote 2: delete + assert_edge + update
        applied(s, [{"action": "create", "model": item["model"], "name": name, "payload": {**item["payload"], "title": "T", "depends_on": []}, "path": f"item/{name}.md"}, *retitled(item, "x1")])
        applied(s, [{"action": "delete", "model": vdoc["model"], "name": vdoc["name"]}, valid_edge(write_copy, "tester-edge"), *retitled(other, "x2")])
        assert tree_digest(write_copy) != before
        a = s.call("undo_changes", steps=2)
        assert a["applied"] is True and a["undone"] == 2 and a["remaining"] == 0, a
        after = tree_digest(write_copy)
        diff = {k for k in before.keys() | after.keys() if before.get(k) != after.get(k)}
        import difflib
        out = []
        for k in sorted(diff):
            a_ = snap.get(k, b"").decode(errors="replace").splitlines(); b_ = Path(k).read_bytes().decode(errors="replace").splitlines() if Path(k).exists() else []
            out.append("### " + k.split("world/")[-1]); out += list(difflib.unified_diff(a_, b_, lineterm="", n=0))
        Path("/dev/shm/undo-tester/bytediff.txt").write_text("\n".join(out))
        assert not diff, sorted(diff)


def test_foreign_write_then_undo_is_stale_and_writes_nothing(write_copy):
    with srv(write_copy) as s:
        item = an_item(s, write_copy)
        applied(s, retitled(item, "mine"))
        with srv(write_copy) as other:
            applied(other, retitled(item, "theirs"))
        before = tree_digest(write_copy)
        a = s.call("undo_changes")
        assert a["applied"] is False and a["rejected"] == "stale" and a["written"] is False and a["remaining"] == 1, a
        assert tree_digest(write_copy) == before


def test_new_server_has_no_stack(write_copy):
    with srv(write_copy) as s:
        applied(s, retitled(an_item(s, write_copy), "in old session"))
    with srv(write_copy) as fresh:
        before = tree_digest(write_copy)
        a = fresh.call("undo_changes")
        assert a["rejected"] == "nothing_to_undo" and a["remaining"] == 0, a
        assert tree_digest(write_copy) == before


def test_two_live_sessions_do_not_share_the_stack(write_copy):
    with srv(write_copy) as A, srv(write_copy) as B:
        ia = an_item(A, write_copy); ib = an_item(B, write_copy, with_dependency=False)
        applied(A, retitled(ia, "A1"))
        applied(B, retitled(ib, "B1"))
        nb = B.call("undo_changes", steps=2)
        assert nb["rejected"] == "nothing_to_undo" and nb["remaining"] == 1, nb
        ra = A.call("undo_changes")
        assert ra["applied"] is True and ra["remaining"] == 0, ra
        assert A.call("read_document", ref=ia["export_id"], field="title")["value"] == ia["payload"]["title"]
        assert A.call("read_document", ref=ib["export_id"], field="title")["value"] == "B1", "A undid B's batch"
        rb = B.call("undo_changes")
        assert rb["applied"] is True and rb["remaining"] == 0, rb
        assert B.call("read_document", ref=ib["export_id"], field="title")["value"] == ib["payload"]["title"]


def test_failed_apply_does_not_push_and_bad_steps_refused(write_copy):
    with srv(write_copy) as s:
        item = an_item(s, write_copy)
        prop = s.call("propose_changes", changes=retitled(item, "never"))["proposal"]
        with srv(write_copy) as other:
            applied(other, retitled(item, "meanwhile"))
        stale = s.call("apply_changes", proposal=prop)
        assert stale["applied"] is False, stale
        before = tree_digest(write_copy)
        for steps in (1, 0, -1):
            a = s.call("undo_changes", steps=steps)
            assert a["rejected"] == "nothing_to_undo" and a["written"] is False, (steps, a)
        assert tree_digest(write_copy) == before


def test_level_1_serves_undo_and_undo_is_not_redoable(write_copy):
    with srv(write_copy, "1") as s:
        item = an_item(s, write_copy)
        applied(s, retitled(item, "lvl1"))
        a = s.call("undo_changes")
        assert a["applied"] is True and a["remaining"] == 0, a
        assert s.call("undo_changes")["rejected"] == "nothing_to_undo"
        assert s.call("read_document", ref=item["export_id"], field="title")["value"] == item["payload"]["title"]
