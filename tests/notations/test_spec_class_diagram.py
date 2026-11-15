from copy import deepcopy
from pathlib import Path

import pytest
import yaml

from sldb.models.notation.diagram_specs.class_diagram import ClassDiagram
from sldb.models.notation.diagram_specs.loader import load
from sldb.models.notation.diagram_specs.validator import validate
from sldb.notations.exceptions import ParseError, ValidationError

EXAMPLE = Path(__file__).parent.parent / "fixtures" / "specs" / "examples" / "class" / "runtime.yml"


def raw():
    return yaml.safe_load(EXAMPLE.read_text())


@pytest.mark.parametrize('mutate,match', [
    (lambda d: d['data']['relations'][0].update(to='Missing'), 'unknown class'),
    (lambda d: d['data']['relations'][0].update(to='NodeSpec'), 'interface or protocol'),
    (lambda d: d['data']['relations'][0].update(to='DataNode'), 'itself'),
    (lambda d: d['data']['relations'][0].update(to_multiplicity='1'), 'multiplicities'),
    (lambda d: d['data']['relations'][1].update(to_multiplicity='3..1'), 'Inverted'),
    (lambda d: d['data']['classes']['DataNode']['attributes'].append({'name':'spec','type':'Other'}), 'Duplicate attribute'),
    (lambda d: d['data']['classes']['DataNode']['methods'].append(deepcopy(d['data']['classes']['DataNode']['methods'][0])), 'Duplicate method'),
    (lambda d: d['data']['classes']['DataNode']['methods'][0]['parameters'].append({'name':'input','type':'Other'}), 'Duplicate parameter'),
    (lambda d: d['data']['classes']['ExecutableNode']['methods'][0].update(static=True), 'static and abstract'),
])
def test_semantic_errors_are_rejected(mutate, match):
    data = raw()
    mutate(data)
    with pytest.raises(ValidationError, match=match):
        validate(ClassDiagram.model_validate(data))


def test_inheritance_cycle_is_rejected_but_dependency_cycles_are_allowed():
    data = raw()
    data['data']['relations'] = [
        {'from':'DataNode', 'to':'NodeSpec', 'relation':'inheritance'},
        {'from':'NodeSpec', 'to':'DataNode', 'relation':'inheritance'},
    ]
    with pytest.raises(ValidationError, match='cycle'):
        validate(ClassDiagram.model_validate(data))
    for relation in data['data']['relations']:
        relation['relation'] = 'dependency'
    validate(ClassDiagram.model_validate(data))


def test_overloads_with_distinct_parameter_types_are_allowed():
    data = raw()
    overload = deepcopy(data['data']['classes']['DataNode']['methods'][0])
    overload['parameters'][1]['type'] = 'OtherInput'
    data['data']['classes']['DataNode']['methods'].append(overload)
    validate(ClassDiagram.model_validate(data))


@pytest.mark.parametrize('mutate', [
    lambda d: d['data']['classes'].update({'bad-id': {}}),
    lambda d: d['data']['classes']['DataNode']['methods'][0].update(returnz='Typo'),
    lambda d: d['data']['classes']['DataNode']['methods'][0].update(name='run\n}'),
    lambda d: d['data']['classes']['DataNode']['attributes'][0].update(type='Type\nOther'),
    lambda d: d['data']['relations'][0].update(relation='implements'),
    lambda d: d['data']['relations'][1].update(to_multiplicity='many'),
])
def test_invalid_schema_fails_at_load(tmp_path, mutate):
    data = raw()
    mutate(data)
    path = tmp_path / 'invalid.yml'
    path.write_text(yaml.safe_dump(data))
    with pytest.raises(ParseError, match='Invalid diagram schema'):
        load(path)
