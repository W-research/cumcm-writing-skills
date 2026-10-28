# 验证方式与结果

测试分为四层，结论按实际完成层级报告：

| 层级 | 验证内容 |
|---|---|
| 离线单元测试 | 清单、链接、独立Skill目录、隐私扫描、规则与失败控制 |
| 输出评估 | 已保存输出的必要条件和语义审阅 |
| 职责路由 | 单插件环境与加入宽泛论文Skill的冲突场景，分别记录 |
| 原生应用 | 客户端安装、Word/MathType转换、版面与编号的实际记录 |

本版机器检查摘要见 [validation-results.json](validation-results.json)，模型评估记录见 [运行清单](../evals/runs/manifest.json)。这类用例是抽样评估，不代表总体成功率或竞赛效果；正常输出、需要澄清及触发冲突应分别报告。

Skill与输入指纹用于标记证据版本。日常修改后只提示证据可能过期；正式发版可以选择严格检查。没有模型运行权限的贡献者仍可提交文字或结构修订。

MathType使用经验与原生测试从 [版本记录](../skills/mathtype-texvc/references/native-tests.json) 读取，测试方法见 [手工清单](../skills/mathtype-texvc/references/manual-tests.md)。`author_usage` 记录版本明确的长期使用经验，不要求截图；具体测试的 `pass` 需要该用例的证据。语法检查和使用经验均不计为逐项测试通过。

公开记录只保留相对路径、测试条件和结果，不包含个人安装清单、账号、令牌或本机目录。
