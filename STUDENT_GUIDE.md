# 学生提交流程（仓库协作者模式）

下面的命令中，请把 `你的GitHub用户名`、`学号` 和 `姓名` 换成自己的信息。

## 第一步：接受仓库邀请

1. 登录 GitHub。
2. 打开 GitHub 发来的仓库协作邀请。
3. 点击 **Accept invitation**。
4. 打开教师仓库：`https://github.com/hpulz1108-coder/git-practice-classroom`。

必须先接受邀请，否则无法把分支 Push 到教师仓库。

## 第二步：Clone 到电脑

在终端中直接 Clone 教师仓库：

```bash
git clone https://github.com/hpulz1108-coder/git-practice-classroom.git
cd git-practice-classroom
```

## 第三步：创建自己的分支

```bash
git switch main
git pull origin main
git switch -c hw01/学号-姓名
```

例如：

```bash
git switch -c hw01/20260001-张三
```

可以用下面的命令确认当前分支：

```bash
git branch --show-current
```

## 第四步：创建作业文件

在 `submissions/hw01` 目录中新建：

```text
学号-姓名.md
```

按照仓库首页的示例填写姓名、学号、GitHub 用户名和学习记录。

## 第五步：检查并提交

```bash
git status
git add submissions/hw01/学号-姓名.md
git commit -m "提交姓名的 Git 练习"
```

例如：

```bash
git add submissions/hw01/20260001-张三.md
git commit -m "提交张三的 Git 练习"
```

## 第六步：Push 到仓库中的个人分支

```bash
git push -u origin hw01/学号-姓名
```

例如：

```bash
git push -u origin hw01/20260001-张三
```

## 第七步：创建 Pull Request

1. 打开教师的 GitHub 仓库。
2. 点击页面提示中的 **Compare & pull request**。
3. 确认目标分支是 `main`，来源分支是自己的 `hw01/学号-姓名`。
4. 标题填写 `Git练习 - 学号 - 姓名`。
5. 按模板填写检查项。
6. 点击 **Create pull request**。

看到 Pull Request 页面就表示提交成功。后续如需修改，继续在同一分支修改、Commit 并 Push，Pull Request 会自动更新，不需要重复创建。

## 提交下一次作业

开始 `hw02` 前，先回到 `main` 并获取教师发布的最新内容：

```bash
git switch main
git pull origin main
git switch -c hw02/学号-姓名
```

然后按照 [`assignments/hw02/README.md`](assignments/hw02/README.md) 的要求，在 `submissions/hw02/学号-姓名/` 中完成作业，Commit、Push，并创建新的 Pull Request。每次作业都应使用新的分支。

## 常用排错命令

查看文件状态：

```bash
git status
```

查看提交记录：

```bash
git log --oneline --decorate -5
```

查看远程仓库：

```bash
git remote -v
```

如果 Git 提示尚未设置姓名和邮箱，可执行：

```bash
git config --global user.name "你的姓名"
git config --global user.email "你的GitHub邮箱"
```

请勿直接复制同学的文件；遇到问题时，把 `git status` 的输出发给老师或助教。
