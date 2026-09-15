"""Existing model import references survive definition modularization."""
from types import SimpleNamespace

from sldb.cli.commands.models_utils import registered_model_source
from sldb.cli.main import main
from sldb.models.knowledge_surface import CliCommandDoc, SurfaceDoc, AnchorDoc
from sldb.models.cli_command_doc import CliCommandDoc as CommandDefinition
from sldb.models.surface_doc import SurfaceDoc as SurfaceDefinition
from sldb.models.anchor_doc import AnchorDoc as AnchorDefinition
from sldb.store.io import load_store_index, save_store_index


def test_public_model_exports_keep_identity():
    assert (CliCommandDoc, SurfaceDoc, AnchorDoc) == (CommandDefinition, SurfaceDefinition, AnchorDefinition)


def test_old_registry_path_follows_public_reexports_to_editable_definition(project, invoke, capsys):
    assert invoke("sync")[0] == 0
    store = project / ".sldb"
    index = load_store_index(store)
    from pathlib import Path
    import sldb.models.knowledge_surface as exports
    entry = next(e for e in index.models if e.name == "CliCommandDoc")
    entry.path = str(Path(exports.__file__))
    save_store_index(store, index)
    path, module, attr = registered_model_source(SimpleNamespace(store=str(store), model="CliCommandDoc", pythonpath=None))
    assert path.name == "cli_command_doc.py"
    assert attr == "CliCommandDoc"
    assert module == "sldb.models.cli_command_doc"
    assert main(["models", "template", "show", "CliCommandDoc", "--store", str(store)]) == 0
    assert "⸢rev•command_path⸥" in capsys.readouterr().out
