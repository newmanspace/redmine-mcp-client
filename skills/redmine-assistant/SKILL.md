---
name: redmine-assistant
description: This skill should be used when the user asks to "list issues", "create issue", "search Redmine", "get wiki page", "create report", "query project data", "run SQL against warehouse", or discusses Redmine project management, issue tracking, wiki documentation, or AI report generation.
version: 1.0.0
---

# Redmine Assistant

## 概述

本 Skill 提供与 Redmine MCP 服务器交互的完整能力，包括：

1. **Issue 管理** - 创建/更新/查询/搜索问题
2. **Wiki 管理** - 获取/创建/更新文档页面
3. **项目管理** - 列出项目、搜索项目问题
4. **全局搜索** - 跨 Issue 和 Wiki 搜索
5. **AI 报表构建器** - 模板化报表生成（HTML/Email/Markdown）
6. **订阅推送** - Email/DingTalk/Telegram 定期推送
7. **ETL 管理** - 数据同步/ETL 监控
8. **配置管理** - 支持环境变量配置（MCP 地址、Token）

## 子技能

### redmine-report-builder

**报表开发专用 Skill**，提供：
- 表结构探索和解释
- SQL 自动生成
- 模板一键创建
- **自动化工作流脚本** (`scripts/automate_report.py`)

详见：[`SKILL-report-builder.md`](./SKILL-report-builder.md)

## 参考文档

| 文档 | 说明 |
|------|------|
| [references/mcp-tools.md](./references/mcp-tools.md) | MCP 工具完整参考 |
| [references/workflows.md](./references/workflows.md) | 常用工作流示例 |
| [references/data-schema.md](./references/data-schema.md) | 数据仓库表结构 |
| [SKILL-report-builder.md](./SKILL-report-builder.md) | 报表开发助手 |

## MCP 工具调用指南

### 发现可用工具

调用 MCP 工具前，先确认工具是否可用：

```
可用工具列表通过 MCP 协议自动加载
```

### Issue 相关工具调用

#### 获取 Issue 详情
```python
get_redmine_issue(issue_id=123, include_journals=True, include_attachments=True)
```

#### 列出我的问题（分页）
```python
list_my_redmine_issues(limit=25, offset=0, include_pagination_info=True)
```

#### 搜索 Issue
```python
search_redmine_issues(
    query="bug fix",
    project_id=176,
    status_id="*",  # 仅开放问题
    limit=25,
    fields=["id", "subject", "status", "priority"]  # 减少 token 使用
)
```

#### 创建 Issue
```python
create_redmine_issue(
    project_id=176,
    subject="Fix login bug",
    description="Detailed description...",
    tracker_id=1,  # Bug
    priority_id=3,  # High
    assigned_to_id=30,
    due_date="2026-03-31"
)
```

#### 更新 Issue
```python
update_redmine_issue(
    issue_id=123,
    fields={
        "status_name": "Resolved",  # 自动解析为 status_id
        "notes": "Fixed the issue"
    }
)
```

### Wiki 相关工具调用

#### 获取 Wiki 页面
```python
get_redmine_wiki_page(
    project_id=176,
    wiki_page_title="Installation_Guide",
    version=None,  # None = 最新版本
    include_attachments=True
)
```

#### 创建 Wiki 页面
```python
create_redmine_wiki_page(
    project_id=176,
    wiki_page_title="Getting_Started",
    text="# Getting Started\n\nWelcome...",
    comments="Initial page"
)
```

#### 更新 Wiki 页面
```python
update_redmine_wiki_page(
    project_id=176,
    wiki_page_title="FAQ",
    text="# FAQ\n\nUpdated content...",
    comments="Added new entries"
)
```

### 搜索工具调用

#### 全局搜索（Issue + Wiki）
```python
search_entire_redmine(
    query="installation",
    resources=["issues", "wiki_pages"],  # 或仅 ["issues"]
    limit=50
)
```

#### 项目内搜索 Issue
```python
search_redmine_issues(
    query="performance",
    project_id=176,
    limit=25
)
```

### 报表构建器工具调用

#### 获取数据目录
```python
get_redmine_data_catalog(schema="warehouse", limit=100)
```

#### 搜索表/字段
```python
search_redmine_data_catalog(keyword="issue", schema="dwd")
```

#### 执行 SQL 查询
```python
execute_redmine_sql_query(
    sql="SELECT * FROM dwd_issues_full WHERE status_id = 1 LIMIT 10",
    limit=100
)
```

#### 保存报表模板
```python
save_redmine_report_template(
    code_content='def run(params): ...',  # 完整 Python 代码
    description="Developer efficiency report",
    is_public=False,
    version_comment="Initial version"
)
```

#### 列出模板
```python
list_redmine_report_templates(limit=50)
```

#### 预览模板
```python
preview_redmine_template(
    template_id="tpl_dev_efficiency",
    params={"date_range": "last_3_months"},
    limit=10,
    output_format="html",  # html/markdown/plain
    version_type="latest"
)
```

#### 执行模板
```python
execute_redmine_report_template(
    template_id="tpl_dev_efficiency",
    params={"date_range": "last_3_months"},
    output_format="html"
)
```

#### 订阅模板推送
```python
subscribe_redmine_template(
    template_id="tpl_dev_efficiency",
    channel="email",
    report_type="weekly",  # daily/weekly/monthly
    send_time="09:00",
    send_day_of_week="Mon",
    language="zh_CN"
)
```

