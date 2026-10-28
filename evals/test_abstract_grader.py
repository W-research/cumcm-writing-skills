"""Grader controls: reward bounded results, not defensive paper prose."""
import unittest
from check_outputs import check_abstract, split_paper_notes

PAPER='''# 产品质量检验

## 摘要

在240件产品的独立测试集上，逻辑回归与规则基线的准确率分别为87.5%和82.5%，提高5个百分点。
在漏检率不超过4%的条件下，给定候选中选择70件/天、540元/天、漏检率3%的方案。
新批次中三个原候选的漏检率分别为11%、8%、5%，均超出4%上限，三个原候选全部不可行，需扩展候选集合。

关键词：逻辑回归；质量检验；有限候选
'''
NOTES='研究记录未提供统计显著性检验，未做真实生产验证；外推到其他批次需要另外的证据。'


class AbstractGraderTests(unittest.TestCase):
    def test_bounded_results_need_no_disclaimer(self):
        self.assertTrue(all(check_abstract(PAPER).values()))

    def test_notes_after_rule_or_named_heading_are_allowed(self):
        for separator in ['\n---\n\n正文外说明\n','\n## 正文外说明\n','\n正文外说明：\n','\n---\n','\n**正文外说明：** ']:
            with self.subTest(separator=separator):
                output=PAPER+separator+NOTES
                self.assertTrue(all(check_abstract(output).values()))
                body,notes=split_paper_notes(output)
                self.assertNotIn('未做真实生产验证',body)
                self.assertIn('未做真实生产验证',notes)

    def test_old_defensive_body_fails(self):
        bad=PAPER.replace('提高5个百分点。','提高5个百分点，但未进行统计显著性检验，尚不能据此判断其对其他批次的适用性。')
        self.assertFalse(check_abstract(bad)['work_status_notes_outside_body'])
        self.assertFalse(check_abstract(PAPER+'只适用于这组测试数据与合成情景，未做真实生产验证。')['work_status_notes_outside_body'])

    def test_material_gaps_belong_in_notes_not_body(self):
        for note in ['现有记录尚不足以确定新的复检数量及对应费用。',
                     '当前资料不足以给出新方案或报价。',
                     '现有结果不能确定满足约束的新复检数量及相应费用。']:
            with self.subTest(note=note):
                self.assertFalse(check_abstract(PAPER+note)['work_status_notes_outside_body'])
                self.assertTrue(all(check_abstract(PAPER+'\n---\n正文外说明\n'+note).values()))

    def test_unperformed_check_is_not_an_affirmative_claim(self):
        output=PAPER+'但未进行统计显著性检验。'
        self.assertTrue(check_abstract(output)['no_unsupported_strength_claim'])
        self.assertFalse(check_abstract(output)['work_status_notes_outside_body'])

    def test_notes_cannot_supply_missing_results(self):
        output='# 摘要\n建立了模型并求解。\n关键词：检验\n---\n'+PAPER
        checks=check_abstract(output)
        self.assertFalse(checks['classification_results'])
        self.assertFalse(checks['inspection_plan'])
        self.assertFalse(checks['factual_test_scope_in_body'])

    def test_factual_scope_must_be_in_paper(self):
        output=PAPER.replace('在240件产品的独立测试集上，','')+'\n---\n使用240件产品的独立测试集。'
        self.assertFalse(check_abstract(output)['factual_test_scope_in_body'])

    def test_required_negative_result_is_not_defensive(self):
        self.assertTrue(check_abstract(PAPER)['all_candidates_infeasible'])
        self.assertTrue(check_abstract(PAPER)['work_status_notes_outside_body'])

    def test_unsupported_positive_claim_still_fails(self):
        bad=PAPER.replace('提高5个百分点。','提高5个百分点，统计显著且已证明生产适用。')
        self.assertFalse(check_abstract(bad)['no_unsupported_strength_claim'])

    def test_outside_notes_cannot_invent_completed_validation(self):
        self.assertFalse(check_abstract(PAPER+'\n---\n已完成生产验证。')['outside_notes_match_recorded_validation_state'])
        self.assertTrue(check_abstract(PAPER+'\n---\n不能声称已完成生产验证。')['outside_notes_match_recorded_validation_state'])

    def test_setext_abstract_heading_not_notes_separator(self):
        body,notes=split_paper_notes('摘要\n---\n在240件独立测试集上。\n关键词：测试')
        self.assertIn('240',body)
        self.assertEqual(notes,'')


if __name__=='__main__':
    unittest.main()
