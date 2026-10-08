# HW02：理解数据——UCI 四中心心脏病数据审查

## 作业目标

本次作业使用指定的 UCI Heart Disease 四中心历史数据，练习判断：

- 一行数据代表什么，一列数据扮演什么角色；
- 连续、计数、二分类、多分类和有序变量应如何区分；
- 缺失、可疑零值、中心差异和类别不平衡会怎样影响结论；
- 删除、编码和标准化等处理会不会改变研究对象；
- 现有数据能够支持哪些结论，不能支持哪些结论。

本作业仅用于教学和研究准备，不能据此给出临床建议、因果结论或部署承诺。

## 作业材料

材料均在 [`assignments/hw02/resources`](resources) 中：

- `HW02-学生工作单.docx`：必须完成的 Q1–Q6 工作单；
- `assets/pbl-understanding-data/`：四中心数据及配套证据表、图片；
- `notebook/pbl-understanding-data-lab.ipynb`：可选的复核 Notebook，不会编程也可以完成核心任务。

数据来源：UCI Heart Disease，DOI `10.24432/C52P4X`，许可 `CC BY 4.0`。

## 课堂课件

- [`chap2_data.pptx`](lecture/chap2_data.pptx)：第二讲“理解数据”课堂课件，供课后复习使用。
- [`data.md`](lecture/data.md)：第二讲文字讲义，包含变量类型、数据质量、相似性、抽样和预处理等内容。

课件和文字讲义覆盖的内容多于本次作业要求。`data.md` 第七节保留的是早期拓展作业设计；当前 HW02 的必做范围仍以本页说明和学生工作单中的 Q1–Q6 为准。

## 需要完成的内容

### 1. 完成工作单

下载 `HW02-学生工作单.docx`，按照材料顺序完成 Q1–Q6、总答案追踪表和来源证据卡。不得删除题目、证据编号或自己的判断过程。

### 2. 完成数据使用建议书

根据工作单第 0–6 行的判断，在自己的 `README.md` 中提交一份 **300–450 字**的数据使用建议书，必须包含：

1. 最终选择 A、B、C 或 D，并说明可以描述的对象；
2. 至少引用变量类型、分析方法、数据质量和处理后果四类证据；
3. 指出当前数据不能回答的一项新问题；
4. 写出继续使用数据前需要核查的内容；
5. 写出至少一个具体、可判断的停止条件。

不能只写“先清洗再建模”，必须写清楚具体操作及理由。

### 3. 完成来源证据卡

在 `README.md` 中记录一条来自 AI、教材或网页的具体说法，并填写：

- 来源和访问日期；
- 原始说法；
- 使用表 A2–D3 中哪项证据进行核查；
- 适用条件；
- 核查后的修正说法。

使用 AI 时可以保留 AI 的原始说法，但必须自行核查，不能把 AI 输出直接当作证据。

## 提交文件

每位同学在 `submissions/hw02` 下新建自己的文件夹：

```text
submissions/hw02/学号-姓名/
├── README.md
└── 学号-姓名-工作单.docx
```

`README.md` 请复制 [`TEMPLATE.md`](TEMPLATE.md) 后填写。除上述文件外，如确有需要，可在自己的文件夹内增加图片；不要上传其他数据集、压缩包、软件环境或个人敏感信息。

## Git 提交流程

```bash
git switch main
git pull origin main
git switch -c hw02/学号-姓名

mkdir -p submissions/hw02/学号-姓名
cp assignments/hw02/TEMPLATE.md submissions/hw02/学号-姓名/README.md
cp assignments/hw02/resources/HW02-学生工作单.docx submissions/hw02/学号-姓名/学号-姓名-工作单.docx
```

完成作业后，只提交自己的文件夹：

```bash
git status
git add submissions/hw02/学号-姓名/
git commit -m "提交姓名的 HW02 数据作业"
git push -u origin hw02/学号-姓名
```

然后在 GitHub 创建 Pull Request：

- base 分支：`main`
- compare 分支：`hw02/学号-姓名`
- 标题：`HW02 数据理解 - 学号 - 姓名`
- 一个同学只创建一个 HW02 Pull Request；后续修改继续 Push 到同一分支即可。

## 提交检查

- [ ] 分支从最新的 `main` 创建；
- [ ] 只修改自己的 `submissions/hw02/学号-姓名/`；
- [ ] 工作单中的 Q1–Q6、追踪表和来源证据卡已经完成；
- [ ] `README.md` 中的建议书为 300–450 字；
- [ ] 建议书包含证据、边界、继续核查项和停止条件；
- [ ] Pull Request 的目标分支为 `main`；
- [ ] 未提交密码、令牌、手机号等敏感信息。

## 截止时间

以课程群内通知为准。
