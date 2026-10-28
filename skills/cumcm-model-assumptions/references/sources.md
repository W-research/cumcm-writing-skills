# 来源与采纳边界

## 作者整理的材料：案例来源与实际采纳

主要材料来自作者整理的“模型假设”说明、六类常见情形、合理性与过强假设讨论，以及 2020 年 A—E 题论文摘录。以下编号保留为作者整理的材料定位，不代表已独立查阅完整论文或核验其获奖等级。没有把摘录自动认定为正确范式。

| 作者整理的材料定位 | 采纳的写作方法 | 修正/限制 | 对应文件 |
|---|---|---|---|
| 严格确切、模型必需、应有合理性 | 精确陈述、模型落点与证据状态 | 不强制每条做统计检验，不靠“方便”证明合理 | selection-and-scope.md；evidence-and-validation.md |
| 六类常见情形 | 作为候选来源分类 | 非六项必填清单；小概率不等于可忽略；模型名称不决定全部前提 | selection-and-scope.md；model-prerequisites.md |
| A195 | 稳定外场、运动反馈、结构理想化、无内源 | 明确有限厚度/一维解释；辐射取舍需条件 | examples-heat.md |
| A212 | 区段参数、温区边界、注意误差来源 | 不采纳全部误差为零；区分环境稳态与元件非稳态 | examples-heat.md |
| B108 | 分清确定/随机天气、策略生成、玩家目标 | 固定概率不等于独立；共性是启发；理性不推出非合作；失败规则按题设 | examples-decision.md |
| C109 | 指标范围与利率—流失关系 | 不倒置响应与决策；不删题设约束；合并重叠表述 | examples-decision.md |
| C305 | 组内共享参数、参数有效期、风险口径 | 独立不等于无风险；最大个体风险是指标设计；不虚构分组统计；后问保留冲击 | examples-decision.md |
| D011 | 几何表示与观测过程分开 | 不照抄无误差、无干扰保证 | examples-measurement.md |
| D027 | 连接条件、坐标与探针方向 | 相切/水平需出处或近似边界，方向不取消探针接触补偿 | examples-measurement.md |
| E029 | 正常运行、记录与覆盖 | 数据质量和数据完整性可能不同，不机械合并也不空泛重复 | examples-measurement.md |
| E040 | 分层计量、正常工况去重 | 不借用仪器类型及 2%—5% 精度；不取消漏损研究 | examples-measurement.md |
| 合理性与过强假设两问 | 数据、资料、评价改进的关联 | 检验未拒绝不等于证明；文末改进不能补救删掉核心任务 | evidence-and-validation.md |

作者整理的 2024 年国赛 A 题“板凳龙”及几何建模分析，用于 writing-and-review.md 的原创迁移示例，未作为任何获奖论文的引文。该示例是方案级文字，无独立实测验证或求解结果。

## 来源状态

历史 A195–E040 片段及板凳龙原题/方案原件未随包提供，编号只是作者资料的索引，不表示当前用户给过这些材料。普通任务依据当前题目与数据即可；历史资料归属的复核由维护者补充原始出处。技术来源支持方法命题，不证明某个具体数据集满足前提。

**S-H01**：[可复做水量平衡检查](worked-example.md)，包含原创合成输入、计算定义、正常/反例及假设回写，演示有限支持而非真实水库实验。真实题面任务覆盖见 [官网2020 C假设示例](official-credit-assumptions.md)，方案与结果状态分别标注。

长资料定位：MIT 14.382讲义第3.1节；MIT 14.385 Lecture 6的PDF第6页；Markov Property的PDF第2–3页；Poisson Processes第2.2节。定位帮助复核，不代表相关应用均已验证。

## 技术修正的一手资料

以下资料分别支持所列数学或方法命题。案例取舍是作者结合资料作出的建模与写作判断，外部资料按原来源权利使用，本Skill自有内容许可见 [MIT](../LICENSE)。

| 来源 | 支持范围 |
|---|---|
| [NIST/SEMATECH：Check of assumptions](https://www.itl.nist.gov/div898/handbook/pri/section2/pri245.htm) | 残差诊断与假设检查 |
| [MIT：14.382 Notes from 14.381](https://ocw.mit.edu/courses/14-382-econometrics-spring-2017/29d3e55c546c9927eff0035735b35aa9_MIT14_382S17_14381notes.pdf) | 不施加正态性的 Gauss–Markov 模型 |
| [MIT：14.385 Lecture 6](https://ocw.mit.edu/courses/14-385-nonlinear-econometric-analysis-fall-2007/d6bfdd254deebcaeae7a3470eac8953c_lecture06.pdf) | 正态模型中的有限样本推断 |
| [Penn State：Binary Logistic Regression](https://online.stat.psu.edu/stat504/Lesson06) | Logistic 回归的响应结构不要求正态误差 |
| [MIT：Markov Property](https://ocw.mit.edu/courses/res-6-012-introduction-to-probability-spring-2018/f02929e77a4e43c43c97fcd78d114674_hsQnmrHbbms.pdf) | 条件于当前状态的历史无关与状态选取 |
| [MIT：Poisson Processes](https://ocw.mit.edu/courses/6-262-discrete-stochastic-processes-spring-2011/3a19ce0e02d0008877351bfa24f3716a_MIT6_262S11_chap02.pdf) | Poisson 到达过程、独立增量及指数间隔 |
| [NIST：Exponential Distribution](https://www.itl.nist.gov/div898/handbook/eda/section3/eda3667.htm) | 指数分布的恒定风险率 |
| [NIST：Poisson Distribution](https://www.itl.nist.gov/div898/handbook/eda/section3/eda366j.htm) | Poisson 计数分布及矩特征 |
| [SciPy：goodness_of_fit](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.goodness_of_fit.html) | 参数估计后的拟合优度校准，限其支持的连续分布 |
| [COMSOL：Modeling Heat Transfer by Radiation](https://doc.comsol.com/6.4/doc/com.comsol.help.heat/heat_ug_modeling.06.55.html) | 辐射相对贡献依赖温度、发射率等条件 |
| [BIPM：VIM 2.26](https://jcgm.bipm.org/vim/en/2.26.html) | 测量不确定度的含义，与零误差不同 |

资料使用时在相应论断附近引用；不把本表全部粘贴进任意国赛论文。用户未要求文献综述时不扩写综述，也不捏造比赛官方推荐或获奖占比。

## 扩充案例的方式

新增案例至少保留“来源定位、任务/模型背景、可取之处、适用风险、原创改写、证据或验证方向、不可直接迁移的条件”。能改变写作决策的少量案例优于大量未经辨析的摘抄。

只根据摘录时说明未见全文；只有查阅可核验的原文后才能增加精确页码、文献归属或获奖信息。保留专有术语，改写论证组织，避免拼接示例句子冒充当前题目的原创正文。
