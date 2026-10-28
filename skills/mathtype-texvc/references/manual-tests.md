# Word / MathType 十项手工测试

使用新建测试文档，保留每项源码与截图。先记录Word“关于”页面中的版本/内部版本、MathType版本、操作系统及转换入口。截图公开前裁掉账号、最近文档和许可证信息。

每个独立公式原始源码占一个左对齐段落；复制代码行本身，不复制围栏。软换行可以，硬段落换行不可以。成功应同时满足可编辑对象、符号正确和位置合理。

| ID | 测试 | 检查 |
|---|---|---|
| MT01 | 单变量与正文 | 尝试Toggle TeX；若单符号不识别，再试Insert Inline Equation，两个入口分开记录 |
| MT02 | 行内分式 | 公式留在句中，正文仍为普通文字 |
| MT03 | 独立求和 | 符号正确、可编辑、位置合理 |
| MT04 | align | 两行等号对齐 |
| MT05 | aligned | 单独测试，不从MT04成功推断 |
| MT06 | cases | 大括号、分支和条件正确 |
| MT07 | array | 显式列规格、两行和增广分隔线正确 |
| MT08 | 百分号 | 转义百分号和数值保持 |
| MT09 | 编号和引用 | 转换两式、插入编号与引用，在前面新增一式并刷新，检查是否同步 |
| MT10 | 右移对照 | 同一式分别置于左对齐和居中源码段落，转换后截图比较；右移时改回左对齐重试 |

MT01：

```text
$a$ 是参数，$n$ 个样本。
```

MT02：

```text
比值为 $\frac{a+b}{c}$，其中 $c$ 非零。
```

MT03：

```text
\[ \sum_{i=1}^{n} i^2 = \frac{n(n+1)(2n+1)}{6} \]
```

MT04：

```text
\[ \begin{align} a &= b+c \\ &= d+e \end{align} \]
```

MT05：

```text
\[ \begin{aligned} a &= b+c \\ &= d+e \end{aligned} \]
```

MT06：

```text
\[ f(x)=\begin{cases} x^2 & x\geq 0 \\ -x & x<0 \end{cases} \]
```

MT07：

```text
\[ \left[\begin{array}{cc|c}1&2&3\\4&5&6\end{array}\right] \]
```

MT08：

```text
\[ p=12.5\% \]
```

MT09、MT10可使用：

```text
\[ E=mc^2 \]
```

编号使用MathType Insert Number / Insert Reference，不把静态编号或 `\tag` 放进公式体。可尝试“转换后End→Tab→Insert Number”，但需确认当前制表位把编号放在右边；失败时记录具体表现。

## 定界符附加试验

分别在Toggle TeX和Convert Equations中测试 `$$E=mc^2$$`，记成两个不同用例。一个入口成功不代表另一个支持。默认输出仍使用文档规定的行内美元与独立方括号定界符。

## 记录格式

长期使用经验可以先登记，不需要重新跑测试或附截图：

```json
{
  "status": "author_usage",
  "word_version": "Word 2016（16.0.20527.20088）",
  "mathtype_version": "7.8.2.441"
}
```

这类记录支持“作者在该版本组合下长期使用”的表述；需要声称某个具体测试通过时，另用下面的pass记录。

在 [native-tests.json](native-tests.json) 的 `tests` 数组填写结果。通过记录需要真实版本和可核对截图，例如：

```json
{
  "id": "MT04",
  "status": "pass",
  "word_version": "填写实际版本和内部版本号",
  "mathtype_version": "填写实际版本号",
  "os": "填写系统版本",
  "entrypoint": "Toggle TeX",
  "tested_at": "YYYY-MM-DD",
  "artifact": "evidence/mt04.png",
  "notes": "符号、对齐、可编辑性及保存重开结果"
}
```

上面的pass项只是字段格式，不是实测结果。未跑的具体用例可填 `not_run`；失败用 `fail` 并记错误，author_usage可与这些用例并存。证据文件放在本Skill目录内，发布前去除个人信息。
