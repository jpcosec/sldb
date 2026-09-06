---
id: cmd-sldb-lint
system: sldb
command_path: lint
synopsis: Lint knowledge references for canonical paths.
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_command
provenance: src/sldb/cli/parsers/
---

# lint

## Synopsis

Lint knowledge references for canonical paths.

## Purpose

The `sldb lint` command: Lint knowledge references for canonical paths.

## How It Works

Implemented under src/sldb/cli/parsers/ as the argparse subcommand 'lint'. It parses the listed arguments and dispatches to its handler in the sldb CLI runtime over the .sldb store.

## Arguments

target | optional | File or directory to lint (default: recursive scan of repo)
--repo-root | optional | Repository root path (default: auto-detect from cwd)
--format | optional | 

## Usage

lint
