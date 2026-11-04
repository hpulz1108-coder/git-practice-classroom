# 第 4 讲：降维、PCA 与 UMAP

> 主题负责人：zhang。原课程安排“第 3 讲b”，现独立授课。

## 一、课程定位

- **主题**：如何把复杂高维数据压缩到可理解的低维空间？
- **先备知识**：样本、特征、均值与方差；第 3 讲的高维数据背景。
- **建议时长**：课堂 45 分钟，课后实验与报告 60–90 分钟。
- **实验数据**：Golub 白血病微阵列表达，72 个样本、7,129 个探针，ALL 47、AML 25。

本讲聚焦降维方法和证据解释，高维距离与过拟合实验已由第 3 讲承担。

## 二、驱动问题与核心问题

团队将白血病表达数据画成二维图，认为：“图上分离的簇证明发现了疾病机制，而且可以预测新患者。”你会要求哪些证据，才接受这个结论？

1. 降维是为了可视化，还是为了建模？
2. PCA 和 UMAP 有什么区别？
3. 如何避免过度解释降维图？

## 三、学习目标

1. 区分可视化、去噪、特征压缩、结构探索和建模输入五种目的。
2. 完成按列标准化，解释 PCA 对尺度的敏感性。
3. 解释主成分、explained variance 和 loading，绘制标注解释率的 PC1–PC2 图。
4. 对同一输入运行 UMAP，比较参数或种子改变后的局部结构。
5. 区分二维图、生物学解释与新样本预测证据。
6. 将标准化与 PCA 放入训练折内，识别信息泄露。

## 四、降维要解决什么问题

降维将原始特征映射为更少的坐标。一个主成分通常组合许多特征，不能把它理解为直接挑选一个基因。

| 目的 | 输出 | 如何评价 |
|---|---|---|
| 可视化 | 二维或三维坐标 | 可读性、参数稳定性与解释边界 |
| 去噪 | 减少不稳定变化的表示 | 重复测量或下游验证，不是仅看图更整齐 |
| 压缩特征 | 较少坐标、近似重建 | 维数、重建误差、解释率与计算成本 |
| 发现样本结构 | 候选分组、梯度与邻域 | 稳定性、外部信息与独立数据验证 |
| 后续建模输入 | 可一致变换新样本的特征 | 无泄露的交叉验证与独立测试表现 |

用于建模与用于看图可以使用同一算法，但拟合范围和评价问题不同。丢弃部分方向可能去噪，也可能丢掉弱但重要的预测信号。

## 五、PCA：寻找方差最大的线性方向

### 5.1 标准化与中心化

PCA 通常先中心化。z-score 为 `z_ij=(x_ij−μ_j)/s_j`，让各列以自身变异尺度计量。`StandardScaler` 使用总体标准差（ddof=0）；常量列需另外检查，本数据没有常量探针。

仅中心化不会消除尺度差异。数值尺度大或变异大的特征可能主导原尺度 PCA；标准化后各列方差接近 1，更强调相关变化。但标准化也可能放大低变异噪声。因此应解释选择理由，并保留原尺度对照，不能只比较谁的解释率更高。

本数据含负值，不是 RNA-seq 原始计数，不直接取 log 或 log1p。此处标准化不替代微阵列上游归一化和批次处理。

### 5.2 主成分与 explained variance

对中心化输入 Z，第一主成分方向 w₁ 在单位长度约束下，使投影 `t₁=Z w₁` 的方差最大。PC2 与 PC1 正交，解释该约束下最多的剩余方差，之后依次类推。

`explained_variance_ratio_[k]` 是第 k 个主成分的方差占当前输入总方差的比例，累计解释率是各项之和。它不是诊断准确率或生物学真相的比例。PCA 不使用诊断标签，最大方差方向不一定最能区分 ALL 与 AML。

样本得分是投影后的坐标。中心化后，72 个样本至多有 71 个非零主成分，即使原始输入有 7,129 列。

### 5.3 loading 表示什么

本课将 `pca.components_.T` 定义为方向权重（loading）。PC1 得分由全部输入加权求和：`PC1_i=Σ_j w_j z_ij`。其他软件可能使用乘以主成分标准差后的 loading 或变量与主成分的相关系数，须注明定义。

绝对权重大说明该特征在该方向上的系数大，不等于差异表达显著、分类重要或致病。整体同时翻转权重和样本得分的符号，只改变轴朝向，不改变解释率。

## 六、UMAP：展示非线性局部结构

UMAP 从高维近邻关系构建图，并优化低维嵌入，侧重保持局部邻域。它常用于单细胞和复杂表型的探索性展示，帮助观察两条线性方向难以充分表达的局部关系。

- `n_neighbors` 控制构建邻域时考虑的邻居数量；较小值更强调较小尺度的结构。
- `min_dist` 影响低维点可以堆得多紧，不是生物学样本间的真实距离阈值。
- 距离度量、预处理和随机种子也影响结果，必须记录。

UMAP1/UMAP2 是嵌入坐标，不是基因或疾病轴，没有与 PCA 等价的 explained variance。邻近可提示局部相似，但不是所有近邻都被保留；岛屿间距离、面积、朝向和点密度不能直接量化生物学差异。看见簇只能提出假设，不能确认真实亚型或机制。

## 七、PCA 与 UMAP 如何选

