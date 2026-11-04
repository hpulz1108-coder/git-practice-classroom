# 数据说明：Golub 白血病基因表达数据

第 4 讲“降维、PCA 与 UMAP”使用这组数据；它与第 3 讲沿用同一来源，已于 2026-09-25 下载并检查。

## 来源与引用

- 数据版本：OpenML `leukemia`，dataset ID 1104，version 1。
- 数据页面：<https://www.openml.org/d/1104>。
- 元数据：<https://www.openml.org/api/v1/json/data/1104>。
- 原始下载：<https://openml.org/data/v1/download/53987/leukemia.arff>。
- 原研究：Golub et al. (1999), *Molecular Classification of Cancer: Class Discovery and Class Prediction by Gene Expression Monitoring*, Science 286, 531–537，<https://doi.org/10.1126/science.286.5439.531>。研究归属依据下载文件和 OpenML 说明，未独立核验原论文全文。
- OpenML 元数据的 `licence` 为 `Public`；该字段不等于一份明确的 CC 授权条款。保留来源和引用，不将其改写为 CC BY 或 public domain。

## 文件与读取

| 文件 | 用途 |
|---|---|
| `leukemia/source/leukemia.arff` | 下载的原始文件，字节未修改 |
| `leukemia/source/openml-metadata.json` | 来源元数据快照 |
| `leukemia/leukemia.csv` | 带表头的本讲课堂数据 |
| `inspection.json` | 检查结果、派生规则及 SHA-256 |

在本单元目录运行 Python 时：

```python
import pandas as pd

df = pd.read_csv('data/leukemia/leukemia.csv')
X = df.drop(columns=['sample_id', 'original_split', 'diagnosis'])
y = df['diagnosis']
train = df['original_split'].eq('train')
```

原始 ARFF 的类别声明包含空格，部分读取器会报类别不匹配；课堂 CSV 已将类别两端空格去除。CSV 保留全部行、全部特征、原始数值及顺序；只增加教学行号与原始划分标记，并将 `CLASS` 改名为 `diagnosis`。

## 观测单位与字段

每行是一份白血病样本的微阵列表达谱，每个数值列是一个探针特征。**7,129 个探针特征不等于 7,129 个不同基因**，其中包含 `AFFX` 控制探针。课堂保留全部探针用于方法教学，不能直接把高 loading 探针称为致病基因。

| 字段 | 含义与使用边界 |
|---|---|
| `sample_id` | G001–G072，按源行序生成的教学编号，不是原始患者 ID |
| `original_split` | 按源说明标记：前 38 行 train，其余 34 行 test |
| `diagnosis` | ALL：急性淋巴细胞白血病；AML：急性髓系白血病 |
| 其余 7,129 列 | 保留原始探针名称的表达测量，唯一的模型输入列 |

来源快照没有提供可用于本课的患者重复映射、中心或批次字段。不能据此证明患者层面的独立性，也不能检验或排除批次效应。`original_split` 是源文件划分，不是新开展的外部临床验证。

## 本地实际检查

- n=72，p=7,129，p/n≈99.01，属于真实 p≫n 数据。
- 类别：ALL 47、AML 25；训练部分 ALL 27、AML 11；测试部分 ALL 20、AML 14。
- 全部输入为有限数值；常量特征 0；完全重复的特征行 0；探针列名均唯一。
- 范围 −28,400 至 71,369；负值 147,174 个，零值 1,615 个。这不是 RNA-seq 原始计数，不能直接取 log 或 log1p，也不能擅自把非正值当缺失。
- ARFF 的 MD5 为 `338f0779a7c2e0ad62f98d987b43edae`，与 OpenML 元数据一致。各文件 SHA-256 见 `inspection.json`。

## 本讲使用规则

1. 输入为全部 7,129 个探针；不按诊断筛选特征，不重复距离集中、逐维分类或标签置换实验。
2. 描述性 PCA/UMAP 使用全部 72 行，按探针做 z-score，诊断仅在拟合后着色。该图不能用于估计新患者预测性能。
3. 原尺度 PCA 仅作尺度敏感性对照；标准化不替代微阵列上游归一化，也不是对所有表达数据都最优的通用结论。
4. UMAP 基线为 n_neighbors=15、min_dist=0.1、metric=euclidean、random_state=42；分别只改邻居数为 5、min_dist 为 0.5 或种子为 7。
5. 可选建模对照只在原始 38 个 train 样本内做三折交叉验证；标准化、PCA 和分类器均在折内拟合。不使用另 34 个样本调参或报告新测试成绩。若第 3 讲已看过其测试结果，不能把它们重新称作未见过的独立测试证据。

本文件记录数据与任务约定，不包含课堂实验答案。
