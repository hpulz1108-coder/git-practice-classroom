# HW03：高维数据与维度灾难

## 作业目标

本次作业使用 Golub 白血病基因表达数据，比较不同探针数量下的距离分布、近远邻关系、训练表现、测试表现和特征选择稳定性。核心问题是：

> 在样本数远小于特征数时，保留更多特征是否一定能得到更可靠的模型？

需要依据实验结果回答，不能预先把全部新增特征都认定为噪声，也不能根据一次测试结果断言“越多越好”。

## 作业材料

- [`resources/HW03-学生工作单.md`](resources/HW03-学生工作单.md)：T1–T5和H1；
- [`resources/notebook/high-dimension-lab.ipynb`](resources/notebook/high-dimension-lab.ipynb)：距离、泛化和筛选稳定性实验；
- [`resources/data`](resources/data)：72份样本、7129个探针的白血病表达数据及说明；
- [`resources/scripts/experiments.py`](resources/scripts/experiments.py)：Notebook调用的实验代码；
- [`resources/requirements.txt`](resources/requirements.txt)：建议环境；
- [`lecture/High-dimension.md`](lecture/High-dimension.md)：第三讲文字讲义；
- [`lecture/high-dimension-pbl-questions-v2.pptx`](lecture/high-dimension-pbl-questions-v2.pptx)：课堂提问课件。

数据来源与许可见 [`resources/data/README.md`](resources/data/README.md)。本作业使用处理后的教学数据，不支持因果、临床有效性或部署结论。

## 需要完成的内容

### 1. 完成学生工作单

完成T1–T5以及H1。H1为600–900字，不需要再提交内容重复的独立报告。回答应包含实际实验数值、推理和适用边界。

### 2. 运行Notebook

按从上到下的顺序运行Notebook并保留输出。先写预测，再运行对应实验。不要根据测试集表现反复挑选特征数。

建议在独立环境中运行：

```bash
python3 -m venv .venv-hw03
source .venv-hw03/bin/activate
python -m pip install -r assignments/hw03/resources/requirements.txt
cd assignments/hw03/resources
jupyter notebook notebook/high-dimension-lab.ipynb
```

Windows PowerShell激活环境可使用：

```powershell
.venv-hw03\Scripts\Activate.ps1
```

Notebook运行完成后保存，再复制到自己的提交目录。`student-results`为运行过程文件，不需要提交。

### 3. 完成README

复制 [`TEMPLATE.md`](TEMPLATE.md)，填写身份信息、最终结论、关键证据、运行环境和AI使用说明。

## 提交文件

每位同学只在自己的目录中提交三个文件：

```text
submissions/hw03/学号-姓名/
├── README.md
├── 学号-姓名-工作单.md
└── 学号-姓名-high-dimension-lab.ipynb
```

创建提交目录并复制模板：

```bash
mkdir -p submissions/hw03/学号-姓名
cp assignments/hw03/TEMPLATE.md submissions/hw03/学号-姓名/README.md
cp assignments/hw03/resources/HW03-学生工作单.md submissions/hw03/学号-姓名/学号-姓名-工作单.md
```

运行并保存Notebook后复制：

```bash
cp assignments/hw03/resources/notebook/high-dimension-lab.ipynb \
  submissions/hw03/学号-姓名/学号-姓名-high-dimension-lab.ipynb
```

不要提交数据副本、`student-results`、虚拟环境、压缩包、缓存文件或个人敏感信息。

## Git提交流程

无论HW02是否完成，HW03都从最新的`main`建立独立分支：

```bash
git switch main
git pull origin main
git switch -c hw03/学号-姓名
```

只提交自己的HW03目录：

```bash
git status
git add submissions/hw03/学号-姓名/
git commit -m "提交姓名的 HW03 高维数据作业"
git push -u origin hw03/学号-姓名
```

然后在GitHub创建Pull Request：

- base分支：`main`
- compare分支：`hw03/学号-姓名`
- 标题：`HW03 高维数据 - 学号 - 姓名`

一个同学只创建一个HW03 Pull Request。后续修改继续Push到同一分支。

## 与HW02的关系

HW02补交通道保持开放，尚未完成HW02的同学也可以正常开始HW03。

- HW02继续使用`hw02/学号-姓名`分支和原HW02 Pull Request；
- HW03必须从最新`main`新建`hw03/学号-姓名`分支；
- 不要从HW02分支创建HW03分支；
- 不要把HW02和HW03放进同一个Pull Request。

## 提交检查

- [ ] HW03分支从最新`main`创建；
- [ ] 只修改自己的`submissions/hw03/学号-姓名/`；
- [ ] T1–T5和H1已完成；
- [ ] 工作单引用了实际实验数值；
- [ ] Notebook已从头运行并保留输出；
- [ ] README记录了环境、随机种子、代码改动和AI核查；
- [ ] Pull Request目标分支为`main`；
- [ ] 未提交数据副本、虚拟环境或敏感信息。

## 截止时间

以课程群内通知为准。
