# CUMCM Writing Skills

[English](README.md) | 中文

CUMCM Writing Skills 是一组用于数学建模竞赛论文写作的智能体 Skill，共五个，覆盖问题重述、问题分析、模型假设、标题摘要关键词，以及可在 Word 中用 MathType 转换的公式源码。默认面向全国大学生数学建模竞赛（国赛/CUMCM），也可按电工杯、华数杯、MathorCup 等比赛的模板使用。

它们把题目、你的模型和结果整理成论文章节：保全题目中的每个子任务和约束，结果连同取得它的范围一起写清，尚未完成的检验放在正文之外。模型求解仍由你完成。插件支持 Claude Code 和 Codex。

## 首个版本

0.1.0 是首个公开版本，指令和目录结构仍可能调整。提交前请对照你自己的模型和结果逐节核对生成的内容。

## 五个 Skill

| Skill | 用途 |
|---|---|
| `cumcm-problem-restatement` | 整理背景、已知条件和逐问任务，检查题意遗漏 |
| `cumcm-problem-analysis` | 解释建模思路、选型理由、检验方式与问题间关系 |
| `cumcm-model-assumptions` | 筛选必要假设，说明依据、适用范围与模型作用 |
| `cumcm-abstract` | 根据已有结果整理标题、摘要和关键词 |
| `mathtype-texvc` | 准备贴到 Word 的公式，排查 MathType 转换失败或公式偏移 |

## 示例

下面是一个合成任务中问题重述的前后对比。

> 根据附件建立模型，分析服务站风险，给出最优补助方案。

> 面向有维修记录和无维修记录的两类服务站，分别量化维护风险，并在给定总额内安排补助。对选中站点保留单站金额限制；后续停水情景下重新评估影响，给出调整安排。

后者写明了两类对象、任务、约束和情景变化，也没有把“给出方案”擅自升级为已证明的最优。

每个 Skill 的 `references/worked-example.md` 都有一份完整的合成算例。[examples/official-2020-c](examples/official-2020-c/README.md) 用国赛 2020 年 C 题的官方题面和附件演示四个章节如何衔接。

## 安装

### Claude Code

```text
/plugin install cumcm-writing-skills --marketplace W-research/cumcm-writing-skills
```

会话中使用这条命令需要 Claude Code v2.1.275 或更新版本，在终端中使用需要 v2.1.292 或更新版本。较旧版本先添加市场再安装：

```text
/plugin marketplace add W-research/cumcm-writing-skills
/plugin install cumcm-writing-skills@cumcm-writing-skills
```

试用本地副本可运行 `claude --plugin-dir ./cumcm-writing-skills`。详见[官方插件文档](https://code.claude.com/docs/en/discover-plugins)。

### Codex

`.codex-plugin/plugin.json` 指向 `skills/` 目录。也可以按你的 Codex 安装方式单独加载某个 Skill 目录。

### 单独使用一个 Skill

复制整个 `skills/<skill-name>/` 目录，连同其中的 `references/`、`LICENSE` 和第三方声明。每个 Skill 需要的链接都在自己的目录里，可以单独上传或安装。章节 Skill 不依赖 `mathtype-texvc`，只有你要求输出 MathType 公式时才会用到它。

## 使用

- 说明比赛和章节，例如“这是国赛论文，帮我写模型假设”。
- “帮我写第一部分”这类不明确的请求会先确认章节；普通课程论文摘要不在范围内。
- 只要求审查时只给意见；明确要求修改文件时才会写回。
- 如果同时安装了功能宽泛的论文写作 Skill，两者可能同时加载，请直接点名要用的 Skill。

## 竞赛 AI 使用规定

国赛 2026 年规定：在参考文献前写 AI 工具使用声明；使用了 AI 的，在支撑材料中提交 `AI工具使用详情.pdf`，记录工具、用途、提示过程以及对输出的采纳、修改和核验情况。核心建模与分析须由参赛队主导，AI 参与的内容须经人工审查核实。其他比赛以各自当届规定为准。详见[本地要点](skills/cumcm-abstract/references/competition-compliance.md)和[官方规定](https://www.mcm.edu.cn/html_cn/node/fef94648f2836ab6cc81586f4c38512b.html)。

## 开发

```sh
python -m unittest discover -s evals -p 'test_*.py' -v
python evals/check_outputs.py --responses evals/runs
python evals/check_freshness.py
```

这些检查只读本地文件，不调用模型。Skill 指纹变化默认只给警告，修改错别字、链接不会被挡住；正式发版前运行 `python evals/check_freshness.py --release`。模型输出的生成与检查方式见 [evals/README.md](evals/README.md)，各层验证见 [docs/validation.md](docs/validation.md)。MathType 实测按[手工测试清单](skills/mathtype-texvc/references/manual-tests.md)记录。

欢迎提交 Issue 和 Pull Request。

## 许可证

项目自有内容采用 [MIT 许可证](LICENSE)。第三方版权与许可见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。本仓库不分发官方赛题和数据，请从官方渠道获取。
