# 第五章数据说明

主数据来自 V3 的 `heart-disease-four-site.csv`，本章保留假设检验所需字段，并新增教学标签：

- `disease = 1` 表示 `num > 0`，`0` 表示 `num = 0`；
- `sex_label` 和 `disease_label` 仅用于读表，不替代原始编码。

每行是一名受试者；四个 `site` 是数据来源中心，不应未经讨论地当作随机处理组。数据用于统计推断练习，不支持临床因果结论。

字段：`age` 年龄；`sex` 0=female、1=male；`trestbps` 静息收缩压；`chol` 血清胆固醇；`thalach` 最大心率；`oldpeak` 运动相对静息 ST 段压低；`num` 原始疾病等级。缺失值保留为空。