| 比较 | PCA | UMAP |
|---|---|---|
| 映射 | 线性投影 | 非线性嵌入 |
| 主要保留信息 | 方差最大的正交方向 | 局部邻域结构 |
| 可解释性 | 权重、坐标与解释率可追踪 | 轴无固定生物学含义 |
| 常见用途 | 压缩、探索、建模输入 | 复杂结构的探索性可视化 |
| 关键限制 | 大方差不一定是预测信号 | 簇间距离与簇数容易被过度解读 |
| 新样本使用 | 训练数据拟合后 transform | 支持 transform 的实现也须在训练数据拟合 |

二者均不能凭二维图证明临床泛化或因果关系。UMAP 图更分簇，不自动意味着优于 PCA。

## 八、课堂练习：同一数据，两个视角

按 [学生工作单](../resources/HW04-学生工作单.md) 四项任务开展。先预测再运行。以下代码在本章目录执行；所需依赖见 `../resources/requirements.txt`。

### 8.1 标准化与 PCA

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from umap import UMAP

df = pd.read_csv('resources/data/leukemia/leukemia.csv')
X = df.drop(columns=['sample_id', 'original_split', 'diagnosis'])
assert X.shape == (72, 7129) and np.isfinite(X.to_numpy()).all()
Z = StandardScaler().fit_transform(X)  # 此处只描述全部72个样本
print('标准化检查：', np.abs(Z.mean(axis=0)).max(),
      np.abs(Z.std(axis=0, ddof=0)-1).max())
pca = PCA(svd_solver='full').fit(Z)
scores = pca.transform(Z)
evr = pca.explained_variance_ratio_
print('PC1、PC2解释率及合计：', evr[:2], evr[:2].sum())
weights = pd.Series(pca.components_[0], index=X.columns)
print(weights.loc[weights.abs().nlargest(5).index])
```

讨论：PC1 是否等于最能区分疾病的方向？前两轴能否代表全部数据？选一个 loading 说明其含义和边界。

### 8.2 UMAP 与并排比较

```python
embedding = UMAP(n_components=2, n_neighbors=15, min_dist=0.1,
                 metric='euclidean', random_state=42, n_jobs=1).fit_transform(Z)
fig, axes = plt.subplots(1, 2, figsize=(10, 4))
for label, color in [('ALL', '#387ca3'), ('AML', '#d57839')]:
    mask = df.diagnosis.eq(label).to_numpy()
    axes[0].scatter(scores[mask, 0], scores[mask, 1], label=label, c=color)
    axes[1].scatter(embedding[mask, 0], embedding[mask, 1], label=label, c=color)
axes[0].set(xlabel=f'PC1 ({evr[0]:.1%})', ylabel=f'PC2 ({evr[1]:.1%})', title='PCA')
axes[1].set(xlabel='UMAP1', ylabel='UMAP2', title='UMAP')
for ax in axes:
    ax.legend()
plt.tight_layout()
plt.show()
```

诊断只用于事后着色。课后完成原尺度 PCA、累计解释率图及三个 UMAP 单因素对照：只改邻居数为 5、只改 min_dist 为 0.5、只改种子为 7。保留全部结果与样本编号，不挑最漂亮的一张。

讨论：两种方法展示的结构有何异同？哪些邻近关系稳定？缺少批次字段时为什么不能宣称已排除批次效应？

## 九、三种常见错误

| 错误判断 | 修正方式 |
|---|---|
| UMAP 有几个岛屿，就有几个真实亚型 | 保留参数对照，明确聚类定义，再用独立信息和数据验证 |
| PCA 不用标签，可全数据降维后交叉验证 | 验证样本仍影响均值、尺度和协方差；完整 Pipeline 必须折内拟合 |
| 不检查尺度，直接使用原值做 PCA | 说明单位与方差，比较标准化和原尺度，并解释代价 |

正确预测流程：先划分 → 每个训练折拟合标准化、PCA 和分类器 → 用已有变换处理验证折 → 固定方案后评估未参与选择的测试数据。

本讲可选实验仅在原始 38 个训练样本内，用同一分层三折比较 `StandardScaler → 1近邻` 与 `StandardScaler → PCA(10) → 1近邻`，不重新查看原始测试成绩选参数。如果此前用全部 72 行探索并据此调整方案，这些样本也不能重新当作完全未见的确认性测试证据。

## 十、退出卡与作业

退出卡：用“主张—证据—推理—边界”四句话回答驱动问题，引用一项 PCA 结果与一项 UMAP 对照，并提出下一步验证。

课后用自己的话解释：

1. PCA 第一主成分代表什么？结合本次解释率与一个探针权重回答。
2. 为什么 PCA 前通常需要标准化？结合原尺度对照，说明作用与代价。
3. UMAP 图能说明什么，不能说明什么？结合一次参数或种子对照回答。

评价关注拟合范围、可复现对照和解释边界，不以图是否漂亮或分组是否清楚评分。请以自己实际运行得到的结果为准，不要只抄写示例结论。

## 十一、参考资料

- 数据与原研究：[本地来源记录](../resources/data/README.md)。
- PCA：[scikit-learn 用户指南](https://scikit-learn.org/stable/modules/decomposition.html#pca)。
- UMAP：[基本使用](https://umap-learn.readthedocs.io/en/latest/basic_usage.html)、[参数说明](https://umap-learn.readthedocs.io/en/latest/parameters.html)。
- 信息泄露：[scikit-learn 常见陷阱](https://scikit-learn.org/stable/common_pitfalls.html#data-leakage)。
