# CUMCM Writing Skills

作者 **W** · **0.1.0** · **MIT**

把题意、模型与结果写成清楚的数学建模竞赛论文章节。默认面向国赛，也可按电工杯、华数杯、MathorCup等比赛模板适配。

## 改写能改变什么

下面是一个合成任务中的问题重述对比。

**改写前**

> 根据附件建立模型，分析服务站风险，给出最优补助方案。

**改写后**

> 面向有维修记录和无维修记录的两类服务站，分别量化维护风险，并在给定总额内安排补助。对选中站点保留单站金额限制；后续停水情景下重新评估影响，给出调整安排。

后者明确了对象差异、任务、约束和情景变化，也没有把“给出方案”擅自升级为已证明最优。各Skill自带更多完整输入、参考输出与反例。

## 安装

### Claude Code：一条命令添加市场并安装

~~~text
/plugin install cumcm-writing-skills --marketplace W-research/cumcm-writing-skills
~~~

会话中的该写法需Claude Code v2.1.275或更新版本；终端形式需v2.1.292或更新版本。较旧版本可分两步：

~~~text
/plugin marketplace add W-research/cumcm-writing-skills
/plugin install cumcm-writing-skills@cumcm-writing-skills
~~~

下载到本地后，也可用：

~~~text
/plugin marketplace add ./cumcm-writing-skills
/plugin install cumcm-writing-skills@cumcm-writing-skills
~~~

或在终端用 claude --plugin-dir ./cumcm-writing-skills 试用。命令和版本要求见 [官方安装文档](https://code.claude.com/docs/en/discover-plugins)。市场入口位于 .claude-plugin/marketplace.json。

### 单独使用一个Skill

复制 skills/<skill-name>/ 整个目录，保留参考文件、LICENSE和第三方声明。每个Skill的必需链接都限制在自身目录中，支持按客户端要求单独上传或安装。MathType联用是可选能力；单独安装章节Skill仍能完成普通文字工作。

Codex可使用 .codex-plugin/plugin.json，或按其Skill安装方式加载单独目录。实际调用名以客户端显示结果为准。

## 五个职责

| Skill | 常见请求 |
|---|---|
| cumcm-problem-restatement | 整理背景、已知条件和逐问任务，检查题意遗漏 |
| cumcm-problem-analysis | 解释建模思路、选型理由、检验与问题间关系 |
| cumcm-model-assumptions | 筛选必要假设，解释依据、范围与模型作用 |
| cumcm-abstract | 从已有结果整理标题、摘要和关键词 |
| mathtype-texvc | 准备贴到Word的公式，排查MathType转换失败或位置异常 |

明确数模竞赛上下文后再选择章节。“帮我写第一部分”等不明确请求先澄清；普通课程论文摘要不是竞赛摘要任务。只审查给意见，要求改写给限定范围的稿件，明确要求修改文件才写回。

如果同时安装功能宽泛的论文Skill，可显式指定要用本插件的哪个章节Skill。不同客户端可能同时激活多个匹配项；本插件不修改其他插件的触发规则。

需要只评估本插件时，使用仅启用本插件的独立项目。显式点名一个章节Skill，并不能保证另一个写着“任何部分都必须使用”的Skill不会同时加载。

## 从输入到正文

合成储水例展示四节如何协作：重述保全任务，分析解释水量平衡和有限候选比较，假设检查独立观测，摘要保留实际答案和条件。完整示例位于各Skill的 references/worked-example.md。

更复杂的 [官方2020 C示例](examples/official-2020-c/README.md) 展示真实题面和附件信息差异。重述和分析Skill的日常参考入口直接指向各自目录内的官方版本，单独安装时也能读取。

## 测试与贡献

~~~sh
python -m unittest discover -s evals -p 'test_*.py' -v
python evals/check_outputs.py --responses evals/runs
python evals/check_freshness.py
~~~

前两项检查本地结构、独立安装、规则和已保存输出，不调用模型。指纹变化默认只警告；错别字、链接修复等贡献不因缺少模型权限被阻塞。正式发版可运行 python evals/check_freshness.py --release 严格检查，并评估哪些用例需要重跑。

[测试说明](evals/README.md) 区分静态检查、插件独立环境生成、共装冲突和人工检查。新增测试应覆盖任务含义与证据边界，不只匹配关键词。

## Word / MathType 手工测试

使用 [十项测试清单](skills/mathtype-texvc/references/manual-tests.md) 记录Word与MathType版本、实际转换入口、截图和结果。测试表接受后续真实通过或失败记录；语法依据、官方文档和原生实测保持分开。

长期使用经验可登记为 `author_usage`，只要求Word和MathType版本，不要求截图；具体用例的 `pass` 仍保留版本和证据要求。作者使用经验与逐项测试相互补充，不混为一类。

## 使用边界与竞赛合规

这套工具辅助组织和核对材料，模型求解、结果核验和提交责任仍由作者承担。参考示例中的数值不自动属于当前研究，插件不承诺奖项或查重结果。

国赛2026要求在参考文献前声明AI使用情况；使用AI时提交“AI工具使用详情.pdf”，记录工具版本、用途、提示过程，以及采纳、修改与核验情况。后者的记录项有语言润色例外，并不免除声明或人工责任。其他竞赛遵守各自当届要求。详见 [本地合规要点](skills/cumcm-abstract/references/competition-compliance.md) 和 [官方规定](https://www.mcm.edu.cn/html_cn/node/fef94648f2836ab6cc81586f4c38512b.html)。

自有内容使用MIT。第三方版权和许可见 [THIRD_PARTY_NOTICES](THIRD_PARTY_NOTICES.md)；原始赛题和数据从官方来源获取。
