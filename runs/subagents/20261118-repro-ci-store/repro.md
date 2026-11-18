# Reproducción: el job store del CI de sldb construye el store dos veces

## CI (GitHub)
Run 44169114744 sobre 6d87f126, job store 134343092734 (ver ci-job-134343092734.json):
- Build deskops' store, Prepare pron's store y Rebuild sldb's store from its sources (`sldb stores build --check`): success.
- Check generated CLI reference (`sldb stores build && sldb selfdoc check`): cancelled; el job excedió el máximo de 6h0m0s.

## Local, con el layout del runner (2026-11-18, robocop2)
Clones de GitHub en /dev/shm/ci-store: sldb 40d399e (6d87f126 + solo commits de desk), deskops a6bb2591 y pron a0c4100. Sin scion y sin knowledge/symbols. Venv /mnt/ssd/proyectos/SLDB_1/.venv. Ver local-repro-store-job.log:
- deskops `sldb stores build`: rc 0
- pron `make world`: rc 0
- sldb `sldb stores build --check`: rc 0 en 110 min, con un proceso al 100 % de CPU todo el tiempo y solo alertas.
- Con knowledge/symbols presente, el mismo build tarda unos 55 min (corridas anteriores del integrador).

## Causa (hipótesis fuerte)
`sldb stores build --help`: "--check  Rebuild a scratch copy of the sources and compare, writing nothing here". El paso siguiente del workflow vuelve a correr un `sldb stores build` completo, así que el job hace dos builds de ~110 min o más en el runner, que es más lento, y no entra en 6 h.
