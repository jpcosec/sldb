# Current CLI Tree

```text
sldb
├── extract <model-ref> <input-md> <output-json|yaml> [--format json|yaml] [--pythonpath PATH]
├── render <model-ref> <input-data> <output-md> [--pythonpath PATH]
├── validate <model-ref> (--input FILE | --data FILE) [--format text|json|yaml] [--pythonpath PATH]
├── init [path] [--force]
├── example [path]
├── store
│   ├── init [--path PATH] [--force]
│   ├── add <path> [--name NAME] [--store PATH]
│   ├── check [--store PATH] [--format text|json|yaml] [--pythonpath PATH]
│   └── update [--store PATH] [--pythonpath PATH]
├── model
│   ├── add <model-ref> [--store PATH] [--pythonpath PATH]
│   └── update <name> [--store PATH] [--pythonpath PATH]
└── doc
    ├── add --model NAME -o PATH <payload> [--name NAME] [--store PATH] [--pythonpath PATH]
    ├── track <path> --model NAME [--name NAME] [--store PATH] [--pythonpath PATH] [--force]
    └── update <name> --model NAME <payload> [--store PATH] [--pythonpath PATH]
```

## Command Groups

- direct document workflows: `extract`, `render`, `validate`
- project bootstrapping: `init`, `example`
- store registry workflows: `store ...`
- model contract workflows: `model ...`
- document instance workflows: `doc ...`
