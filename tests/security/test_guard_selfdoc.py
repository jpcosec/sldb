"""SEGURIDAD resto 2, selfdoc: knowledge/ is generated, so a symlink there (a symbol document
swapped for a link out of the root) is refused with a clear error naming its finding, never
read nor written through."""

from __future__ import annotations

import shutil
from pathlib import Path

from tests.security.audited import World, make_world

REPO = Path(__file__).resolve().parents[2]
PROJECT = f"""import shutil
from sldb import api
(root / 'src' / 'demo').mkdir(parents=True)
(root / 'src' / 'demo' / 'm.py').write_text('def kept():\\n    \\"\\"\\"Kept.\\"\\"\\"\\n', encoding='utf-8')
api.add_model(sp, 'sldb.models.relation_type_doc:RelationTypeDoc')
(root / 'types').mkdir()
for name in ('contains', 'imports', 'references'):
    shutil.copy({str(REPO)!r} + f'/sldb/relation_types/{{name}}.md', root / 'types' / f'{{name}}.md')
    api.track_document_file(sp, 'RelationTypeDoc', root / 'types' / f'{{name}}.md', name)
"""


def test_python_sync_refuses_a_symlinked_symbol_document(tmp_path):
    world = make_world(tmp_path)
    assert not world.api(PROJECT)["error"]
    argv = ("selfdoc", "python-sync", "--store", ".sldb", "--source-root", "src", "--system", "demo")
    assert world.cli(*argv)["code"] == 0
    symbol = next((world.root / "knowledge" / "symbols").glob("*kept*.md"))
    secret_before = world.secret.read_text(encoding="utf-8")
    symbol.unlink()
    symbol.symlink_to(world.secret)
    (world.root / "src" / "demo" / "m.py").write_text('def kept():\n    """Kept, changed."""\n', encoding="utf-8")
    ran = world.cli(*argv)
    assert not world.outside_opened(ran)
    assert ran["code"] != 0 and "store/path-outside-root" in ran["output"] and "Traceback" not in ran["output"]
    assert world.secret.read_text(encoding="utf-8") == secret_before
