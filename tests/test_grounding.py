import copy
from decimal import localcontext
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from exorien.grounding import InvalidEncounter, compare

ROOT = Path(__file__).resolve().parents[1]


class GroundingTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((ROOT / 'examples/temperature.json').read_text())

    def test_conversion_and_evidence(self):
        result = compare(self.data)
        self.assertEqual(result['status'], 'comparable')
        self.assertEqual(result['delta'], '0.00')
        self.assertEqual(result['unit'], 'K')
        self.assertEqual(result['evidence'], ['synthetic:reading-1', 'synthetic:reading-2'])
        self.assertIs(result['action_authorized'], False)

    def test_mismatched_context_is_unknown(self):
        for field in ('vocabulary', 'quantity', 'referent', 'frame', 'window'):
            with self.subTest(field=field):
                data = copy.deepcopy(self.data)
                data['observations'][1][field] = 'other'
                self.assertEqual(compare(data)['status'], 'unknown')

    def test_unknown_conversion(self):
        self.data['observations'][1]['unit'] = 'F'
        self.assertEqual(compare(self.data)['status'], 'unknown')

    def test_disagreement_and_boundary(self):
        self.data['observations'][1]['value'] = '293.16'
        self.assertEqual(compare(self.data)['status'], 'comparable')
        self.data['observations'][1]['value'] = '293.17'
        self.assertEqual(compare(self.data)['status'], 'different')

    def test_opaque_same_units(self):
        for obs in self.data['observations']:
            obs.update(quantity='count', unit='items', value='3')
        self.assertEqual(compare(self.data)['status'], 'comparable')

    def test_invalid_values(self):
        for value in (True, None, 20, 'NaN', 'Infinity', '-Infinity', 'no', '1e30', '1e-20', '1e1000000'):
            with self.subTest(value=value):
                data = copy.deepcopy(self.data)
                data['observations'][0]['value'] = value
                with self.assertRaises(InvalidEncounter):
                    compare(data)

    def test_negative_absolute_temperature(self):
        self.data['observations'][0]['value'] = '-274'
        with self.assertRaises(InvalidEncounter):
            compare(self.data)

    def test_invalid_structure(self):
        for data in (None, [], {}, {'version': '0.1', 'observations': [1, 2]}):
            with self.subTest(data=data), self.assertRaises(InvalidEncounter):
                compare(data)

    def test_invalid_required_fields(self):
        for field in ('observer', 'evidence', 'vocabulary', 'quantity', 'referent', 'frame', 'window', 'unit'):
            data = copy.deepcopy(self.data)
            del data['observations'][0][field]
            with self.subTest(field=field), self.assertRaises(InvalidEncounter):
                compare(data)

    def test_negative_tolerance(self):
        self.data['tolerance'] = '-0.1'
        with self.assertRaises(InvalidEncounter):
            compare(self.data)

    def test_observers_must_differ(self):
        self.data['observations'][1]['observer'] = self.data['observations'][0]['observer']
        with self.assertRaises(InvalidEncounter):
            compare(self.data)

    def test_caller_decimal_context_does_not_change_results(self):
        expected = compare(self.data)
        with localcontext() as context:
            context.prec = 2
            self.assertEqual(compare(self.data), expected)

    def test_input_unchanged(self):
        original = copy.deepcopy(self.data)
        compare(self.data)
        self.assertEqual(original, self.data)

    def test_cli(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'encounter.json'
            for expected, mutate in ((0, lambda d: None), (1, lambda d: d['observations'][1].update(frame='other'))):
                data = copy.deepcopy(self.data)
                mutate(data)
                path.write_text(json.dumps(data))
                run = subprocess.run([sys.executable, '-m', 'exorien', str(path)], cwd=ROOT, capture_output=True, text=True)
                self.assertEqual(run.returncode, expected, run.stderr)
                self.assertIs(json.loads(run.stdout)['action_authorized'], False)
            data = copy.deepcopy(self.data)
            data['observations'][0]['value'] = '1e1000000'
            path.write_text(json.dumps(data))
            run = subprocess.run([sys.executable, '-m', 'exorien', str(path)], cwd=ROOT, capture_output=True, text=True)
            self.assertEqual(run.returncode, 2)
            self.assertNotIn('Traceback', run.stderr)
            path.write_text('{')
            run = subprocess.run([sys.executable, '-m', 'exorien', str(path)], cwd=ROOT, capture_output=True, text=True)
            self.assertEqual(run.returncode, 2)
            self.assertEqual(run.stdout, '')
            self.assertNotIn('Traceback', run.stderr)


if __name__ == '__main__':
    unittest.main()
