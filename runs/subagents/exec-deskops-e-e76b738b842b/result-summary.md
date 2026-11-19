# Result
Cause: argparse in newer 3.12 patch releases no longer marks a defaultless nargs="*" positional as required; selfdoc read action.required directly.
Fix: src/sldb/selfdoc/arguments.py `_required()` normalizes that case to True (historical value, matches committed reference). Test: tests/selfdoc/test_argument_required.py.
Validation: see validation.log (selfdoc check changed=[], check.sh --fast rc 0).
Limitation: could not run the host python (/usr/bin/python3.12 absent in container); verified by simulating required=False in the test.
Files: src/sldb/selfdoc/arguments.py, tests/selfdoc/test_argument_required.py
