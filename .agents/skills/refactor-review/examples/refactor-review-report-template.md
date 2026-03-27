# Refactor Review Report Template

**重构编号**: REFACTOR-XXX-<name>
**审查日期**: YYYY-MM-DD
**审查员**: AI Reviewer

## 审查结论

- [ ] **Approved** - 重构符合全部原则
- [ ] **Risks** - 存在风险点需关注
- [ ] **Rejected** - 违反核心原则，需重新重构

## 审查检查点

| 检查项 | 状态 | 备注 |
|--------|------|------|
| 重构文档完整 | ✅/❌ | |
| 分层架构合规 | ✅/❌ | |
| 测试先行原则 | ✅/❌ | |
| 自下而上顺序 | ✅/❌ | |
| 上层测试覆盖 | ✅/❌ | |
| 代码质量达标 | ✅/❌ | |
| 架构一致性 | ✅/❌ | |

## 发现的问题

### Critical (阻断)

- [ ] 无
- [ ] 问题描述及影响

### High (高优先级)

- [ ] 无
- [ ] 问题描述及影响

### Medium (中优先级)

- [ ] 无
- [ ] 问题描述及影响

## 修正建议

<具体修改指引>

## 附录

### 测试覆盖率

```
Name                    Stmts   Miss  Cover
-------------------------------------------
src/redmine_mcp_server   X       Y     Z%
```

### 变更统计

```
X files changed, +N insertions(+), -M deletions(-)
```

### Git 提交历史

```
<git log --oneline 输出>
```

### 审查依据

- [REFACTOR-XXX-*.md](../../../docs/development/refactoring/REFACTOR-XXX-*.md) - 重构文档
- [REFACTOR-002](../../../docs/development/refactoring/REFACTOR-002-mcp-tools-layered.md) - 参考示例
