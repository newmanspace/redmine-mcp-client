# Git Commit 消息正确示例集

> 本文件供 `git-commit` 技能在生成提交消息时作为 Few-shot 参考样例。

## ✅ 正确格式

```
feat(mcp): add issue search tool docs/development/features/feature-01-issue-search.md
```
```
fix(db): resolve null pointer in user query docs/development/issues/ISSUE-072.md
```
```
refactor(etl): extract ods sync logic to service layer docs/development/issues/ISSUE-103.md
```
```
docs(feature): add ai report builder spec docs/development/features/feature-09-ai-report.md
```
```
test(warehouse): add dws aggregation edge case tests docs/development/features/feature-09-ai-report.md
```

## ❌ 违规格式 (绝对禁止)

```
Added new feature for searching issues                                          ← 过去时态，无类型/scope，末尾无引用文档地址
```
```
feat(mcp): Add Issue Search Tool For Users.                                     ← 首字母大写，末尾有句号，无引用文档地址
```
```
feat(mcp): add a comprehensive issue search tool docs/development/issues.md     ← 超过 50 字符 (标题主体)
```
```
fix: resolve bug #123                                                           ← 错用了 Redmine Issue 号，而不是文档地址
```
