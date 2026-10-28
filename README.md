# CUMCM Writing Skills

[![skill-checks](https://github.com/W-research/cumcm-writing-skills/actions/workflows/checks.yml/badge.svg)](https://github.com/W-research/cumcm-writing-skills/actions/workflows/checks.yml)

English | [中文](README.zh.md)

CUMCM Writing Skills is a set of five agent skills for writing papers for Chinese mathematical modeling contests. They cover the problem restatement, problem analysis, model assumptions, title / abstract / keywords, and formula source that converts with MathType in Word. The default target is CUMCM (全国大学生数学建模竞赛); the same skills can follow the templates of other contests such as the Electrician Cup (电工杯), Huashu Cup (华数杯) and MathorCup.

The skills turn the problem statement, your model and your results into paper sections. They keep every sub-task and constraint from the problem, state each result together with the scope it was obtained in, and keep unfinished checks out of the paper text. They do not solve the model for you. Output is written in Chinese. The plugin works with Claude Code and Codex.

## Early release

Version 0.1.0 is the first public release. Instructions and file layout may still change. Check every generated section against your own model and results before you submit.

## Skills

| Skill | Use it for |
|---|---|
| `cumcm-problem-restatement` | Background, given conditions and per-question tasks, with a check for missed sub-tasks |
| `cumcm-problem-analysis` | Modeling route, reasons for the chosen model, validation and links between questions |
| `cumcm-model-assumptions` | Necessary assumptions, their basis, scope and role in the model |
| `cumcm-abstract` | Title, abstract and keywords built from results you already have |
| `mathtype-texvc` | Formula source to paste into Word, and fixes when MathType conversion fails or shifts |

## Example

A problem restatement from a synthetic task, before and after:

> 根据附件建立模型，分析服务站风险，给出最优补助方案。
>
> *Build a model from the attachments, analyse station risk and give the optimal subsidy plan.*

> 面向有维修记录和无维修记录的两类服务站，分别量化维护风险，并在给定总额内安排补助。对选中站点保留单站金额限制；后续停水情景下重新评估影响，给出调整安排。
>
> *For stations with and without maintenance records, quantify maintenance risk separately and allocate subsidies within the given total. Keep the per-station limit for selected stations; under the later water-outage scenario, reassess the impact and give an adjusted plan.*

The second version names the two kinds of objects, the task, the constraint and the scenario change, and it does not turn "give a plan" into a claim of a proven optimum.

Each skill ships a complete synthetic worked example in `references/worked-example.md`. [examples/official-2020-c](examples/official-2020-c/README.md) walks through the official CUMCM 2020 Problem C statement and its attachments.

## Install

### Claude Code

```text
/plugin install cumcm-writing-skills --marketplace W-research/cumcm-writing-skills
```

This form needs Claude Code v2.1.275 or later inside a session, or v2.1.292 or later from the terminal. On older versions, add the marketplace first:

```text
/plugin marketplace add W-research/cumcm-writing-skills
/plugin install cumcm-writing-skills@cumcm-writing-skills
```

To try a local copy, run `claude --plugin-dir ./cumcm-writing-skills`. See the [official plugin docs](https://code.claude.com/docs/en/discover-plugins) for details.

### Codex

`.codex-plugin/plugin.json` points Codex at the `skills/` folder. You can also load a single skill folder the way your Codex setup installs skills.

### A single skill

Copy the whole `skills/<skill-name>/` folder, including its `references/`, `LICENSE` and third-party notices. Every link a skill needs stays inside its own folder, so each one can be uploaded or installed on its own. The chapter skills work without `mathtype-texvc`; they only use it when you ask for MathType formulas.

## Usage

- Name the contest and the section, for example "这是国赛论文，帮我写模型假设".
- A vague request such as "帮我写第一部分" gets a clarifying question. Ordinary course-paper abstracts are out of scope.
- A review request returns comments only. Files are changed only when you explicitly ask.
- If a broad paper-writing skill is also installed, both may load. Name the skill you want to use.

## Contest AI rules

The CUMCM 2026 rules ask for an AI-use statement before the references and, when AI was used, an `AI工具使用详情.pdf` in the supporting materials that records tools, purposes, prompts and how outputs were adopted and checked. Core modeling and analysis must be led by the team, and AI-generated content must be reviewed by people. Other contests follow their own rules for the current year. See the [local summary](skills/cumcm-abstract/references/competition-compliance.md) and the [official rules](https://www.mcm.edu.cn/html_cn/node/fef94648f2836ab6cc81586f4c38512b.html).

## Roadmap

Planned skills, in no fixed order:

- **Notation check** (符号说明): check that every symbol is defined once and used consistently across the paper.
- **Sensitivity analysis write-up** (灵敏度分析): write the section from sensitivity results you already have.
- **Model evaluation and extension** (模型评价与推广): state the strengths, limits and extensions that the paper's results support.

Writing the model establishment and solving section is not planned. That is the team's core work, and the contest rules require the team to lead it. Suggestions are welcome in issues.

## Development

```sh
python -m unittest discover -s evals -p 'test_*.py' -v
python evals/check_outputs.py --responses evals/runs
python evals/check_freshness.py
```

The checks use only the Python standard library. Python 3.11 or later is enough, and CI runs on 3.11. They read local files only and never call a model. A changed skill fingerprint only produces a warning, so typo and link fixes are not blocked; run `python evals/check_freshness.py --release` before a release. See [evals/README.md](evals/README.md) for how model outputs are generated and checked, and [docs/validation.md](docs/validation.md) for the validation levels. MathType results are recorded with the [manual test checklist](skills/mathtype-texvc/references/manual-tests.md).

Some files are copied into the skill folders so that each skill also works when installed on its own. `examples/official-2020-c/source.json` is copied to `references/official-2020-c-source.json` in four skills, and the upstream license texts in `licenses/` are copied to two skills. Edit the original and update every copy in the same change; the tests check that the copies match.

See [CONTRIBUTING.md](CONTRIBUTING.md) for how to report problems and submit changes. Issues and pull requests are welcome.

## License

Project content is released under the [MIT License](LICENSE). Third-party copyrights and licenses are listed in [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md). Official contest problems and data are not redistributed here; get them from the official sources.