### 模板版本管理

#### 获取版本历史
```python
get_redmine_template_versions(template_id="tpl_dev_efficiency", limit=50)
```

#### 回滚版本
```python
rollback_redmine_template_version(
    template_id="tpl_dev_efficiency",
    target_version=2
)
```

#### 对比版本
```python
compare_redmine_template_versions(
    template_id="tpl_dev_efficiency",
    version_a=1,
    version_b=2
)
```

#### 激活版本
```python
activate_redmine_template_version(
    template_id="tpl_dev_efficiency",
    version=2
)
```

### 订阅管理

#### 列出订阅
```python
list_my_subscriptions()
```

#### 取消订阅
```python
unsubscribe_project(project_id=176)
```

#### 测试邮件服务
```python
test_email_service(to_email="user@example.com")
```

### ETL 管理

#### 查看 ETL 看板
```python
get_etl_dashboard()
```

#### 查看 ETL 历史
```python
get_etl_history(limit=20, status="success")
```

#### 回填数据
```python
etl_project_backfill(
    project_ids=[176],
    start_date="2026-01-01",
    end_date="2026-03-01"
)
```

#### 重新执行
```python
etl_project_rerun(
    project_ids=[176],
    since="2026-03-01T00:00:00",
    force=True
)
```

### 自动化工作流脚本

该 Skill 提供 `scripts/automate_report.py`，允许 Agent 快速执行预定义的复杂报表工作流：

```bash
# 执行项目日报自动化工作流
python3 scripts/automate_report.py project_daily --project 176

# 执行开发者效率自动化工作流
python3 scripts/automate_report.py dev_efficiency --project 176
```

### 配置说明

脚本支持通过环境变量进行自定义配置：

```bash
export REDMINE_MCP_URL="http://YOUR_SERVER_IP:8000/mcp"
export REDMINE_MCP_TOKEN="your_token_here"
```

或者创建 `.env` 文件（参考 [`.env.example`](file:///docker/redmine-mcp-client/.env.example)）。

## 常用工作流

### 工作流 1：创建 Issue 并指派

```python
# 1. 获取项目信息
projects = list_redmine_projects()

# 2. 创建 Issue
result = create_redmine_issue(
    project_id=176,
    subject="Bug: Login page 404 error",
    description="Users report 404 when clicking login...",
    tracker_id=1,
    priority_id=3,
    assigned_to_id=30,
    due_date="2026-03-31"
)

# 3. 确认创建成功
print(f"Created issue #{result['id']}")
```

### 工作流 2：搜索并更新 Issue

```python
# 1. 搜索相关 Issue
issues = search_redmine_issues(
    query="login 404",
    project_id=176,
    status_id="*",  # 仅开放
    fields=["id", "subject", "status"]
)

# 2. 更新第一个匹配
if issues:
    update_redmine_issue(
        issue_id=issues[0]["id"],
        fields={
            "status_name": "In Progress",
            "notes": "Investigating..."
        }
    )
```

### 工作流 3：创建报表模板

```python
# 1. 查看可用数据表
catalog = get_redmine_data_catalog(schema="dwd")

# 2. 设计 SQL
sql = """
SELECT
    u.name as user_name,
    COUNT(i.id) as issues_fixed,
    AVG(i.estimated_hours) as avg_hours
FROM dwd_issues_full i
JOIN dim_users u ON i.assigned_to_id = u.id
WHERE i.status_id = 5  # Closed
GROUP BY u.name
ORDER BY issues_fixed DESC
"""

# 3. 测试 SQL
result = execute_redmine_sql_query(sql, limit=10)

# 4. 保存为模板
code = '''
def run(params, output_format="html"):
    sql = """SELECT ..."""
    data = execute_sql(sql)

    if output_format == "html":
        return render_html(data, title="Developer Efficiency")
    elif output_format == "markdown":
        return render_markdown(data)
    else:
        return {"data": data}
'''

save_redmine_report_template(
    code_content=code,
    description="Developer efficiency report",
    is_public=False
)
```

### 工作流 4：订阅定期报告

```python
# 1. 列出可用模板
templates = list_redmine_report_templates()

# 2. 订阅模板
subscribe_redmine_template(
    template_id="tpl_dev_efficiency",
    channel="email",
    report_type="weekly",
    send_time="09:00",
    send_day_of_week="Mon",
    language="zh_CN"
)

# 3. 确认订阅
subscriptions = list_my_subscriptions()
```

## 最佳实践

### Token 优化

1. **使用分页**：`limit=25` 默认值，避免大量数据一次性加载
2. **字段选择**：`fields=["id", "subject", "status"]` 仅获取必要字段
3. **按需加载**：`include_journals=False` 当不需要评论时

### 错误处理

```python
result = get_redmine_issue(issue_id=99999)
if "error" in result:
    print(f"Error: {result['error']}")
    # 处理错误...
```

### 安全考虑

1. **SELECT  Only**：SQL 查询仅允许 SELECT 语句
2. **参数绑定**：所有用户输入使用参数绑定
3. **行限制**：默认 LIMIT 100，最大 LIMIT 1000

## 参考文件

- [`references/mcp-tools.md`](./references/mcp-tools.md) - 完整 MCP 工具参考
- [`references/workflows.md`](./references/workflows.md) - 详细工作流示例
- [`references/api-docs.md`](./references/api-docs.md) - Redmine API 文档

## 示例文件

- [`examples/templates/`](./examples/templates/) - 报表模板示例
