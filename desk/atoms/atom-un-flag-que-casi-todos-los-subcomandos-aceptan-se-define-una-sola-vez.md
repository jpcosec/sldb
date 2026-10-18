---
id: atom-un-flag-que-casi-todos-los-subcomandos-aceptan-se-define-una-sola-vez
title: Un flag que casi todos los subcomandos aceptan se define una sola vez
five_wh_one_plus: how_not
tags:
- system:sldb
---

# Un flag que casi todos los subcomandos aceptan se define una sola vez

## Answer

No repetir --format por subparser: así fue como models show, models template show y docs update quedaron sin él y lo rechazaban. Se define en un solo lugar (sldb/cli/output_format.py: add_format y emit). Y argparse, con parse_args en la raíz, reporta los argumentos sobrantes con el uso de la raíz: parse_known_args más el error del subparser más profundo (cli/subcommand_errors.py) dice qué comando lo rechazó.
