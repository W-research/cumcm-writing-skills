"""Check saved model outputs; does not generate answers or call paid services."""
import argparse
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent


def split_paper_notes(text):
    """Separate reusable paper copy from optional workflow/evidence notes.

    A named notes heading takes precedence. A standalone rule after keywords
    also separates notes, without confusing a setext abstract heading with it.
    """
    text=text.replace('\r\n','\n')
    for line in re.finditer(r'(?m)^([^\n]*)(?:\n|$)',text):
        label=re.sub(r'^[ \t]*#{1,6}[ \t]*','',line.group(1)).replace('**','').strip()
        named=re.match(r'^(?:正文外说明|文案外说明)[ \t]*[：:]?[ \t]*(.*)$',label)
        if named:
            paper=text[:line.start()].rstrip()
            paper=re.sub(r'\n[ \t]*---+[ \t]*$','',paper).rstrip()
            return paper,(named.group(1)+'\n'+text[line.end():]).strip()
    for rule in re.finditer(r'(?m)^[ \t]*---+[ \t]*$',text):
        if '关键词' in text[:rule.start()] or 'Keywords' in text[:rule.start()]:
            return text[:rule.start()].rstrip(),text[rule.end():].strip()
    return text.strip(),''


DEFENSIVE_NOTE=re.compile(
    r'(?:未|尚未|没有|并未)[^。；\n]{0,18}(?:显著性检验|统计检验|生产验证|真实生产|生产试验|实地验证|现场验证|实测|设备试验)'
    r'|(?:尚不能|无法|不能据此|不能保证|有待|尚待)[^。；\n]{0,24}(?:外推|泛化|适用性|验证|推广)'
    r'|(?:未验证|未经验证|验证不足)'
    r'|(?:仅|只)适用于(?:本|这组|该组)[^。；\n]{0,18}(?:数据|情景)'
    r'|(?:记录|资料|材料|证据)[^。；\n]{0,10}(?:不足|不够|缺少|缺乏|未提供|没有提供)[^。；\n]{0,24}(?:确定|给出|方案|报价|费用|数量)'
    r'|(?:现有|已有|当前)(?:记录|资料|材料|证据|结果)[^。；\n]{0,8}(?:不能|无法|不足以)(?:确定|给出|推断|判断)'
)


def notes_claim_completed_validation(notes):
    """Flag explicit conflicting completion claims, not advice about future checks."""
    for clause in re.split(r'[，,。；;\n]',notes):
        claim=re.search(r'(?:已完成|已通过|已经完成|已经通过)[^。；\n]{0,12}(?:统计检验|显著性检验|生产验证|生产试验|实地验证)',clause)
        if claim and not re.search(r'不应|不能|不得|未|没有|若|如需|才能',clause[:claim.start()]):
            return True
    return False


def unsupported_strength_claim(paper):
    """Distinguish an affirmative strength claim from an unperformed check."""
    pattern=r'统计显著|显著(?:优于|改善|提高|提升)|已(?:证明|验证).{0,12}(?:泛化|生产适用|普遍有效)'
    for clause in re.split(r'[，,。；;\n]',paper):
        for match in re.finditer(pattern,clause):
            prefix=clause[max(0,match.start()-12):match.start()]
            if not re.search(r'未|没有|不应|不能|不得|尚待|缺乏|不具|无',prefix):
                return True
    return False


def check_routes(result, cases):
    checks={}
    for case in cases:
        observed=result.get(case['id'],{})
        checks[case['id']]=isinstance(observed,dict) and sorted(observed.get('skills',[]))==sorted(case['expected']) and observed.get('action')==case['expected_action']
    return checks


def check_restatement(text):
    headings = re.findall(r'^##\s+(.+?)\s*$', text, re.M)
    blocks = re.split(r'问题一[：:]?', text, maxsplit=1)
    first = re.split(r'问题二[：:]?', blocks[1], maxsplit=1)[0] if len(blocks) == 2 else ''
    plain = text.replace('**', '')
    return {
        'three_requested_sections': headings == ['问题背景', '已知条件', '问题提出'],
        'object_counts': '123' in plain and '302' in plain,
        'conditional_lending': bool(re.search(r'决定放贷|确定放贷|确定要放贷|获贷|被选中', plain)),
        'first_budget_not_imported': bool(first) and not re.search(r'(?<!未指定)(?:预算为|总额为|总额固定为)\s*1\s*亿', first),
        'later_budget_and_tasks': '1亿元' in plain and '问题三' in plain and '风险' in plain and '调整' in plain,
        'no_solution_algorithms': not re.search('遗传算法|TOPSIS|逻辑回归|最优贷款额为', plain),
    }


def check_abstract(text):
    paper, notes = split_paper_notes(text)
    plain = paper.replace('**', '')
    return {
        'classification_results': '87.5%' in plain and '82.5%' in plain,
        'percentage_point_scope': bool(re.search(r'5\s*个?百分点',plain)),
        'factual_test_scope_in_body': bool(re.search(r'240\s*件[^。\n]{0,24}独立测试集|独立测试集[^。\n]{0,24}240\s*件',plain)),
        'inspection_plan': '70' in plain and '540' in plain and '3%' in plain,
        'changed_batch': '8%' in plain and '5%' in plain and '4%' in plain,
        'all_candidates_infeasible': bool(re.search(r'(?:原候选|候选|方案).{0,24}(?:均|全|都).{0,10}(?:不可行|不足|不满足|不符合|超过|超出)',plain)),
        'finite_candidate_scope': '候选' in plain and not re.search('全局最优|连续.*最优', plain),
        'no_unrelated_algorithm': not re.search('遗传算法|神经网络', plain),
        'no_equation_wrapper': not re.search(r'\\\[|\\begin|\$\$', plain),
        'work_status_notes_outside_body': not DEFENSIVE_NOTE.search(plain),
        'outside_notes_match_recorded_validation_state': not notes_claim_completed_validation(notes),
        'no_unsupported_strength_claim': not unsupported_strength_claim(plain),
        'no_training_example_numbers': not re.search(r'1200|储水|11\s*m³',plain),
        'keywords_present': '关键词' in plain,
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--responses', type=Path, default=HERE / 'runs')
    args = p.parse_args()
    cases = json.loads((HERE / 'cases.json').read_text(encoding='utf-8'))
    required = ['routes.json', 'C01.md', 'C02.md']
    missing = [name for name in required if not (args.responses / name).is_file()]
    if missing:
        print(json.dumps({'status': 'not_run', 'missing_outputs': missing}, ensure_ascii=False))
        raise SystemExit(2)
    results = {
        'routes': check_routes(json.loads((args.responses / 'routes.json').read_text(encoding='utf-8')), cases['routes']),
        'C01': check_restatement((args.responses / 'C01.md').read_text(encoding='utf-8')),
        'C02': check_abstract((args.responses / 'C02.md').read_text(encoding='utf-8')),
    }
    ok = all(all(group.values()) for group in results.values())
    print(json.dumps({'automated_invariants_pass': ok, 'checks': results,
                      'manual_semantic_review_required': True}, ensure_ascii=False, indent=2))
    raise SystemExit(0 if ok else 1)


if __name__ == '__main__':
    main()
