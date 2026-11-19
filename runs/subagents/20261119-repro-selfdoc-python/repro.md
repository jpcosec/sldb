# Reproducción (integrador, 2026-11-19)

- host.txt: con /usr/bin/python3.12 (3.12.3) del host, el argumento files de 'sldb stores merge-driver' sale con su nargs y required tal como los ve argparse en el host.
- diff-contenedor.txt: el ejecutor deskops-e-e2793c478ec4 regeneró la referencia en el contenedor scion (python 3.12 de uv) con 'sldb selfdoc sync' y el campo required cambió (commit 1c6d26ee).
- En el host, 'sldb selfdoc check' marcó selfdoc/changed para knowledge/commands/cmd-sldb-stores-merge-driver.md hasta que el coordinador restauró la versión del host (98ae6cc6). Lo mismo pasó el 18-11 en la tarea de --check --keep.
