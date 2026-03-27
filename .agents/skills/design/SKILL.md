---
name: design
description: 根据需求初步出具架构防呆方案与全盘 Feature 说明文档
---
# 方案设计 (Design)

本技能负责将一个中大型业务需求，转化为一份结构化的架构设计文档。它是动手写代码之前的蓝图产出能力。

## 前置约束（提问驱动与项目嗅探）
在接到需求并开始撰写方案前，**必须严格执行以下前置动作**：
1. **自动嗅探全局**：读取并扫描项目根目录的核心配置文件，探测当前所用的具体版本栈及业务逻辑上下文。
2. **主动提问澄清**：强制向用户提出 1 到 2 个关于业务背景的澄清问题（如：是否有极高并发要求？是否需要兼容某历史版本数据？）。**必须等待明确回答后，才能开始撰写方案。**

## 文档架构与输出标准
在获得澄清问题的回答后，基于诉求自动出具一份结构化的设计方案文档，存放路径遵循 `docs/development/features/` 目录下的 README 要求。
文档内容应当严格遵守该项目规定的 Feature 骨架（参见 `design/examples/feature-document-template.md`）：
1. **Overview**: 目的、价值与作用域
2. **Architecture**: 组件交互与数据流向（是否符合 ODS→DWD→DWS 层原则）
3. **API/MCP Design**: 接口标准与 payload（`<verb>_redmine_<noun>`）
4. **Database Design**: Schema 或迁移思路
5. **Implementation Plan**: 具体阶段切分

## 输出动作

审查完成后，生成一份标准的 `Design Document`（参见 `design/examples/feature-document-template.md`），包含：

1. **Overview** - 目的与作用域
2. **Architecture** - 组件交互图（是否符合 ODS→DWD→DWS 层）
3. **API/MCP Design** - 接口标准（`<verb>_redmine_<noun>`）
4. **Database Design** - Schema 变更
5. **Implementation Plan** - 阶段划分

状态标记：
- ✅ **Approved** — 方案可行
- ⚠️ **Risks** — 需补充说明
- ❌ **Rejected** — 架构违规
