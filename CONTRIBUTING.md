# Contributing

English | [中文](CONTRIBUTING.zh.md)

Thanks for helping improve CUMCM Writing Skills.

## Reporting problems

Open an issue and include:

- which skill you used;
- the request you gave;
- the relevant part of the output, and what you expected instead;
- the client and its version (Claude Code, claude.ai or Codex).

Do not post contest solutions or paper content while a contest is running. Issues are public, and contest rules restrict communication outside the team during the contest. Reproduce the problem with a past or made-up problem instead.

## Making changes

- Each skill lives in `skills/<skill-name>/`. Keep `SKILL.md` short and put long explanations and examples in `references/`.
- Every link a skill needs must stay inside its own folder, so that the skill also works when installed on its own.
- Some files are copied into the skill folders. Edit the original and update every copy in the same change: `examples/official-2020-c/source.json` is copied to `references/official-2020-c-source.json` in four skills, and the license texts in `licenses/` are copied to two skills.
- Keep evaluation material out of the skills: numbers and scenarios from `evals/inputs/` must not appear under `skills/`. The tests reject it.
- Mark where every example comes from: synthetic, an official contest problem, or the author's teaching notes.

## Checks

```sh
python -m unittest discover -s evals -p 'test_*.py' -v
python evals/check_outputs.py --responses evals/runs
python evals/check_freshness.py
```

The checks use only the Python standard library and run on Python 3.11 or later. GitHub Actions runs the same commands on every push and pull request.

When you change a skill's instructions, `check_freshness.py` warns that the saved model outputs in `evals/runs/` are out of date. You do not need to rerun the models for a pull request; the maintainer reruns the affected cases before a release and then checks with `python evals/check_freshness.py --release`. See [evals/README.md](evals/README.md) for how those runs are made.

## Pull requests

- Keep one topic per pull request and say what changed and why.
- For changes users will notice, add a line under an `Unreleased` heading at the top of [CHANGELOG.md](CHANGELOG.md).
- Commit the way you normally would; there is no need to split a change into many small commits.

## License

By contributing, you agree that your contribution is released under the [MIT License](LICENSE).
