# HW04：降维、PCA 与 UMAP

## 作业目标

本次作业使用 Golub 白血病微阵列表达数据，练习把高维表达矩阵压缩到低维空间，并判断一张“分开的图”究竟能支持什么结论。核心问题是：

> 二维图上的分离，是否足以证明疾病机制，或预测新患者？

完成后，你应能：

- 区分可视化、压缩、去噪、结构探索和建模输入这几种降维目的；
- 解释标准化、PCA 的 explained variance 和 loading；
- 通过 UMAP 参数/随机种子对照，判断局部结构的稳定程度；
- 说明描述性降维与预测建模在拟合范围上的区别，识别信息泄露；
- 用“主张—证据—推理—边界”写出有证据约束的结论。

## 作业材料

- [`lecture/Dimension-reduction.md`](lecture/Dimension-reduction.md)：讲解稿与课堂代码；
- [`resources/HW04-学生工作单.md`](resources/HW04-学生工作单.md)：四项任务与提交要求；
- [`resources/slides/dimension-reduction-pbl.pptx`](resources/slides/dimension-reduction-pbl.pptx)：课堂课件；
- [`resources/data/README.md`](resources/data/README.md)：数据来源、字段和解释边界；
- [`resources/data/leukemia/leukemia.csv`](resources/data/leukemia/leukemia.csv)：72 个样本、7,129 个探针的课堂数据；
- [`TEMPLATE.md`](TEMPLATE.md)：提交目录中的 README 模板；
- [`resources/requirements.txt`](resources/requirements.txt)：建议 Python 环境。

本次公开材料不包含教师参考答案、教师分析脚本和答案插图。请先阅读数据说明，再开始实验。

## 需要完成的内容

1. **任务 1：目的与拟合范围**
   - 比较可视化、去噪、压缩、结构探索和建模输入的评价方式；
   - 画出“描述性降维”和“预测新样本”的两条流程；
   - 用自己的话解释为什么全数据先标准化/PCA 再交叉验证会泄露信息。

2. **任务 2：PCA 对照**
   - 对全部 72 个样本按探针标准化，报告 PC1、PC2 的解释率及累计解释率曲线；
   - 绘制 PC1–PC2 图，列出 PC1 绝对权重最大的 5 个探针及带符号权重；
   - 做一次“仅中心化、不标准化”的原尺度 PCA，对比解释率和高权重探针；
   - 解释 PCA 结果的含义与不能推出的结论。

3. **任务 3：UMAP 稳定性**
   - 使用基线参数 `n_neighbors=15`、`min_dist=0.1`、`metric='euclidean'`、`random_state=42`、`n_jobs=1`；
   - 只改一个因素，分别比较 `n_neighbors=5`、`min_dist=0.5`、`random_state=7`；
   - 并排比较 PCA 与 UMAP，记录样本编号与坐标对应关系；
   - 说明哪些关系相对稳定，以及岛屿、距离、方向和分离不能直接代表什么。

4. **任务 4：证据边界结论**
   - 用四句话回应“图上分得开，就证明发现了疾病机制，并可以预测新患者”；
   - 至少引用一项 PCA 数值或 loading，以及一项 UMAP 参数对照；
   - 提出一项能把探索性图形结论升级为生物医学结论的后续验证。

## 运行建议

建议在独立环境中运行：

```bash
python3 -m venv .venv-hw04
source .venv-hw04/bin/activate
python -m pip install -r assignments/hw04/resources/requirements.txt
```

Windows PowerShell：

```powershell
.venv-hw04\Scripts\Activate.ps1
```

数据读取示例：

```python
import pandas as pd

df = pd.read_csv("assignments/hw04/resources/data/leukemia/leukemia.csv")
X = df.drop(columns=["sample_id", "original_split", "diagnosis"])
y = df["diagnosis"]
```

描述性 PCA/UMAP 可以在全部 72 个样本上拟合，但诊断标签只能在拟合后用于着色。若做预测交叉验证，标准化、PCA 和分类器必须一起放进每个训练折的 Pipeline。

## 提交文件

每位同学只在自己的目录中提交：

```text
submissions/hw04/学号-姓名/
├── README.md
├── 学号-姓名-工作单.md
└── 学号-姓名-分析.ipynb      # 或等价的 PDF/Markdown 分析报告
```

README 可复制 [`TEMPLATE.md`](TEMPLATE.md)。分析文件必须保留代码、实际输出和图，不能只提交截图或最终结论。报告中请记录：Python/软件包版本、随机种子、输入特征、标准化方式、拟合范围以及 AI 使用和核查情况。

不要提交数据副本、虚拟环境、缓存、压缩包、Office 临时文件或任何个人敏感信息。

## Git 提交流程

无论 HW02、HW03 是否完成，HW04 都从最新 `main` 建立新分支：

```bash
git switch main
git pull origin main
git switch -c hw04/学号-姓名
```

只提交自己的 HW04 目录：

```bash
git add submissions/hw04/学号-姓名/
git commit -m "提交姓名的 HW04 降维作业"
git push -u origin hw04/学号-姓名
```

然后创建 Pull Request：

- base：`main`；
- compare：自己的 `hw04/学号-姓名`；
- 标题：`HW04 降维 - 学号 - 姓名`。

一个同学只创建一个 HW04 Pull Request；需要修改时继续在同一分支提交并 Push，原 Pull Request 会自动更新。HW02/HW03 的补交继续使用各自的分支和 Pull Request，不要混在 HW04 中。

## 提交前自查

- [ ] 工作单四项任务已完成；
- [ ] PCA 与 UMAP 的参数、种子和实际结果已记录；
- [ ] 已区分描述性图形与预测性能；
- [ ] 已说明标准化/PCA 的拟合范围，避免信息泄露；
- [ ] 报告保留代码、输出和图；
- [ ] 只修改自己的 `submissions/hw04/学号-姓名/`；
- [ ] Pull Request 目标分支为 `main`。

截止时间以课程群通知为准。
