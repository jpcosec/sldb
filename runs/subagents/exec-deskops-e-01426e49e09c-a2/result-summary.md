# Resultado intento 2
- heading_scan.py: nuevo scan_heading_bodies (cuerpos desde el AST con rangos de linea; ATX, setext, indentados).
- lossy_overwrite.py: usa scan_heading_bodies; sin cuerpo encontrado => se rechaza (falla cerrado); se quitaron las definiciones duplicadas.
- tests/api/test_lossy_overwrite_content.py: +4 (setext e indentado, rechazo y aceptacion).
- CHANGELOG.md actualizado.
- Validacion: ver validation.log. Commit en la rama deskops/deskops-e-01426e49e09c-a2 con Task-Id.
- Nota: un encabezado con sangria justo tras un item de lista queda dentro del item (no es top-level, no es 'no declarado'); el test lo separa con '---'.
- Revisar: check.sh --fast rc 1 solo por identidad/workbench_demo.
