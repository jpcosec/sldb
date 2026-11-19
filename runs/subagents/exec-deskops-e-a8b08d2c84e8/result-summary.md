# Result
run_id: exec-deskops-e-a8b08d2c84e8
Files: src/sldb/api/documents/lossy_overwrite.py, src/sldb/api/documents/payload_save.py, tests/api/test_structural_noise.py, CHANGELOG.md
refuse_lossy_overwrite now takes the rendered text; refuses only undeclared headings/frontmatter keys of the current file absent from it. save runs the guard after render. Two new tests. Validation: see validation.log (both rc 0).
Not verified: deskops tests/test_promotion_nesting.py (integrator).
