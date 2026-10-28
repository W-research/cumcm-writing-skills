# 参与贡献

[English](CONTRIBUTING.md) | 中文

感谢你帮助改进 CUMCM Writing Skills。

## 反馈问题

提交 Issue 时请写明：

- 用的是哪个 Skill；
- 你发出的请求；
- 输出中有问题的部分，以及你期望的结果；
- 所用客户端及版本（Claude Code、claude.ai 或 Codex）。

比赛进行期间，不要在 Issue 里贴赛题解答或论文内容。Issue 是公开的，竞赛规则限制比赛期间与队外交流。需要复现时，请改用往届题目或自拟的题目。

## 修改内容

- 每个 Skill 在 `skills/<skill-name>/` 目录下。`SKILL.md` 保持简短，较长的说明和示例放在 `references/` 里。
- 每个 Skill 需要的链接都要留在它自己的目录里，这样单独安装时也能用。
- 有些文件复制到了各 Skill 目录中，修改时先改原件，并在同一次修改里同步所有副本：`examples/official-2020-c/source.json` 复制为四个 Skill 中的 `references/official-2020-c-source.json`，`licenses/` 里的许可证复制到了两个 Skill 中。
- 评测材料不要进入 Skill：`evals/inputs/` 里的数字和场景不能出现在 `skills/` 下，测试会拒绝。
- 每个示例都要注明来源：合成题、官方赛题，或作者整理的教学材料。

## 检查

```sh
python -m unittest discover -s evals -p 'test_*.py' -v
python evals/check_outputs.py --responses evals/runs
python evals/check_freshness.py
```

这些检查只用 Python 标准库，Python 3.11 及以上即可。GitHub Actions 会在每次推送和 Pull Request 时运行同样的命令。

修改 Skill 指令后，`check_freshness.py` 会提示 `evals/runs/` 中保存的模型输出已过期。提交 Pull Request 不需要重跑模型；维护者会在发版前重跑受影响的用例，再用 `python evals/check_freshness.py --release` 检查。重跑方式见 [evals/README.md](evals/README.md)。

## Pull Request

- 每个 Pull Request 只做一件事，写清改了什么、为什么改。
- 用户能感知到的改动，在 [CHANGELOG.md](CHANGELOG.md) 顶部的 `Unreleased` 标题下加一行。
- 按平常的习惯提交即可，不需要把一次改动拆成很多个小提交。

## 许可证

提交贡献即表示你同意贡献内容按 [MIT 许可证](LICENSE) 发布。
