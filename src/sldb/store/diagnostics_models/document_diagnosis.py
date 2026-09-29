from __future__ import annotations
from dataclasses import dataclass, field
from sldb.store.diagnostics_models.diagnosis_note import DiagnosisNote
from sldb.store.diagnostics_models.document_verdicts import EXPLANATIONS, NEEDS_DECISION, REMEDIES



@dataclass
class DocumentDiagnosis:
    """Diagnostic state for a single document.

    The hashes are named for what they sign, not for their position in the chain
    (`docs/versionado-y-colaboracion.md`):

    - ``content`` — `hash_c`, SHA-256 of the markdown TEXT. Moves on any rewrite of
      the file, including one that changes nothing a model can read.
    - ``fields`` — `hash_d`, SHA-256 of the EXTRACTED PAYLOAD under the model's
      contract. Moves only when a field's value actually changes.

    That split is the whole basis of the verdict: text moving while fields hold
    still is an expected mutation (reformatting, a trailing newline); fields moving
    is a real change to the data.

    The two sides of a comparison are named for WHERE they were read, not for which
    is "right" — neither is authoritative alone. ``*_on_disk`` is recomputed from the
    file now; ``*_in_index`` is what the store recorded at the last write. Which one
    is stale is exactly what the caller is trying to find out.

    The letter aliases (`hash_c_ok`, …) remain because the store's PERSISTED keys are
    still `hash_c`/`hash_d`: renaming those would invalidate every store on disk.
    """

    name: str
    path: str
    content_ok: bool
    fields_ok: bool
    path_exists: bool
    note: DiagnosisNote
    content_on_disk: str | None = None
    content_in_index: str | None = None
    fields_on_disk: str | None = None
    fields_in_index: str | None = None
    # Which fields moved, when both sides carry a per-field map. Empty means the question could
    # not be asked (a store written before `field_hashes`, or a document that no longer
    # extracts) — never that no field moved, which `fields_ok` already answers.
    changed_fields: list[str] = field(default_factory=list)

    @property
    def hash_c_ok(self) -> bool:
        """Deprecated alias for `content_ok`."""
        return self.content_ok

    @property
    def hash_d_ok(self) -> bool:
        """Deprecated alias for `fields_ok`."""
        return self.fields_ok

    @property
    def hash_c_expected(self) -> str | None:
        """Deprecated alias for `content_on_disk`."""
        return self.content_on_disk

    @property
    def hash_c_actual(self) -> str | None:
        """Deprecated alias for `content_in_index`."""
        return self.content_in_index

    @property
    def hash_d_expected(self) -> str | None:
        """Deprecated alias for `fields_on_disk`."""
        return self.fields_on_disk

    @property
    def hash_d_actual(self) -> str | None:
        """Deprecated alias for `fields_in_index`."""
        return self.fields_in_index

    def explain(self) -> str:
        """One line saying what is wrong and what to do about it."""
        if self.note is DiagnosisNote.MISSING:
            return f"missing: tracked at {self.path}, not on disk"
        base = EXPLANATIONS[self.note]
        return f"{base} [fields: {', '.join(self.changed_fields)}]" if self.changed_fields else base

    @property
    def needs_decision(self) -> bool:
        """Whether a human must look before anything is run.

        A field value that changed, or a document that vanished, is not something a command
        should paper over: the index is the only record of what the value used to be.
        """
        return self.note in NEEDS_DECISION

    def inspect(self) -> str:
        """What to open to judge this finding — the document, or the model that reinterpreted it."""
        return "the model's contract, not this file" if self.note is DiagnosisNote.CONTRACT_MUTATION else self.path

    def remedy(self) -> str:
        """The command that resolves this finding, or what to decide when none does."""
        return REMEDIES[self.note]
