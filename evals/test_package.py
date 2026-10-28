import json
import re
import unittest
import tempfile
import hashlib
import ast
from decimal import Decimal as D
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_outputs import check_routes, check_restatement, check_abstract, split_paper_notes
from validators import valid_repository, native_errors, stale_records, text_hash


class PackageTests(unittest.TestCase):
    def test_five_skill_names(self):
        self.assertEqual({p.name for p in (ROOT/'skills').iterdir()}, {
            'cumcm-abstract', 'cumcm-problem-restatement', 'cumcm-problem-analysis',
            'cumcm-model-assumptions', 'mathtype-texvc'})

    def test_manifests(self):
        for host in ['.claude-plugin', '.codex-plugin']:
            obj = json.loads((ROOT/host/'plugin.json').read_text(encoding='utf-8'))
            self.assertEqual(obj['name'], 'cumcm-writing-skills')
            self.assertEqual(obj['author']['name'], 'W')
            self.assertEqual(obj['license'], 'MIT')
            self.assertRegex(obj['version'], r'^\d+\.\d+\.\d+$')
            self.assertTrue(valid_repository(obj.get('repository')))

    def test_utf8_metadata(self):
        for p in ROOT.glob('.*-plugin/plugin.json'):
            self.assertNotIn('\\u', p.read_text(encoding='utf-8'))

    def test_entrypoint_identity_and_size(self):
        for p in (ROOT/'skills').glob('*/SKILL.md'):
            text = p.read_text(encoding='utf-8')
            self.assertIn('name: '+p.parent.name, text)
            self.assertIn('license: MIT', text)
        self.assertLessEqual((ROOT/'skills/cumcm-abstract/SKILL.md').stat().st_size, 9000)

    def test_all_local_links(self):
        for p in ROOT.rglob('*.md'):
            for target in re.findall(r'\[[^\]]+\]\(([^\s)]+)\)', p.read_text(encoding='utf-8')):
                if target.startswith(('https:', 'http:', '#')):
                    continue
                resolved = (p.parent/target.split('#')[0]).resolve()
                self.assertTrue(resolved.is_relative_to(ROOT.resolve()), (p, target))
                self.assertTrue(resolved.exists(), (p, target))

    def test_each_skill_is_self_contained(self):
        for skill in (ROOT/'skills').iterdir():
            for p in skill.rglob('*.md'):
                for target in re.findall(r'\[[^\]]+\]\(([^\s)]+)\)',p.read_text(encoding='utf-8')):
                    if target.startswith(('https:','http:','#')):
                        continue
                    resolved=(p.parent/target.split('#')[0]).resolve()
                    self.assertTrue(resolved.is_relative_to(skill.resolve()),(p,target))
                    self.assertTrue(resolved.exists(),(p,target))

    def test_no_stale_runtime_identity(self):
        for p in (ROOT/'skills').rglob('*'):
            if p.suffix not in ('.md', '.yaml'):
                continue
            text = p.read_text(encoding='utf-8')
            for stale in ['本次会话', '用户此前', '用户补充的截图', '用户已选择进阶',
                          '后续用户要求已覆盖', '随包可复核范围（', '/mnt/skills/public',
                          '$math-abstract', 'result_registry.csv', 'claim_ledger.csv']:
                self.assertNotIn(stale, text, p)

    def test_personal_structure_is_default(self):
        text = (ROOT/'skills/cumcm-problem-restatement/SKILL.md').read_text(encoding='utf-8')
        self.assertIn('模板另有要求', text)
        self.assertNotIn('不得另立', text)
        example = (ROOT/'skills/cumcm-problem-restatement/references/example-credit.md').read_text(encoding='utf-8')
        self.assertIn('#### 1.2 问题提出', example)
        self.assertNotIn('#### 1.2 问题要求', example)

    def test_mathtype_has_single_rule_owner(self):
        for p in (ROOT/'skills').glob('cumcm-*/SKILL.md'):
            text = p.read_text(encoding='utf-8')
            self.assertEqual(text.count('`mathtype-texvc`'), 1)
            self.assertNotIn('\\tag', text)
            self.assertNotIn('源码段落左对齐', text)

    def test_native_status_not_fabricated(self):
        skill=ROOT/'skills/mathtype-texvc'
        data=json.loads((skill/'references/native-tests.json').read_text(encoding='utf-8'))
        self.assertEqual(native_errors(data,skill),[])

    def test_license_attribution(self):
        self.assertIn('Copyright (c) 2026 W', (ROOT/'LICENSE').read_text(encoding='utf-8'))
        self.assertIn('数模skill contributors', (ROOT/'licenses/cumcm-paper-hand-skill-MIT.txt').read_text(encoding='utf-8'))
        self.assertIn('handsomeZR-netizen', (ROOT/'licenses/mathmodel-skill-MIT.txt').read_text(encoding='utf-8'))

    def test_official_data_bounds(self):
        source = json.loads((ROOT/'examples/official-2020-c/source.json').read_text(encoding='utf-8'))
        stats = source['enterprise_metadata_check']
        self.assertEqual(sum(stats['ratings'].values()), stats['records'])
        self.assertEqual(sum(stats['default_labels'].values()), stats['records'])
        self.assertEqual(stats['records'], 123)
        self.assertFalse(source['redistributed_original_files'])

    def test_water_model(self):
        levels = []
        s = D(5)
        for a,b in zip([10,8,12], [9,11,10]):
            s += D(a)-D(b); levels.append(s)
        self.assertEqual(levels, list(map(D,[6,3,5])))
        peak = max([D(5)]+levels)
        choices = [(5,1000),(6,1200),(8,1600)]
        self.assertEqual(min((x for x in choices if x[0]>=peak),key=lambda x:x[1]), (6,1200))
        s=D(5); shock=[]
        for a,b in zip([10,8,12],[9,11,10]):
            s += D(a)*D('1.2')-D(b); shock.append(s)
        self.assertEqual(shock, list(map(D,['8','6.6','11'])))

    def test_route_checker_rejects_false_positive(self):
        cases=json.loads((ROOT/'evals/cases.json').read_text(encoding='utf-8'))['routes']
        correct={c['id']:{'skills':c['expected'],'action':c['expected_action']} for c in cases}
        self.assertTrue(all(check_routes(correct,cases).values()))
        incorrect=dict(correct); incorrect['R01']={'skills':['cumcm-problem-restatement'],'action':'use'}
        incorrect['R06']={'skills':['cumcm-abstract'],'action':'use'}
        result=check_routes(incorrect,cases)
        self.assertFalse(result['R01']); self.assertFalse(result['R06'])
        del correct['R06']
        self.assertFalse(check_routes(correct,cases)['R06'])

    def test_content_checker_negative_controls(self):
        bad='## 问题背景\n123家302家。\n## 问题提出\n问题一总额为1亿元。问题二给风险。问题三调整。'
        self.assertFalse(check_restatement(bad)['three_requested_sections'])
        self.assertFalse(check_restatement(bad)['first_budget_not_imported'])
        self.assertFalse(check_abstract('采用遗传算法，全局最优容量6 m³，1200元。')['no_unrelated_algorithm'])
        self.assertFalse(check_abstract('容量6 m³，1200元。')['classification_results'])

    def test_repository_field_is_future_compatible(self):
        self.assertTrue(valid_repository(None))
        self.assertTrue(valid_repository('https://github.com/example/project'))
        self.assertFalse(valid_repository('file:///private/project'))
        self.assertFalse(valid_repository('https://user:secret@example.com/repo'))

    def test_future_native_pass_requires_versions(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder)
            (root/'evidence.png').write_bytes(b'test fixture')
            good={'id':'MT04','status':'pass','word_version':'16.0.12345','mathtype_version':'7.4',
                  'os':'Windows 11','entrypoint':'Toggle TeX','tested_at':'2026-10-27','artifact':'evidence.png'}
            self.assertEqual(native_errors({'tests':[good]},root),[])
            bad=dict(good);bad['word_version']='填写实际版本'
            self.assertTrue(native_errors({'tests':[bad]},root))
            self.assertEqual(native_errors({'tests':[{'id':'MT05','status':'not_run'}]},root),[])
            self.assertTrue(native_errors({'tests':[{'id':'MT06','status':'pass','word_version':None}]},root))
            self.assertTrue(native_errors({'tests':{}},root))

    def test_author_usage_needs_versions_not_screenshot(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder)
            usage={'status':'author_usage','word_version':'Word 2016（16.0.20527.20088）','mathtype_version':'7.8.2.441'}
            self.assertEqual(native_errors({'tests':[usage]},root),[])
            missing=dict(usage);del missing['mathtype_version']
            self.assertTrue(native_errors({'tests':[missing]},root))
            promoted=dict(usage,status='pass')
            self.assertTrue(native_errors({'tests':[promoted]},root))

    def test_duplicate_source_manifests_match(self):
        canonical=ROOT/'examples/official-2020-c/source.json'
        copies=list((ROOT/'skills').glob('*/references/official-2020-c-source.json'))
        self.assertEqual(len(copies),4)
        expected=hashlib.sha256(canonical.read_bytes()).digest()
        for copy in copies:
            self.assertEqual(hashlib.sha256(copy.read_bytes()).digest(),expected,str(copy.relative_to(ROOT)))

    def test_duplicate_upstream_licenses_match(self):
        for name in ['cumcm-paper-hand-skill-MIT.txt','mathmodel-skill-MIT.txt']:
            copies=list((ROOT/'skills').glob('*/licenses/'+name))
            self.assertEqual(len(copies),2)
            expected=hashlib.sha256((ROOT/'licenses'/name).read_bytes()).digest()
            for copy in copies:
                self.assertEqual(hashlib.sha256(copy.read_bytes()).digest(),expected,str(copy.relative_to(ROOT)))

    def test_credit_example_body_retains_d_policy(self):
        text=(ROOT/'skills/cumcm-problem-restatement/references/example-credit.md').read_text(encoding='utf-8')
        body=text.split('#### 1.2 问题提出',1)[1].split('## 为什么这样写',1)[0]
        self.assertRegex(body,r'D\s*级企业原则上不放贷')

    def test_public_python_text_reads_use_utf8(self):
        for path in (ROOT/'evals').glob('*.py'):
            tree=ast.parse(path.read_text(encoding='utf-8'))
            for node in ast.walk(tree):
                if isinstance(node,ast.Call) and isinstance(node.func,ast.Attribute) and node.func.attr=='read_text':
                    explicit=[k.value for k in node.keywords if k.arg=='encoding']
                    positional=node.args[:1]
                    values=explicit or positional
                    self.assertTrue(values,'Missing read_text encoding: '+path.name)
                    self.assertTrue(isinstance(values[0],ast.Constant) and values[0].value=='utf-8',path.name)

    def test_freshness_detects_changes_without_publication_rule(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder);p=root/'SKILL.md';p.write_text('v1',encoding='utf-8')
            manifest={'skill_and_input_sha256':{'SKILL.md':text_hash(p)}}
            self.assertEqual(stale_records(root,manifest),[])
            p.write_text('v2',encoding='utf-8')
            self.assertEqual(stale_records(root,manifest),['SKILL.md'])

    def test_public_files_have_no_personal_paths(self):
        for p in ROOT.rglob('*'):
            if p.suffix not in {'.md','.json','.yaml','.yml','.txt'}:
                continue
            text=p.read_text(encoding='utf-8')
            self.assertNotRegex(text,r'/mnt/[a-z]/[Uu]sers/|[A-Za-z]:[\\/]+Users[\\/]+|/\.codex/skills/')

    def test_marketplace_points_to_plugin(self):
        obj=json.loads((ROOT/'.claude-plugin/marketplace.json').read_text(encoding='utf-8'))
        self.assertEqual(obj['owner']['name'],'W')
        self.assertEqual(obj['plugins'][0]['name'],'cumcm-writing-skills')
        self.assertEqual(obj['plugins'][0]['source'],'./')
        self.assertTrue(isinstance(obj.get('description'),str) and obj['description'].strip())


if __name__ == '__main__':
    unittest.main()
