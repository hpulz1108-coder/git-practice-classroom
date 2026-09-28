# Git 练习课堂

这是全班共用的 Git 练习仓库。本次练习的目标是完成一次标准的开源协作流程：

> Fork 仓库 → Clone 到本地 → 创建分支 → 修改文件 → Commit → Push → 发起 Pull Request

请不要直接修改其他同学的文件，也不要在仓库中上传密码、令牌、身份证号、手机号等敏感信息。

## 本次作业

在 `submissions` 目录中新建一份 Markdown 文件，文件名格式为：

```text
学号-姓名.md
```

例如：

```text
submissions/20260001-张三.md
```

文件内容可参考下面的格式：

```markdown
# Git 练习提交

- 姓名：张三
- 学号：20260001
- GitHub 用户名：zhangsan

## 我完成的操作

- [x] Fork 仓库
- [x] Clone 仓库
- [x] 创建分支
- [x] 提交更改
- [x] Push 分支
- [x] 创建 Pull Request

## 学习记录

写一两句话，说明这次练习中遇到的问题或学到的内容。
```

完整操作方法见 [学生提交流程](STUDENT_GUIDE.md)。

## 提交规则

1. 每位同学只修改自己在 `submissions` 目录下的文件。
2. 分支名使用 `submission/学号-姓名`，例如 `submission/20260001-张三`。
3. Commit 信息应说明做了什么，例如 `提交张三的 Git 练习`。
4. Pull Request 标题使用 `Git练习 - 学号 - 姓名`。
5. Pull Request 成功创建即视为提交；教师审核后统一合并。
6. 不要把账号密码、访问令牌或其他敏感信息提交到仓库。

## 教师批改

教师通过 Pull Requests 页面检查：

- 文件是否放在正确目录；
- 文件名和内容是否符合要求；
- 是否使用了独立分支；
- Commit 信息是否清晰；
- 是否正确发起 Pull Request。

