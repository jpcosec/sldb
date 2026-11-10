"""What a store's surroundings say, as findings: its declaration, links, contents and ignores.

Errors: a declared store that was never built (`stores check` passed on it with 0 documents,
inbox 20261020-024137), a link to no store, and structural noise, which the writes already
refuse (owner's decision, 2026-10-20). Alerts: blocks a rewrite would lose, a model shadowing
its owner's, and the cache not ignored by git. Error too: `.sldb/` ignored, since its past is read from git.
"""

from __future__ import annotations

from pathlib import Path

from sldb.core.finding import Finding, alert, error

_NOISE_FIX = "create a model that inherits it and declares those sections as optrev fields"


def unbuilt(store_path: Path) -> Finding | None:
    """A store whose declaration names models while its index has none (or no index at all)."""
    from sldb.api.stores.store_declaration import declaration_path, load_declaration
    from sldb.store.io import load_store_index
    from sldb.store.layout import store_exists

    if not declaration_path(store_path).is_file() or not load_declaration(store_path).models:
        return None
    if store_exists(store_path) and load_store_index(store_path).models:
        return None
    return error("store/unbuilt", str(store_path), "the store is declared (.sldb/store.yaml) but not built", "sldb stores build")


def surroundings_findings(store_path: Path, root: Path, pythonpath: str | None) -> list[Finding]:
    if found := unbuilt(store_path):
        return [found]
    return [*_links(store_path), *_noise(store_path, root, pythonpath), *_rewrite_loss(store_path, root, pythonpath), *_shadowed(store_path, pythonpath), *_gitignore(store_path)]


def _links(store_path: Path) -> list[Finding]:
    from sldb.api.stores.store_links import store_links

    fix = "sldb stores add <path> --name {0} --replace   (or `sldb stores remove {0}`)"
    return [_link_finding(link, fix.format(link["name"])) for link in store_links(store_path) if link["status"] != "ok"]


def _link_finding(link: dict, fix: str) -> Finding:
    """A link whose directory is absent (a sibling repository not checked out, as in a CI runner)
    is `store/link-absent`, an alert by default that names the link and its path; a link to a
    directory that holds no store is `store/link-broken`, an error."""
    what = f"the linked store is {link['status']}: {link['resolved']}"
    if link["status"] == "missing":
        return alert("store/link-absent", link["name"], what, fix)
    return error("store/link-broken", link["name"], what, fix)


def _noise(store_path: Path, root: Path, pythonpath: str | None) -> list[Finding]:
    from sldb.api.stores.scan_structural_noise import scan_structural_noise

    return [error("store/structural-noise", f"{r.model}:{r.document}", f"{len(r.undeclared)} heading(s) the model does not declare: {', '.join(r.undeclared)}", _NOISE_FIX, r.document) for r in scan_structural_noise(store_path, root, pythonpath)]


def _rewrite_loss(store_path: Path, root: Path, pythonpath: str | None) -> list[Finding]:
    from sldb.api.stores.scan_rewrite_loss import scan_rewrite_loss

    what = "{n} block(s) its model does not read would be lost on a rewrite ({path})"
    return [alert("store/rewrite-loss", f"{i['model']}:{i['document']}", what.format(n=len(i["lost"]), path=i["path"]), "move that content into a field the model declares", i["document"]) for i in scan_rewrite_loss(store_path, root, pythonpath)]


def _shadowed(store_path: Path, pythonpath: str | None) -> list[Finding]:
    from sldb.api.model_registry.model_reference import same_model_class
    from sldb.store.model_origin import shadowed_models

    found = shadowed_models(store_path, lambda a, b: same_model_class(a, b, pythonpath))
    return [alert("store/model-shadowed", s["model"], f"{'a copy of' if s['copy'] else 'another class under the name of'} the model the store linked as '{s['store']}' owns", f"sldb models inherit {s['store']}:{s['model']}" if s["copy"] else "give the override a name of its own") for s in found]


def _gitignore(store_path: Path) -> list[Finding]:
    """`.sldb/` ignored is an error (the store's past is read from git, so nothing of it may be
    ignored); the cache not ignored is an alert (it is regenerable, and would be versioned)."""
    from sldb.api.stores.gitignore_policy import gitignore_policy

    policy = gitignore_policy(Path(store_path))
    if policy is None:
        return []
    ignored = [path for path, bad in ((".sldb/core/", policy["core_ignored"]), (".sldb/store.yaml", policy["declaration_ignored"])) if bad]
    found = [error("stores/core_ignored", ".gitignore", f"git ignores {', '.join(f'`{p}`' for p in ignored)}: the store is versioned whole, its past is read from git", "remove that rule from the root .gitignore (`sldb stores migrate-layout` rewrites it)")] if ignored else []
    if not policy["cache_ignored"]:
        found.append(alert("stores/cache_not_ignored", ".gitignore", "`.sldb_cache/` is not ignored by git: it is regenerable and must not be versioned", "add the line `.sldb_cache/` to the root .gitignore (`sldb stores init` and `sldb stores migrate-layout` write it)"))
    return found
