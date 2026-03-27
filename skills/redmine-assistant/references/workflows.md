# 常用工作流

本文件记录 Redmine MCP 常用工作流和最佳实践。

## 目录

1. [Issue 管理工作流](#issue-管理工作流)
2. [Wiki 管理工作流](#wiki-管理工作流)
3. [报表开发工作流](#报表开发工作流)
4. [订阅推送工作流](#订阅推送工作流)
5. [ETL 管理工作流](#etl-管理工作流)

---

## Issue 管理工作流

### 工作流 1：创建并指派 Issue

**场景**：在项目中发现 Bug，创建 Issue 并指派给对应开发人员。

```python
# 步骤 1：获取项目列表确认 project_id
projects = list_redmine_projects()
# 找到目标项目，例如 project_id=176

# 步骤 2：创建 Issue
result = create_redmine_issue(
    project_id=176,
    subject="Bug: Login page returns 404",
    description="""
## Problem
Users report 404 error when clicking the login button.

## Steps to Reproduce
1. Navigate to /login
2. Click 'Login' button
3. 404 error appears

## Expected Behavior
Should redirect to dashboard after login.
""",
    tracker_id=1,  # Bug
    priority_id=3,  # High
    assigned_to_id=30,  # Developer ID
    due_date="2026-03-31",
    custom_fields={
        "5": "Production"  # Environment field
    }
)

# 步骤 3：确认创建成功
if "error" not in result:
    print(f"Created issue #{result['id']}")
    print(f"Subject: {result['subject']}")
    print(f"Status: {result['status']['name']}")
else:
    print(f"Error: {result['error']}")
```

**注意事项**:
- 某些项目要求必填字段（如 `assigned_to_id`, `due_date`）
- 自定义字段 ID 因 Redmine 实例而异
- 使用 `custom_fields` 传递自定义字段值

**myCIM2+ DevOps 项目 (#176) 必填字段**:
根据该项目配置，创建 Issue 时以下字段为必填：
- `assigned_to_id` - 指派人 ID
- `due_date` - 截止日期 (YYYY-MM-DD 格式)
- `custom_fields["1"]` - Root Cause (根本原因)
- `custom_fields["2"]` - 其他自定义字段

示例:
```python
create_redmine_issue(
    project_id=176,
    subject="Issue title",
    description="Description...",
    assigned_to_id=30,
    due_date="2026-03-31",
    custom_fields={
        "1": "根因分析",  # Root Cause - 必填
        "2": "其他字段值"
    }
)
```

---

### 工作流 2：搜索并批量更新 Issue

**场景**：将项目中所有 "In Progress" 状态的 Issue 更新为 "On Hold"。

```python
# 步骤 1：搜索目标 Issue
issues = search_redmine_issues(
    query="",  # 空查询匹配所有
    project_id=176,
    status_id="2",  # In Progress
    limit=100,
    fields=["id", "subject", "status"]
)

# 步骤 2：批量更新
updated_count = 0
for issue in issues:
    result = update_redmine_issue(
        issue_id=issue["id"],
        fields={
            "status_name": "On Hold",
            "notes": "Blocked by infrastructure issue"
        }
    )
    if "error" not in result:
        updated_count += 1
        print(f"Updated #{issue['id']}: {issue['subject']}")
    else:
        print(f"Failed to update #{issue['id']}: {result.get('error')}")

print(f"Total updated: {updated_count}/{len(issues)}")
```

---

### 工作流 3：查询我的待办事项

**场景**：每天早上查看分配给自己的 Issue。

```python
# 获取我的所有开放 Issue
my_issues = list_my_redmine_issues(
    limit=50,
    include_pagination_info=True,
    status_id="*"  # 开放状态
)

# 处理分页响应
if "pagination" in my_issues:
    issues = my_issues["issues"]
    total = my_issues["pagination"]["total"]
    print(f"You have {total} open issues (showing {len(issues)})")
else:
    issues = my_issues
    print(f"You have {len(issues)} issues")

# 按优先级排序显示
for issue in issues:
    priority = issue.get("priority", {}).get("name", "N/A")
    status = issue.get("status", {}).get("name", "N/A")
    print(f"#{issue['id']} [{priority}] {issue['subject']} - {status}")
```

---

### 工作流 4：Issue 评论和状态流转

**场景**：更新 Issue 状态并添加解决说明。

```python
# 获取 Issue 详情（含历史评论）
issue = get_redmine_issue(
    issue_id=123,
    include_journals=True,
    include_attachments=True
)

# 查看历史评论
if issue.get("journals"):
    print("Comment history:")
    for journal in issue["journals"][-5:]:  # 最近 5 条评论
        print(f"  {journal['user']['name']}: {journal.get('notes', '')}")

# 更新状态并添加说明
result = update_redmine_issue(
    issue_id=123,
    fields={
        "status_name": "Resolved",
        "notes": """
## Root Cause
The 404 error was caused by a missing route configuration.

## Solution
Added the missing route in config/routes.rb

## Testing
- Tested login flow locally
- Verified on staging environment
""",
        "fixed_version_id": 10  # Target version
    }
)
```

---

## Wiki 管理工作流

### 工作流 1：创建项目文档

**场景**：为新项目创建完整的 Wiki 文档结构。

```python
# 文档结构
pages = [
    {
        "title": "Getting_Started",
        "text": """# Getting Started

## Prerequisites
- Python 3.8+
- PostgreSQL 13+

## Installation
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Configure database: `cp .env.example .env`
4. Run migrations: `rails db:migrate`
"""
    },
    {
        "title": "Architecture",
        "text": """# Architecture

## System Overview
The system follows a layered architecture:

1. **Presentation Layer**: React frontend
2. **Application Layer**: Rails API
3. **Data Layer**: PostgreSQL + Redis

## Data Flow
User -> React App -> Rails API -> PostgreSQL
"""
    },
    {
        "title": "API_Reference",
        "text": """# API Reference

## Authentication
All requests require API key in header:
```
X-Redmine-API-Key: your-api-key
```

## Endpoints

### GET /issues.json
Returns list of issues.

### POST /issues.json
Create new issue.
"""
    }
]

# 批量创建
project_id = 176
for page in pages:
    result = create_redmine_wiki_page(
        project_id=project_id,
        wiki_page_title=page["title"],
        text=page["text"],
        comments="Initial documentation"
    )
    if "error" not in result:
        print(f"Created: {page['title']}")
    else:
        print(f"Failed: {page['title']} - {result.get('error')}")
```

---

### 工作流 2：更新 Wiki 并保留版本历史

**场景**：更新文档时添加详细的变更说明。

```python
# 获取当前版本
current = get_redmine_wiki_page(
    project_id=176,
    wiki_page_title="Installation_Guide"
)

print(f"Current version: {current['version']}")
print(f"Last updated: {current['updated_on']}")

# 更新内容
new_content = """
# Installation Guide

## Updated: 2026-03-26

## System Requirements
- Python 3.9+ (updated from 3.8)
- PostgreSQL 14+ (updated from 13)
- Node.js 18+ (new requirement)

## Installation Steps
...
"""

result = update_redmine_wiki_page(
    project_id=176,
    wiki_page_title="Installation_Guide",
    text=new_content,
    comments="Update requirements for v2.0: Python 3.9+, PostgreSQL 14+, add Node.js 18+"
)

print(f"Updated to version: {result['version']}")
```

---

## 报表开发工作流

### 工作流 1：探索数据仓库

**场景**：了解可用的数据表和字段。

```python
# 步骤 1：获取数据目录
catalog = get_redmine_data_catalog(schema="dwd", limit=50)

print("Available tables in DWD schema:")
for table in catalog.get("tables", []):
    print(f"  - {table['table_name']}")

# 步骤 2：搜索特定主题的表
search_result = search_redmine_data_catalog(
    keyword="issue",
    schema="warehouse"
)

print(f"\nTables matching 'issue':")
for table in search_result.get("matching_tables", []):
    print(f"  - {table}")

print(f"\nColumns matching 'issue':")
for col in search_result.get("matching_columns", []):
    print(f"  - {col['table']}.{col['column']} ({col['type']})")
```

---

### 工作流 2：开发和测试 SQL 查询

**场景**：开发一个开发者效率统计报表。

```python
# 步骤 1：探索表结构
catalog = get_redmine_data_catalog(schema="dwd")

# 步骤 2：编写查询
sql = """
SELECT
    u.login,
    u.name,
    COUNT(i.id) as total_issues,
    COUNT(CASE WHEN i.status_id = 5 THEN 1 END) as closed_issues,
    AVG(i.estimated_hours) as avg_hours,
    SUM(i.done_ratio) / COUNT(*) as avg_completion
FROM dwd_issues_full i
LEFT JOIN dim_users u ON i.assigned_to_id = u.id
WHERE i.created_on >= DATE_TRUNC('month', CURRENT_DATE - INTERVAL '1 month')
  AND i.created_on < DATE_TRUNC('month', CURRENT_DATE)
GROUP BY u.login, u.name
ORDER BY closed_issues DESC
LIMIT 20
"""

# 步骤 3：测试查询
result = execute_redmine_sql_query(sql, limit=20)

if result.get("success"):
    print(f"Query executed in {result['execution_time_ms']}ms")
    print(f"Rows returned: {result['row_count']}")

    # 显示数据
    columns = result["data"][0].keys() if result["data"] else []
    print("| " + " | ".join(columns) + " |")
    print("|" + "|".join(["---"] * len(columns)) + "|")

    for row in result["data"][:5]:
        print("| " + " | ".join(str(v) for v in row.values()) + " |")
else:
    print(f"Error: {result.get('error')}")
```

---

### 工作流 3：保存报表模板

**场景**：将测试好的 SQL 保存为可复用的模板。

```python
# 完整的模板代码
template_code = '''
def run(params, output_format="html"):
    """Developer Efficiency Report"""

    # Get parameters
    months = params.get("months", 1)

    # SQL query
    sql = f"""
    SELECT
        u.login,
        u.name,
        COUNT(i.id) as total_issues,
        COUNT(CASE WHEN i.status_id = 5 THEN 1 END) as closed_issues,
        AVG(i.estimated_hours) as avg_hours
    FROM dwd_issues_full i
    LEFT JOIN dim_users u ON i.assigned_to_id = u.id
    WHERE i.created_on >= DATE_TRUNC('month', CURRENT_DATE - INTERVAL '{months} month')
    GROUP BY u.login, u.name
    ORDER BY closed_issues DESC
    """

    # Execute query
    data = execute_sql(sql)

    # Render based on output_format
    if output_format == "html":
        return render_html(data, title="Developer Efficiency Report")
    elif output_format == "markdown":
        return render_markdown(data, title="Developer Efficiency Report")
    elif output_format == "email":
        return render_mail(data, title="Developer Efficiency Report")
    else:
        return {"data": data}
'''

# 保存模板
result = save_redmine_report_template(
    code_content=template_code,
    description="Monthly developer efficiency statistics",
    is_public=False,
    version_comment="Initial version with basic metrics"
)

if result.get("success"):
    template_id = result["template"]["template_id"]
    print(f"Template saved: {template_id}")
    print(f"Version: {result['template']['version']}")
else:
    print(f"Error: {result.get('error')}")
```

---

### 工作流 4：预览和执行模板

**场景**：预览模板效果并执行生成报表。

```python
# 步骤 1：列出可用模板
templates = list_redmine_report_templates(limit=10)
for t in templates.get("templates", []):
    print(f"  {t['template_id']}: {t['name']}")

# 步骤 2：预览模板（Markdown 格式）
preview = preview_redmine_template(
    template_id="tpl_dev_efficiency",
    params={"months": 1},
    limit=10,
    output_format="markdown",
    version_type="latest"
)

print("\n### Preview (Markdown) ###")
print(preview.get("content", ""))

# 步骤 3：执行完整报表（HTML 格式）
report = execute_redmine_report_template(
    template_id="tpl_dev_efficiency",
    params={"months": 3},
    output_format="html"
)

print(f"\n### Report Generated ###")
print(f"Execution time: {report.get('execution_time_ms')}ms")
print(f"Row count: {report.get('row_count')}")
```

---

## 订阅推送工作流

### 工作流 1：订阅定期报表

**场景**：订阅每周效率报告，自动发送到邮箱。

```python
# 步骤 1：查看可用模板
templates = list_redmine_report_templates()

# 步骤 2：订阅模板
result = subscribe_redmine_template(
    template_id="tpl_dev_efficiency",
    channel="email",
    report_type="weekly",
    send_time="09:00",
    send_day_of_week="Mon",
    language="zh_CN",
    user_name="John Doe",
    user_email="john@example.com"
)

if "subscription_id" in result:
    print(f"Subscribed! ID: {result['subscription_id']}")
    print(f"Next delivery: Monday at 09:00")
else:
    print(f"Error: {result.get('error')}")

# 步骤 3：查看我的订阅
subscriptions = list_my_subscriptions()
print("\nMy subscriptions:")
for sub in subscriptions.get("subscriptions", []):
    print(f"  - {sub['template_id']} ({sub['report_type']}) -> {sub['channel_id']}")
```

---

### 工作流 2：测试邮件服务

**场景**：在订阅前测试邮件服务配置。

```python
# 测试邮件服务
result = test_email_service(to_email="test@example.com")

if result.get("connection", {}).get("success"):
    print("Email service is configured correctly!")
    print(f"SMTP Server: {result['connection']['smtp_server']}")
    print(f"Connection: {result['connection'].get('message', '')}")

    if result.get("test_email", {}).get("success"):
        print("Test email sent successfully!")
    else:
        print(f"Test email failed: {result['test_email'].get('error')}")
else:
    print(f"Connection failed: {result.get('error')}")
```

---

## ETL 管理工作流

### 工作流 1：查看 ETL 状态

**场景**：检查数据同步状态。

```python
# 获取 ETL 看板
dashboard = get_etl_dashboard()

print("### ETL Dashboard ###")
print(f"Health Score: {dashboard.get('health_score', 'N/A')}")

status = dashboard.get("current_status", {})
print(f"Last Sync: {status.get('last_sync_time', 'N/A')}")
print(f"Status: {status.get('status', 'N/A')}")

stats = dashboard.get("statistics_7d", {})
print(f"\n7-day Statistics:")
print(f"  Total Runs: {stats.get('total_runs', 0)}")
print(f"  Success Rate: {stats.get('success_rate', 0):.1%}")
print(f"  Avg Duration: {stats.get('avg_duration_ms', 0) / 1000:.1f}s")

# 查看最近历史
history = get_etl_history(limit=10)
print("\n### Recent History ###")
for record in history.get("history", [])[:5]:
    print(f"  [{record['status']}] {record['dag_id']} - {record['execution_time_ms']}ms")
```

---

### 工作流 2：回填历史数据

**场景**：新部署后需要回填历史数据。

```python
# 回填最近 3 个月的数据
result = etl_project_backfill(
    project_ids=[176, 177],  # 特定项目
    start_date="2026-01-01",
    end_date="2026-03-26",
    force=False,  # 跳过已同步数据
    skip_inactive=True  # 跳过已关闭项目
)

print("### Backfill Results ###")
print(f"Status: {result.get('status')}")
print(f"Projects processed: {result.get('projects_processed', 0)}")
print(f"Total records synced: {result.get('total_records', 0)}")
print(f"Duration: {result.get('duration_ms', 0) / 1000:.1f}s")

if result.get("details"):
    print("\n### Details by Layer ###")
    for layer, count in result["details"].items():
        print(f"  {layer}: {count} records")
```

---

### 工作流 3：重新执行失败的 ETL

**场景**：ETL 执行失败后重新运行。

```python
# 查看失败的执行
history = get_etl_history(limit=10, status="failed")

if history.get("history"):
    failed_dag = history["history"][0]["dag_id"]
    print(f"Last failed DAG: {failed_dag}")

    # 重新执行
    result = etl_project_rerun(
        project_ids=None,  # 所有项目
        since="2026-03-25T00:00:00",
        force=True,
        retry_failed_only=True
    )

    print("### Re-run Results ###")
    print(f"Status: {result.get('status')}")
    print(f"Projects: {result.get('projects_processed', 0)}")
    print(f"Records: {result.get('total_records', 0)}")
```

---

## 最佳实践

### Token 优化

```python
# 差：获取所有字段，消耗大量 token
issues = list_my_redmine_issues(limit=100)

# 好：仅获取必要字段
issues = list_my_redmine_issues(
    limit=100,
    # fields=["id", "subject", "status"]  # 如果工具支持
)
```

### 错误处理

```python
def safe_get_issue(issue_id):
    result = get_redmine_issue(issue_id)
    if "error" in result:
        logging.error(f"Failed to get issue {issue_id}: {result['error']}")
        return None
    return result

def safe_create_issue(**kwargs):
    result = create_redmine_issue(**kwargs)
    if "error" in result:
        logging.error(f"Failed to create issue: {result['error']}")
        return None
    return result
```

### 分页处理

```python
def get_all_my_issues():
    all_issues = []
    offset = 0
    limit = 100

    while True:
        result = list_my_redmine_issues(
            limit=limit,
            offset=offset,
            include_pagination_info=True
        )

        issues = result.get("issues", [])
        all_issues.extend(issues)

        if not result.get("pagination", {}).get("has_next"):
            break

        offset += limit

    return all_issues
```
