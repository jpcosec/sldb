# Model Reference

## Related Concepts

- [StructuredNLDoc Model](structurednldoc-model.atom.md)
- [Payload Inputs](payload-inputs.atom.md)
- [Store](store.atom.md)

## What It Is

A model reference is the Python import string that points to a `StructuredNLDoc` class. The required form is `module:ClassName`.

## Why It Matters

SLDB needs an unambiguous way to import the model contract that defines a document template, field schema, and semantics.

## How It Works

Commands such as `extract`, `render`, `validate`, and `models add` import the module, resolve the named class, and verify that it is a `StructuredNLDoc` subclass. If the module is in your project rather than installed, pass `--pythonpath`.

## When It Shows Up

You encounter model refs when registering a model, validating a model directly, or rendering/extracting without going through a store lookup.

## Where It Lives

The string lives in CLI input and in store metadata. The class itself lives in Python code such as `docs/models.py` or `src/myapp/docs.py`. <!-- gone -->

## Who Uses It

Anyone registering or directly invoking a model uses a model ref.
