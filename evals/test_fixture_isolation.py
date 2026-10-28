"""Keep content-eval facts out of runtime skills; report exact leaking files."""
import json
import re
import tempfile
import unicodedata
import unittest
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEXT_SUFFIXES = {'.md', '.json', '.yaml', '.yml', '.txt', '.py', '.toml'}
NUMBER = re.compile(r'(?<![A-Za-z0-9_.])\d+(?:\.\d+)?(?![A-Za-z0-9_.])')


def numeric_tokens(text):
    """Numeric literals, not substrings of hashes, identifiers or build numbers."""
    return {Decimal(m.group()) for m in NUMBER.finditer(unicodedata.normalize('NFKC', text))}


def protected_numbers(text):
    # Small integers and integer percentages often overlap legitimately.
    # Scenario phrases below protect their field context without banning '4'.
    return {n for n in numeric_tokens(text) if n >= 100 or n != n.to_integral_value()}


def compact(text):
    return re.sub(r'\s+', '', unicodedata.normalize('NFKC', text))


def find_leaks(source, phrases, skill_root):
    numbers = protected_numbers(source)
    leaks = []
    for path in sorted(skill_root.rglob('*')):
        if not path.is_file() or path.suffix not in TEXT_SUFFIXES:
            continue
        text = path.read_text(encoding='utf-8')
        shared = sorted(numbers & numeric_tokens(text))
        copied = [phrase for phrase in phrases if compact(phrase) in compact(text)]
        if shared or copied:
            leaks.append({'file': path.relative_to(skill_root).as_posix(),
                          'numbers': [str(n) for n in shared], 'phrases': copied})
    return leaks


class FixtureIsolationTests(unittest.TestCase):
    def test_all_inputs_have_declared_evaluation_role(self):
        cases = json.loads((ROOT/'evals/cases.json').read_text(encoding='utf-8'))
        declared = {'inputs/routing.json'}
        for case in cases['content']:
            self.assertNotIn(case['request'], declared)
            declared.add(case['request'])
            self.assertIn(case.get('evaluation_role'),
                          {'known_source_regression', 'isolated_content_regression'})
            if case['evaluation_role'] == 'known_source_regression':
                self.assertTrue(case.get('overlap_reason', '').strip())
            else:
                source = (ROOT/'evals'/case['request']).read_text(encoding='utf-8')
                self.assertTrue(protected_numbers(source))
                self.assertTrue(case.get('protected_phrases'))
                for phrase in case['protected_phrases']:
                    self.assertIn(compact(phrase), compact(source))
        self.assertEqual(declared, {p.relative_to(ROOT/'evals').as_posix()
                                    for p in (ROOT/'evals/inputs').rglob('*') if p.is_file()})

    def test_eval_numbers_and_phrases_absent_from_skills(self):
        cases = json.loads((ROOT/'evals/cases.json').read_text(encoding='utf-8'))
        for case in cases['content']:
            if case['evaluation_role'] != 'isolated_content_regression':
                continue
            source = (ROOT/'evals'/case['request']).read_text(encoding='utf-8')
            with self.subTest(case=case['id']):
                self.assertEqual(find_leaks(source, case['protected_phrases'], ROOT/'skills'), [])

    def test_guard_rejects_reintroduced_examples_in_both_locations(self):
        source = (ROOT/'evals/inputs/inspection-abstract.md').read_text(encoding='utf-8')
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root/'references').mkdir()
            (root/'SKILL.md').write_text('在240件产品的独立测试集上。', encoding='utf-8')
            (root/'references/writing.md').write_text('在漏检率4%的上限下，新批次下全部候选不可行。', encoding='utf-8')
            leaks = find_leaks(source, ['漏检率', '新批次'], root)
            self.assertEqual(len(leaks), 2)
            by_file = {item['file']: item for item in leaks}
            self.assertEqual(by_file['SKILL.md']['numbers'], ['240'])
            self.assertEqual(by_file['references/writing.md']['phrases'], ['漏检率', '新批次'])

    def test_numeric_matching_avoids_incidental_substrings(self):
        text = '在240件中；2400件不同；p240不是数值；SHA a240b；Word16.0.20527.20088；3种方案；4%上限。'
        self.assertEqual(protected_numbers(text), {Decimal('240'), Decimal('2400')})
        self.assertFalse(protected_numbers('三种方案；4%上限；Word 16.0.20527.20088'))

    def test_fullwidth_and_percent_literals_are_normalized(self):
        self.assertEqual(protected_numbers('２４０ 件；８７．５％；82.5\\%'),
                         {Decimal('240'), Decimal('87.5'), Decimal('82.5')})


if __name__ == '__main__':
    unittest.main()
