# Redmine MCP 智能集成平台：接口用途与交互流程指南 (User Guide & PPT 素材)

> **核心目标**: 介绍 Redmine MCP (Model Context Protocol) 提供的各类接口及其在全研发周期中的交互逻辑，并以“一张报表的开发”为例演示全流程。

---

## 1. 系统角色与交互架构
Redmine MCP 平台由四个核心组件协同工作：
1.  **Redmine Source (数据源)**: 原始业务数据的发源地（REST API）。
2.  **MCP Server ( redmine 插件)**: 提供给 AI 或客户端调用的标准化工具集（Toolbox）。
3.  **Data Warehouse (PostgreSQL/SQL)**: 存储清洗后的分层数据 (ODS -> DWD -> ADS)。
4.  **Reporting Engine (Python 引擎)**: 驱动动态报表渲染的执行环境。

---

## 2. 核心接口用途分类 (MCP Interface Map)

### A. 实时管理接口 (Management)
*   `search_redmine_issues`: 基于关键词/状态/人的即时 Issue 检索。
*   `update_redmine_issue`: 修改任务状态、负责人和截止时间。
*   `create_redmine_issue`: 自动化创建子任务或关联项。

### B. 数仓透视接口 (Data Access)
*   **元数据检索**: `get_redmine_data_catalog` 用于查看数仓各层表结构。
*   **灵活查询**: `execute_redmine_sql_query` 直接运行 SELECT 语句，从 ADS 层提取统计值。

### C. 报表全生命周期接口 (Report Lifecycle)
*   **开发维护**: `save_redmine_report_template` 提交 Python 版本的报表模版。
*   **即时获取**: `execute_redmine_report_template` 运行已保存的报表并输出 HTML/Markdown。
*   **推送订阅**: `subscribe_redmine_template` 设置定时邮件推送。

---

## 3. 典型交互流程示例：开发一张“项目统计报表”

以下是 AI 配合开发者，从零到一完成报表开发的完整链路：

### Step 1: 数据发现 (Discovery)
*   **调用**: `search_redmine_data_catalog(keyword="dim_project")`
*   **交互**: 系统返回数仓中所有项目相关的表及字段，开发者确认 `warehouse.dim_project` 为当前目标。

### Step 2: 逻辑验证 (Validation)
*   **调用**: `execute_redmine_sql_query(sql="SELECT count(*) FROM warehouse.ods_issues WHERE project_id=...")`
*   **交互**: 开发者在 SQL 沙盒中验证统计逻辑，确保取出的数据符合业务预期。

### Step 3: 模版开发与保存 (Development & Save)
*   **操作**: 开发者编写 Python Class（包含 SQL, HTML 渲染与 Chart.js 配置）。
*   **调用**: `save_redmine_report_template(code_content=..., template_id="my_new_report")`
*   **结果**: 系统解析代码哈希，版本号自动递增（如 v14 -> v15），并生成唯一的存储路径。

### Step 4: 预览与推送 (Preview & Distribution)
*   **预览**: `preview_redmine_template(template_id="...", output_format="email", to_email="...")`
*   **订阅**: `subscribe_redmine_template(template_id="...", report_type="daily")`
*   **交互**: 系统根据配置的 `send_time` 自动执行 Python 渲染逻辑，并向指定渠道通过 MCP 发送富文本报告。

---

## 4. 关键交互流程图 (Logic Flow)
1.  **数据流**: Redmine (RAW) -> ETL -> Warehouse (ADS) -> Template Engine -> User Interface.
2.  **指令流**: Developer (Instruction) -> MCP Server (Tool Call) -> SQL/Python Engine (Execution) -> Formatted Output.

---

## 5. 用户手册建议 (PPT 幻灯片大纲)
*   **Slide 1**: Redmine MCP 是什么？（AI 时代的研发数据翻译官）
*   **Slide 2**: 架构图解：从 REST API 到 Data Warehouse。
*   **Slide 3**: 接口百科：如何查询数据、管理任务、生成报表。
*   **Slide 4**: 实战演示：5 分钟内上线一个新的报表模版（见第 3 节流程）。
*   **Slide 5**: 未来展望：基于 MCP 接口的自动化研发助手（Auto-Reminders, Auto-Diagnosis）。
