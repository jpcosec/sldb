"""`required` for argparse positionals must not depend on the Python patch version."""
import argparse
from sldb.selfdoc.arguments import argument_record


def test_star_positional_without_default_is_required(monkeypatch):
    p = argparse.ArgumentParser()
    action = p.add_argument("files", nargs="*")
    action.required = False  # what newer Python patch releases produce
    assert argument_record(action).required is True


def test_star_positional_with_default_and_options_unchanged():
    p = argparse.ArgumentParser()
    star = p.add_argument("files", nargs="*", default=[])
    star.required = False
    assert argument_record(star).required is False
    assert argument_record(p.add_argument("--x")).required is False
