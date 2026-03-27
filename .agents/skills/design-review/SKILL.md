---
name: design-review
description: 评估架构方案及新 Feature 设计并出具评审
---
# 架构与方案设计评审 (Design Review)

本技能以项目 Committer 的视角，对新方案（如数仓表结构新增、MCP 工具接口变更）进行严密的架构合规性评估。

## 评审检查清单

- [ ] **数仓分层**：是否符合 ODS→DWD→DWS→ADS 单向流
- [ ] **MCP 命名**：是否符合 `<verb>_redmine_<noun>` 格式
- [ ] **性能评估**：是否有 N+1 查询风险
- [ ] **数据倾斜**：DWS 层聚合压力评估
- [ ] **回滚方案**：是否有降级预案

## 输出动作
审查完成后，生成一份标准的 `Design Review Report`（参见 `design-review/examples/design-review-report-template.md`），标明方案状态为：
- ✅ **Feasible** — 可行无阻断
- ⚠️ **Risks** — 存在风险点需补充说明
- ❌ **Blockers** — 基础架构违规，需重新设计
