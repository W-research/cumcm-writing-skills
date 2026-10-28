---
name: mathtype-texvc
description: Prepare or repair math to paste into Word and convert with MathType. Use for MathType, Toggle TeX, 切换TeX, Texvc, 贴到Word、公式转换失败、公式偏右 or missing equation numbering. Preserve mathematical meaning and distinguish desktop conversion routes; not a restriction on ordinary LaTeX.
license: MIT
---

# MathType / Texvc formula source

This skill targets **MathType 7 desktop Toggle TeX in Word** unless the user names another product or conversion command. Preserve the mathematical meaning, symbols, values and requested edit scope.

作者长期使用 **Word 2016（16.0.20527.20088）/ MathType 7.8.2.441**，登记为 `author_usage`。常规回答直接给出操作建议；涉及版本兼容或测试结果时，按[使用与测试记录](references/test-matrix.md)说明证据范围。

## Evidence and entry point

Read [compatibility and evidence](references/texvc-reference.md) for uncertain syntax, product differences or a reported failure. The [evidence table](references/test-matrix.md) distinguishes official documentation, grammar, author usage and per-case tests; none substitutes for another.

For a user-run native check, provide the [ten-case checklist](references/manual-tests.md) and record results in its linked versioned test file.

## What belongs inside math

Mark mathematical variables and expressions as math, including a single letter: write `$a$`, `$n$` or `$x_i$` for a parameter, sample count or indexed variable. Keep ordinary prose outside the delimiters: write `$n$ 个样本`, not `$n 个样本$`. A plain letter used as a section label or ordinary text is not automatically a variable. Units and short operator labels inside a formula can use an appropriate upright form such as `\mathrm{m}`.

Math markup and the converter's detection are separate issues. Some desktop builds do not auto-convert an isolated symbol with Toggle TeX; if `$a$` remains text, use MathType's Insert Inline Equation route for that symbol. Do not append an artificial `+0` merely to force detection or change the mathematical meaning.

## Default source profile

For desktop Toggle TeX, use inline $...$ and display \[...\], as documented by Wiris. Keep a display expression, including both delimiters, in one selectable paragraph. Visual soft wrapping is fine.

~~~text
\[ r_t=(S_t-S_{t-1})-(I_t-O_t) \]
~~~

Prefer familiar command forms such as \leq, \times and \in. Escape literal percent and dollar signs as \% and \$. Keep prose outside math where practical; short labels can use \text{} or \mbox{}.

Use matrix-family environments, cases, array with column specification, or align for multi-line bodies. Check [the reference](references/texvc-reference.md) when other syntax is needed. Avoid document environments, numbering commands and custom macros in this output profile; describe a profile violation as such rather than asserting every MathType product rejects it.

### Dollar-delimited displays

For this desktop Toggle TeX workflow, generate \[...\] by default. **Do not claim that $$...$$ is unsupported by every MathType product or command.** Wiris documents double dollars for its HTML integration. Convert Equations is another command; test the user's version and input route before changing a working delimiter convention.

## Formula body and numbering

Deliver the body separately from the number. Use MathType Insert Number / Insert Reference or Word SEQ / REF fields for automatic numbering and references; plain typed numbers do not renumber.

A common desktop workflow is to select the TeX paragraph, use Toggle TeX, then place the insertion point at the desired numbering position and use Insert Number. The historical End → Tab → Insert Number shortcut depends on the paragraph's tab stops; inspect the actual layout rather than assuming that pressing Tab always reaches the right margin. For chapter-prefixed numbers, configure chapter/section breaks and number formatting. Verify that any break markers are not visibly printed.

Report numbering as instructions unless it was actually executed and read back. Do not insert \tag, \label, \eqref or literal equation numbers into a Texvc body to simulate Word fields.

## DOCX generation and preview

When producing plain TeX for later conversion, put each display formula in one **left-aligned** paragraph, preferably a readable monospace font. Avoid adding manual spaces or tabs to fake centering. MathType display styles can use tab stops; actual post-conversion alignment depends on the user's document and application version.

**Specific offset diagnosis:** if the converted display equation lands too far right, check whether the original TeX paragraph was center-aligned. Paragraph centering can combine with MathType's leading centering tab and shift the result again. Change the source paragraph to left alignment and reconvert in a scratch copy; the TeX body need not change. If the offset remains, inspect the display style and its center/right tab stops. This is a concrete troubleshooting rule, not a claim that every version has been tested.

Use an available document-generation skill or library. Discover its real path and supported tools at runtime; no fixed Claude-only directory is required. If LibreOffice is available, a preview can be made with:

~~~sh
soffice --headless --convert-to pdf --outdir preview document.docx
~~~

Inspect the PDF or render it with an available PDF tool. This verifies the pre-conversion document only. LibreOffice cannot prove that MathType OLE conversion, automatic numbering or post-conversion layout works. If preview or native conversion is unavailable, deliver editable source and state that specific verification gap.

## Failure diagnosis

Identify the product, version and exact command first when they affect the outcome. Inspect the smallest failing expression, then check:

1. Unsupported syntax in the selected profile, especially starred/document environments or custom macros.
2. Numbering mixed into the formula body.
3. Hard paragraph breaks separating display delimiters.
4. Unescaped literal characters or missing array/alignment arguments.
5. For a converted formula shifted right, first remove source-paragraph centering, then check the display style and tab stops if needed.

Explain the specific change, preserve the requested content, and retest only in an authorised scratch document. Reading or repairing source is not permission to overwrite the user's manuscript. Never report a native conversion, version compatibility or page layout as passed without actual evidence.
