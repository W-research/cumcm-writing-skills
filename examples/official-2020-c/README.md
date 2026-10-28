# 官网2020 C：贯穿四节的真实数据示例

题目为“中小微企业的信贷决策”，来源是 [全国大学生数学建模竞赛官网2020年赛题](https://www.mcm.edu.cn/html_cn/node/10405905647c52abfd6377c0311632b5.html)。原始题面与附件从官网获取，读取范围、文件哈希及元数据核对见 [来源清单](source.json)。

## 按章节阅读

| 阶段 | 权威示例入口 | 关注点 |
|---|---|---|
| 重述 | [题面事实与完整重述](../../skills/cumcm-problem-restatement/references/example-credit.md) | 对象、条件、预算适用范围、全部三问 |
| 分析 | [数据条件与三问方案](../../skills/cumcm-problem-analysis/references/examples-finance-evaluation.md) | 标签、样本单位、迁移、冲击与检验 |
| 假设 | [候选前提与适用边界](../../skills/cumcm-model-assumptions/references/official-credit-assumptions.md) | 票据代理、跨期关系、公共特征和情景 |
| 摘要 | [事实与完成状态](../../skills/cumcm-abstract/references/official-credit-evidence.md) | 哪些信息能写，哪些结果需要求解后补全 |

完整示例保存在各自Skill内部，单独安装仍能使用。此页只做导航，避免维护两份同名章节的不同版本。

## 已核对什么

读取完整题面、三个附件的工作表结构，以及附件1全部123条企业基本信息。附件1有评级与违约字段，附件2基本表没有这些字段；负数发票与作废发票含义不同。题面共同约束、三问对象和预算范围均在章节示例中回指来源。

该案例覆盖数据驱动任务、信息迁移和需要明确的模型口径。风险模型、贷款配置和冲击策略尚未计算，因此分析和假设采用方案级表达，摘要提供证据准备而非虚构的终稿结果。它不是获奖论文的复刻。
