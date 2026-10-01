import difflib
import re
from sldb.api.records.search_record import SearchRecord

def search_records(records: list[SearchRecord], term: str, search_in: str, regex: bool = False, fuzzy: bool = False, kinds: set[str] | None = None) -> list[SearchRecord]:
    if term in {"stores", "models", "docs", "sections", "fields"}:
        kind = term[:-1] if term.endswith("s") else term
        return [record for record in records if record.kind == kind]
    if kinds: records = [record for record in records if record.kind in kinds]
    if not term: return records
    return _filter_records(records, term, search_in, regex, fuzzy)

def _filter_records(records, term, search_in, regex, fuzzy):
    matched = []
    for record in records:
        haystacks: list[str] = []
        if search_in in {"physical", "both"}: haystacks.extend(record.physical)
        if search_in in {"semantic", "both"}:
            haystacks.extend(record.semantic)
            haystacks.extend(record.about or [])
        _check_match(record, haystacks, term, regex, fuzzy, matched)
    return matched

def _check_match(record, haystacks, term, regex, fuzzy, matched):
    haystacks = [v for v in haystacks if v]
    if _matches_term(haystacks, term, regex=regex, fuzzy=fuzzy):
        matched.append(record)

def _matches_term(haystacks: list[str], term: str, regex: bool, fuzzy: bool) -> bool:
    if regex:
        return any(re.search(term, value) is not None for value in haystacks)
    if fuzzy:
        target = term.lower()
        return any(difflib.SequenceMatcher(a=target, b=v.lower()).ratio() >= 0.7 or target in v.lower() for v in haystacks)
    return any(term == value or term in value for value in haystacks)
