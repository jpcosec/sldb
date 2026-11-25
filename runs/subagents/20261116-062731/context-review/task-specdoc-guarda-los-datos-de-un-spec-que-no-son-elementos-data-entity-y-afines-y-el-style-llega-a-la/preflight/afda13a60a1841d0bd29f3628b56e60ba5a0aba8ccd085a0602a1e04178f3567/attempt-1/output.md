REFORMULACION
Propósito: que el SpecDoc conserve los datos de un spec que no son elementos (en particular `data.entity`) y que el `style` llegue a la vista resuelta, para que IR11 no pierda información al pasar por el store. Resultado: campo opcional `data: dict[str, Any]` con `default_factory=dict`, marcador YAML copiado de `style`, escritura en `spec_sync_docs.py`, round trip probado, `style` comprobado en `resolve_view`, CHANGELOG y commit del coordinador. Repo: `SLDB_1` (`/mnt/ssd/proyectos/SLDB_1`). Límites: no reexportar clases, no cambiar el YAML de specs, no migrar `docs.models:SpecDoc`, no push; el commit lo hace el coordinador. El nodo es ejecutable, no agregado ni paquete.

AMBIGUEDADES
1. “Un aviso con deskops message send --to <repo>” y “Aviso a <repo>: ...”: no se concreta el identificador de `<repo>`; obligaría a inventar el destinatario o deducirlo de convenciones no incluidas.
2. “mensaje '<título corto de la tarea>'”: no se define qué es “título corto”; obligaría a inventar el criterio de abreviación, aunque corresponda al coordinador.
3. “bajo el encabezado '## 0.1.13 — not released yet'”: no se dice si el ejecutor debe crear ese encabezado si no existe; obligaría a decidir si se añade versión o solo una línea.

DRY-RUN
Lecturas: nota de origen, `src/sldb/models/notation/spec_doc.py`, `src/sldb/api/notations/spec_sync_docs.py`, resolvedor en `sldb.api.notations`, tests nombrados, `CHANGELOG.md` y helpers de test. Cambios previstos: añadir `data` con `Field(default_factory=dict)` y su marcador de plantilla; mapear en sincronización las claves de `data` no tratadas como elementos; pasar `style` a la vista resuelta si falta; test de round trip de `data.entity` y de `style` en vista; línea de CHANGELOG. Dependencias: nota de origen, fixtures/helpers existentes, store `.sldb`, coordinador para commit. Validaciones futuras: `pytest` sobre `test_spec_sync.py` y `test_spec_catalog_sync.py`, `sldb stores build --check --store .sldb`, round trip y clave `style`. Nada se ejecuta aquí.

FUTURO
El coordinador hará el commit y, si corresponde, el aviso; un humano decidirá la publicación/merge y resolverá el destinatario o el título si no hay convención. Otro nodo cubrirá exports y la migración del SpecDoc local.
