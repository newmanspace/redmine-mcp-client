# Feature 设计文档骨架模板

> 新增功能时，`design` 技能的输出应当遵循此骨架结构。
> 文档最终存放路径：`docs/development/features/feature-XX-<name>.md`

---

# Feature-XX: [功能名称]

## 1. Overview
- **目的**：[一句话说清楚这个功能解决什么痛点]
- **价值**：[对用户/系统带来什么收益]
- **作用域**：[影响的模块边界]

## 2. Architecture
- **组件交互图**：[Mermaid 或文字描述组件间的调用关系]
- **数据流向**：[必须标注是否遵循 ODS → DWD → DWS → ADS 层级]
- **依赖关系**：[涉及的上下游服务或模块]

## 3. API / MCP Design
- **工具命名**：`<verb>_redmine_<noun>`
- **入参定义**：

| 参数名 | 类型 | 必选 | 说明 |
|--------|------|------|------|
| `xxx` | `int` | ✅ | ... |

- **返回值结构**：[JSON 示例]

## 4. Database Design
- **新增表**：[表名、字段、索引]
- **Schema 变更**：[ALTER 语句摘要]
- **列顺序**：[参照 `dba-review/resources/column-ordering-standard.md`]

## 5. Implementation Plan
- **Phase 1**：[核心逻辑]
- **Phase 2**：[边缘处理 & 异常兜底]
- **Phase 3**：[测试与文档]

## 6. Risk & Mitigation
- [可能的风险点及其应对措施]
