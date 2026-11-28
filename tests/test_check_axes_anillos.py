"""La puerta de anillos y de tamaño: lo nuevo falla, lo vencido falla, lo vigente pasa."""

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location("check_axes", ROOT / "tools" / "check_axes.py")
check_axes = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(check_axes)

AXES = [{"id": "dentro", "ring": "0a"}, {"id": "fuera", "ring": "2"}]
NO_DEBT = {"import": {}, "size": {}}


def _tree(tmp_path, monkeypatch, files: dict[str, str]):
    for rel, text in files.items():
        (tmp_path / rel).parent.mkdir(parents=True, exist_ok=True)
        (tmp_path / rel).write_text(text, encoding="utf-8")
    monkeypatch.setattr(check_axes, "SRC", tmp_path)
    return {"a.py": "dentro", "b.py": "fuera"}


def test_inward_import_is_not_a_violation(tmp_path, monkeypatch):
    owner = _tree(tmp_path, monkeypatch, {"a.py": "", "b.py": "from sldb.a import x\n"})
    assert check_axes.ring_violations(AXES, owner) == set()


def test_outward_import_is_found_even_relative_and_deferred(tmp_path, monkeypatch):
    owner = _tree(tmp_path, monkeypatch, {"a.py": "def f():\n    from . import b\n", "b.py": ""})
    assert check_axes.ring_violations(AXES, owner) == {("a.py", "b")}


def test_type_checking_import_is_ignored(tmp_path, monkeypatch):
    src = "from typing import TYPE_CHECKING\nif TYPE_CHECKING:\n    from sldb.b import x\n"
    owner = _tree(tmp_path, monkeypatch, {"a.py": src, "b.py": ""})
    assert check_axes.ring_violations(AXES, owner) == set()


def test_violation_not_in_debt_fails(tmp_path, monkeypatch):
    owner = _tree(tmp_path, monkeypatch, {"a.py": "from sldb.b import x\n", "b.py": ""})
    problems = check_axes.anillos_problems(AXES, owner, NO_DEBT)
    assert len(problems) == 1 and "nuevo" in problems[0]


def test_stale_debt_entry_fails(tmp_path, monkeypatch):
    owner = _tree(tmp_path, monkeypatch, {"a.py": "", "b.py": ""})
    problems = check_axes.anillos_problems(AXES, owner, {"import": {"a.py -> b": 0}, "size": {}})
    assert len(problems) == 1 and "vencido" in problems[0]


def test_listed_violation_passes(tmp_path, monkeypatch):
    owner = _tree(tmp_path, monkeypatch, {"a.py": "from sldb.b import x\n", "b.py": ""})
    assert check_axes.anillos_problems(AXES, owner, {"import": {"a.py -> b": 0}, "size": {}}) == []


def test_axis_without_ring_fails():
    assert "ring" in check_axes.anillos_problems([{"id": "x"}], {}, NO_DEBT)[0]


def test_long_function_is_an_offender_and_debt_can_only_shrink(tmp_path, monkeypatch):
    _tree(tmp_path, monkeypatch, {"a.py": "def largo():\n" + "    x = 1\n" * 45, "b.py": ""})
    found = check_axes.size_offenders(["a.py", "b.py"])
    assert found == {"a.py::largo": 46}
    assert "nuevo" in check_axes.debt_problems(found, {}, "t")[0]
    assert check_axes.debt_problems(found, {"a.py::largo": 46}, "t") == []
    assert "creció" in check_axes.debt_problems(found, {"a.py::largo": 45}, "t")[0]
    assert "encogió" in check_axes.debt_problems(found, {"a.py::largo": 60}, "t")[0]
    assert "vencido" in check_axes.debt_problems({}, {"a.py::largo": 46}, "t")[0]


def test_long_file_is_an_offender(tmp_path, monkeypatch):
    _tree(tmp_path, monkeypatch, {"a.py": "x = 1\n" * 301})
    assert check_axes.size_offenders(["a.py"]) == {"a.py": 301}


