# 学生提交流程

下面的命令中，请把 `你的GitHub用户名`、`学号` 和 `姓名` 换成自己的信息。

## 第一步：Fork 教师仓库

1. 登录 GitHub。
2. 打开教师发出的仓库地址。
3. 点击页面右上角的 **Fork**。
4. 点击 **Create fork**。

完成后，你的 GitHub 账号下会出现一份自己的仓库副本。

## 第二步：Clone 到电脑

在终端中执行：

```bash
git clone https://github.com/你的GitHub用户名/git-practice-classroom.git
cd git-practice-classroom
```

## 第三步：创建自己的分支

```bash
git switch -c submission/学号-姓名
```

例如：

```bash
git switch -c submission/20260001-张三
```

可以用下面的命令确认当前分支：

```bash
git branch --show-current
```

## 第四步：创建作业文件

在 `submissions` 目录中新建：

```text
学号-姓名.md
```

按照仓库首页的示例填写姓名、学号、GitHub 用户名和学习记录。

## 第五步：检查并提交

```bash
git status
git add submissions/学号-姓名.md
git commit -m "提交姓名的 Git 练习"
```

例如：

```bash
git add submissions/20260001-张三.md
git commit -m "提交张三的 Git 练习"
```

## 第六步：Push 到自己的 GitHub 仓库

```bash
git push -u origin submission/学号-姓名
```

例如：

```bash
git push -u origin submission/20260001-张三
```

## 第七步：创建 Pull Request

1. 打开自己 Fork 后的 GitHub 仓库。
2. 点击页面提示中的 **Compare & pull request**。
3. 确认目标仓库是教师的 `hpulz1108-coder/git-practice-classroom`，目标分支是 `main`。
4. 标题填写 `Git练习 - 学号 - 姓名`。
5. 按模板填写检查项。
6. 点击 **Create pull request**。

看到 Pull Request 页面就表示提交成功。后续如需修改，继续在同一分支修改、Commit 并 Push，Pull Request 会自动更新，不需要重复创建。

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

