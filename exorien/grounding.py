"""Compare declared observations; never infer shared meaning or permission."""
from decimal import Context, Decimal, InvalidOperation, localcontext


class InvalidEncounter(ValueError):
    """The input is outside this experiment's narrow contract."""


def _text(record, field):
    value = record.get(field)
    if not isinstance(value, str) or not value.strip():
        raise InvalidEncounter(f'{field} must be a nonempty string')
    return value


def _number(value, field):
    # Decimal strings preserve declared precision; JSON booleans are not numbers.
    if not isinstance(value, str):
        raise InvalidEncounter(f'{field} must be a decimal string')
    try:
        result = Decimal(value)
    except InvalidOperation as exc:
        raise InvalidEncounter(f'{field} must be a finite decimal') from exc
    if not result.is_finite() or result.copy_abs() > Decimal('1e12'):
        raise InvalidEncounter(f'{field} must be finite and within +/-1e12')
    if len(result.as_tuple().digits) > 20 or result.as_tuple().exponent < -12:
        raise InvalidEncounter(f'{field} exceeds experiment precision limits')
    return result


def compare(encounter):
    """Compare using a fixed decimal context, independent of the caller."""
    with localcontext(Context(prec=50)):
        return _compare(encounter)


def _compare(encounter):
    """Return comparable/different/unknown plus a trace, with no side effects.

    A shared vocabulary, referent, frame and sampling window are declarations,
    not independently verified facts. Only exact units and C/K are supported.
    """
    if not isinstance(encounter, dict) or encounter.get('version') != '0.1':
        raise InvalidEncounter('expected encounter version 0.1')
    observations = encounter.get('observations')
    if not isinstance(observations, list) or len(observations) != 2:
        raise InvalidEncounter('exactly two observations are required')
    parsed = []
    for observation in observations:
        if not isinstance(observation, dict):
            raise InvalidEncounter('observation must be an object')
        fields = {key: _text(observation, key) for key in (
            'observer', 'evidence', 'vocabulary', 'quantity', 'referent',
            'frame', 'window', 'unit')}
        fields['value'] = _number(observation.get('value'), 'value')
        parsed.append(fields)
    a, b = parsed
    tolerance = _number(encounter.get('tolerance'), 'tolerance')
    if tolerance < 0:
        raise InvalidEncounter('tolerance cannot be negative')
    if a['observer'] == b['observer']:
        raise InvalidEncounter('two distinct observer identifiers are required')
    result = {
        'version': '0.1', 'status': 'unknown', 'action_authorized': False,
        'evidence': [a['evidence'], b['evidence']],
        'assumption': 'Shared identifiers and observations are caller declarations, not verified truth.',
        'trace': [],
    }
    for field in ('vocabulary', 'quantity', 'referent', 'frame', 'window'):
        if a[field] != b[field]:
            result['trace'].append(f'{field} mismatch: explicit grounding required')
    if result['trace']:
        return result
    if a['quantity'] == 'temperature' and {a['unit'], b['unit']} <= {'C', 'K'}:
        values = [o['value'] + (Decimal('273.15') if o['unit'] == 'C' else 0)
                  for o in parsed]
        if any(value < 0 for value in values):
            raise InvalidEncounter('temperature below absolute zero')
        unit = 'K'
        result['trace'].append('Declared temperature observations normalized from C/K to K.')
    elif a['unit'] == b['unit']:
        values = [a['value'], b['value']]
        unit = a['unit']
        result['trace'].append('Same declared unit; no conversion applied.')
    else:
        result['trace'].append('unit mismatch: no supported explicit conversion')
        return result
    delta = abs(values[0] - values[1])
    result.update(status='comparable' if delta <= tolerance else 'different',
                  unit=unit, delta=str(delta), tolerance=str(tolerance))
    result['trace'].append('Compared numeric difference against the caller-declared tolerance; this is not proof of shared experience.')
    return result
