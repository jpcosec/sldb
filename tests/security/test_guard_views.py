"""SEGURIDAD resto 2, views: `list_views` (every view) never opens a ViewDoc whose path is a symlink
out of the root, warns with its finding and lists the others; `run_view` of that one fails with
its finding (`store/path-outside-root`)."""

from __future__ import annotations

import pytest

from tests.security.audited import make_world

VIEWS = """from sldb import api
api.add_model(sp, 'sldb.models.notation_models:ViewDoc', py)
for name in ('board', 'other'):
    api.create_document(sp, 'ViewDoc', root / 'views' / f'{name}.md', {'id': name, 'name': name, 'title': name, 'sections': [{'key': 'memos', 'select': {'model': 'Memo'}, 'fields': ['title']}]}, name, py)
"""


@pytest.fixture
def world(tmp_path):
    made = make_world(tmp_path)
    assert not made.api(VIEWS)["error"]
    (made.root / "views" / "board.md").unlink()
    (made.root / "views" / "board.md").symlink_to(made.secret)
    return made


def test_list_views_does_not_open_the_symlink_warns_and_lists_the_others(world):
    ran = world.api("from sldb import api\nresult = [v['name'] for v in api.list_views(sp)]")
    assert not world.outside_opened(ran) and not ran["error"]
    assert ran["result"] == ["other"] and "store/path-outside-root" in ran["output"]


def test_running_the_symlinked_view_fails_with_its_finding(world):
    ran = world.api("from sldb import api\nresult = api.run_view(sp, 'board')")
    assert not world.outside_opened(ran)
    assert ran["error"].startswith("SLDBDocumentTargetError") and "store/path-outside-root" in ran["error"]
