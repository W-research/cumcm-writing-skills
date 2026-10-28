# Texvc profile, product differences and evidence

## Sources

- [Wiris: MathType 7 with Microsoft Office 2016 or later](https://docs.wiris.com/en_US/mathtype-7-with-microsoft-office-2016-or-later), section “Typing TeX directly into Word (Toggle TeX)”: desktop Toggle TeX uses Texvc; inline input is $...$ and display input is \[...\].
- [Wikimedia parser.pegjs at 7d896329a1387bb58a7fd6388f8b212434911e59](https://github.com/wikimedia/mediawiki-services-texvcjs/blob/7d896329a1387bb58a7fd6388f8b212434911e59/lib/parser.pegjs): syntax-reference snapshot. It is not a disclosed MathType build's source.
- [Wiris HTML integration LaTeX support](https://docs.wiris.com/en_US/mathtype-for-html-formats-standards/latex-support): double-dollar detection belongs to the HTML integration.
- [Native-test status](test-matrix.md): separates documentation, grammar and actual application evidence.

No parser code is bundled. This is W's independently written usage guidance, not a copy of the grammar or a statement that all product versions implement it.

## Grammar-informed output profile

Texvc is a fixed grammar, not a full LaTeX document processor. The inspected grammar has these matrix-like environment rules:

| Environment | Argument |
|---|---|
| matrix, pmatrix, bmatrix, Bmatrix, vmatrix, Vmatrix, smallmatrix | none |
| cases | none |
| array | column specification, e.g. {rl} |
| align, aligned | no column count |
| alignat, alignedat | column count, e.g. {2} |

The presence of align and aligned in this grammar does not establish a minimum MathType version. Prefer align in new desktop output, but keep a working alternative when the user's tested environment supports it. array with an explicit specification is another candidate fallback, to be verified in that environment.

In this profile avoid document environments (equation, starred align, gather, multline, split, eqnarray), numbering commands (\tag, \label, \eqref, \notag, \nonumber) and custom macro definitions. The reference grammar's unknown-environment/function branches explain many “Illegal TeX function” errors; version and route still matter.

Literal percent and dollar signs need escaping. Prefer \mathbb and \mathbf to deprecated aliases. Use command-form operators (\leq, \times, \in, \infty, \to), and place ordinary prose outside math. Short labels may use \text or \mbox, subject to the selected parser and font support.

## Source examples, not native test reports

~~~text
$\frac{a}{b}$
\[ \frac{a+b}{c-d} \]
\[ \sum_{i=1}^{n} i^2=\frac{n(n+1)(2n+1)}{6} \]
\[ \begin{pmatrix}a&b\\c&d\end{pmatrix} \]
\[ \begin{cases}x+y=1\\x-y=0\end{cases} \]
\[ \begin{align}a&=b+c\\&=d+e\end{align} \]
\[ \begin{aligned}a&=b+c\\&=d+e\end{aligned} \]
\[ \begin{array}{rl}a&=b+c\\&=d+e\end{array} \]
\[ \begin{alignat}{2}x&=1,&\quad y&=2\\x&=3,&\quad y&=4\end{alignat} \]
~~~

Each display example is a single paragraph. These are profile examples, not proof of successful conversion in Word. Test meaning and layout after native conversion when that deliverable is required.

## Delimiters and commands are separate questions

Toggle TeX, Convert Equations, pasting into the MathType editor and web integration are distinct routes. Input wrappers may be recognised before the expression grammar runs, so a parser file alone cannot decide which wrapper a Word command recognises.

For Toggle TeX, default to the documented $...$ and \[...\]. The HTML manual explicitly supports $$...$$; that fact must neither be denied nor promoted into a claim about desktop Convert Equations. Ask which route failed and test that route when necessary.

## Word behaviour and verification

Wiris describes MTDisplayEquation styles with center/right tab stops and separate numbering controls. This supports checking document styles when alignment is wrong. It does not prove that every conversion always inserts the same tabs or that End → Tab works in every paragraph.

Prepare raw formula paragraphs left-aligned and without extra manual centering. Then verify the actual converted object, tab stops, automatic number fields and references in the target document. Rendering raw TeX in a PDF checks only pre-conversion layout. Installation paths, app versions and available preview tools must be discovered, not hardcoded.
