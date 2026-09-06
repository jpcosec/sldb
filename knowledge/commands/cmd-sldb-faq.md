---
id: cmd-sldb-faq
system: sldb
command_path: faq
synopsis: Browse the first-use FAQ by question.
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_command
provenance: src/sldb/cli/parsers/
---

# faq

## Synopsis

Browse the first-use FAQ by question.

## Purpose

The `sldb faq` command: Browse the first-use FAQ by question.

## How It Works

Implemented under src/sldb/cli/parsers/ as the argparse subcommand 'faq'. It parses the listed arguments and dispatches to its handler in the sldb CLI runtime over the .sldb store.

## Arguments

question | optional | Question index, slug, or text fragment.
--format | optional | 
--faq-path | optional | FAQ markdown path

## Usage

faq