def test_file_claimed_by_two_axes_is_found(tmp_path, monkeypatch):
    _tree(tmp_path, monkeypatch, {"x/a.py": "", "x/b.py": ""})
    axes = [{"id": "uno", "paths": ["x"]}, {"id": "dos", "paths": ["x/a.py"]}]
    assert check_axes.duplicate_claims(axes) == {"x/a.py": ["uno", "dos"]}


def test_disjoint_axes_have_no_duplicate_claims(tmp_path, monkeypatch):
    _tree(tmp_path, monkeypatch, {"x/a.py": "", "y/b.py": ""})
    axes = [{"id": "uno", "paths": ["x"]}, {"id": "dos", "paths": ["y", "x/ausente.py"]}]
    assert check_axes.duplicate_claims(axes) == {}


def test_real_repo_has_no_file_in_two_axes():
    assert check_axes.duplicate_claims(check_axes.load()["axis"]) == {}


NO_GIT_DEBT = {"import": {}, "size": {}, "git": {}}
RUN_GIT = "import subprocess\n\n\ndef f():\n    return subprocess.run([\"git\", \"log\"], capture_output=True)\n"


def test_git_call_inside_the_ports_axis_passes(tmp_path, monkeypatch):
    _tree(tmp_path, monkeypatch, {"ports/git.py": RUN_GIT})
    assert check_axes.ports_problems({"ports/git.py": "puertos"}, NO_GIT_DEBT) == []


def test_git_call_outside_the_ports_axis_fails(tmp_path, monkeypatch):
    _tree(tmp_path, monkeypatch, {"ports/git.py": "", "api/x.py": RUN_GIT})
    problems = check_axes.ports_problems({"ports/git.py": "puertos", "api/x.py": "fuera"}, NO_GIT_DEBT)
    assert len(problems) == 1 and "nuevo" in problems[0] and "api/x.py" in problems[0]


def test_git_call_in_an_unmapped_file_also_fails(tmp_path, monkeypatch):
    _tree(tmp_path, monkeypatch, {"cli/x.py": "from subprocess import run\nrun(['git', 'status'])\n"})
    assert "cli/x.py" in check_axes.ports_problems({}, NO_GIT_DEBT)[0]


def test_non_git_subprocess_passes(tmp_path, monkeypatch):
    src = "import subprocess\nsubprocess.run(['ls'])\nsubprocess.run(split('git x'))\nsubprocess.Popen(argv)\n"
    _tree(tmp_path, monkeypatch, {"api/x.py": src})
    assert check_axes.ports_problems({"api/x.py": "fuera"}, NO_GIT_DEBT) == []


def test_git_debt_can_only_shrink(tmp_path, monkeypatch):
    _tree(tmp_path, monkeypatch, {"api/x.py": RUN_GIT})
    owner = {"api/x.py": "fuera"}
    assert check_axes.ports_problems(owner, {**NO_GIT_DEBT, "git": {"api/x.py": 1}}) == []
    assert "encogió" in check_axes.ports_problems(owner, {**NO_GIT_DEBT, "git": {"api/x.py": 2}})[0]
    stale = check_axes.ports_problems(owner, {**NO_GIT_DEBT, "git": {"api/x.py": 1, "api/y.py": 1}})
    assert len(stale) == 1 and "vencido" in stale[0]


def test_real_repo_runs_git_only_through_the_ports():
    contract = check_axes.load()
    owner, _ = check_axes.owner_map(contract["axis"])
    assert check_axes.ports_problems(owner, check_axes.load_debt()) == []


def test_real_repo_gates_pass():
    contract = check_axes.load()
    owner, _ = check_axes.owner_map(contract["axis"])
    debt = check_axes.load_debt()
    assert check_axes.anillos_problems(contract["axis"], owner, debt) == []
    assert check_axes.size_problems(owner, debt) == []
