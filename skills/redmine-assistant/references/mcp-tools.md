# MCP 工具参考

完整记录 Redmine MCP Server 提供的所有工具（38 个）。

## 工具清单

### Issue 管理（5 个）

| 工具名 | 描述 | 关键参数 |
|--------|------|----------|
| `get_redmine_issue` | 获取 Issue 详情 | `issue_id`, `include_journals`, `include_attachments` |
| `list_my_redmine_issues` | 列出我的问题（分页） | `limit`, `offset`, `include_pagination_info`, `**filters` |
| `search_redmine_issues` | 搜索 Issue（20+ 过滤器） | `query`, `project_id`, `status_id`, `priority_id`, `fields` |
| `create_redmine_issue` | 创建新 Issue | `project_id`, `subject`, `description`, `**fields` |
| `update_redmine_issue` | 更新 Issue | `issue_id`, `fields`（支持 `status_name`） |

### Wiki 管理（3 个）

| 工具名 | 描述 | 关键参数 |
|--------|------|----------|
| `get_redmine_wiki_page` | 获取 Wiki 页面 | `project_id`, `wiki_page_title`, `version`, `include_attachments` |
| `create_redmine_wiki_page` | 创建 Wiki 页面 | `project_id`, `wiki_page_title`, `text`, `comments` |
| `update_redmine_wiki_page` | 更新 Wiki 页面 | `project_id`, `wiki_page_title`, `text`, `comments` |

### 项目管理（2 个）

| 工具名 | 描述 | 关键参数 |
|--------|------|----------|
| `list_redmine_projects` | 列出所有项目 | 无 |
| `search_redmine_issues` | 项目内搜索 Issue | 同 Issue 搜索 |

### 全局搜索（1 个）

| 工具名 | 描述 | 关键参数 |
|--------|------|----------|
| `search_entire_redmine` | 跨 Issue+Wiki 搜索 | `query`, `resources`, `limit`, `offset` |

### 报表构建器（10 个）

| 工具名 | 描述 | 关键参数 |
|--------|------|----------|
| `get_redmine_data_catalog` | 获取数据仓库目录 | `schema`, `limit` |
| `search_redmine_data_catalog` | 搜索表/字段 | `keyword`, `schema` |
| `execute_redmine_sql_query` | 执行 SQL（SELECT only） | `sql`, `limit`, `validate` |
| `generate_redmine_report_preview` | 生成报表预览 | `sql`, `description`, `limit` |
| `save_redmine_report_template` | 保存模板（版本化） | `code_content`, `description`, `is_public`, `version_comment` |
| `list_redmine_report_templates` | 列出模板 | `user_id`, `limit` |
| `execute_redmine_report_template` | 执行模板 | `template_id`, `params`, `output_format` |
| `preview_redmine_template` | 预览模板 | `template_id`, `params`, `limit`, `output_format`, `version_type` |
| `subscribe_redmine_template` | 订阅模板推送 | `template_id`, `channel`, `report_type`, `send_time` |
| `run_redmine_template_now` | 立即执行模板 | `template_id`, `params` |

### 模板版本管理（5 个）

| 工具名 | 描述 | 关键参数 |
|--------|------|----------|
| `get_redmine_template_versions` | 版本历史 | `template_id`, `limit` |
| `rollback_redmine_template_version` | 回滚版本 | `template_id`, `target_version` |
| `compare_redmine_template_versions` | 对比版本 | `template_id`, `version_a`, `version_b` |
| `activate_redmine_template_version` | 激活版本 | `template_id`, `version` |
| `get_redmine_active_template_version` | 获取激活版本 | `template_id` |
| `get_redmine_report_template` | 获取模板代码 | `template_id`, `version` |

### 订阅管理（4 个）

| 工具名 | 描述 | 关键参数 |
|--------|------|----------|
| `subscribe_project` | 订阅项目报告 | `project_id`, `channel`, `report_type`, `language` |
| `list_my_subscriptions` | 列出订阅 | 无 |
| `unsubscribe_project` | 取消订阅 | `project_id`, `user_id`, `channel` |
| `test_email_service` | 测试邮件服务 | `to_email` |
| `send_redmine_subscription_reports` | 发送订阅报告 | `report_type`, `template_id` |

### ETL 管理（4 个）

| 工具名 | 描述 | 关键参数 |
|--------|------|----------|
| `etl_project_backfill` | 回填历史数据 | `project_ids`, `start_date`, `end_date`, `force` |
| `etl_project_rerun` | 重新执行 ETL | `project_ids`, `since`, `force`, `retry_failed_only` |
| `get_etl_dashboard` | ETL 监控看板 | 无 |
| `get_etl_history` | ETL 执行历史 | `limit`, `dag_id`, `status` |

---

## 详细工具文档

### get_redmine_issue

```python
async def get_redmine_issue(
    issue_id: int,
    include_journals: bool = True,
    include_attachments: bool = True
) -> dict
```

**返回结构**:
```json
{
  "id": 123,
  "subject": "Bug title",
  "description": "...",
  "status": {"id": 1, "name": "New"},
  "priority": {"id": 2, "name": "Normal"},
  "project": {"id": 1, "name": "Project"},
  "journals": [...],
  "attachments": [...]
}
```

---

### list_my_redmine_issues

```python
async def list_my_redmine_issues(
    limit: int = 25,
    offset: int = 0,
    include_pagination_info: bool = False,
    **filters
) -> list[dict] | dict
```

**分页响应**:
```json
{
  "issues": [...],
  "pagination": {
    "total": 150,
    "limit": 25,
    "offset": 0,
    "has_next": true,
    "next_offset": 25
  }
}
```

---

### search_redmine_issues

```python
async def search_redmine_issues(
    query: str,
    limit: int = 25,
    offset: int = 0,
    include_pagination_info: bool = False,
    fields: list[str] = None,
    project_id: int = None,
    status_id: str = None,
    priority_id: str = None,
    tracker_id: int = None,
    assigned_to_id: int = None,
    fixed_version_id: int = None,
    category_id: int = None,
    start_date: str = None,
    due_date: str = None,
    created_on: str = None,
    updated_on: str = None,
    closed_on: str = None,
    parent_id: int = None,
    subproject_id: str = None,
    open_issues: bool = False
) -> list[dict] | dict
```

**支持的操作符**:
- `status_id="*"` - 仅开放问题
- `due_date=">=2026-03-01"` - 日期范围
- `fields=["id", "subject"]` - 字段选择

---

### create_redmine_issue

```python
async def create_redmine_issue(
    project_id: int,
    subject: str,
    description: str = "",
    tracker_id: int = None,
    priority_id: int = None,
    status_id: int = None,
    category_id: int = None,
    fixed_version_id: int = None,
    parent_issue_id: int = None,
    assigned_to_id: int = None,
    due_date: str = None,
    start_date: str = None,
    estimated_hours: float = None,
    custom_fields: dict = None
) -> dict
```

**自定义字段示例**:
```json
{
  "custom_fields": {
    "5": "Some value",
    "10": "123"
  }
}
```

---

### update_redmine_issue

```python
async def update_redmine_issue(
    issue_id: int,
    fields: dict
) -> dict
```

**支持 `status_name` 自动解析**:
```json
{
  "fields": {
    "status_name": "Resolved",
    "notes": "Fixed"
  }
}
```

---

### get_redmine_wiki_page

```python
async def get_redmine_wiki_page(
    project_id: str | int,
    wiki_page_title: str,
    version: int = None,
    include_attachments: bool = True
) -> dict
```

---

### execute_redmine_sql_query

```python
async def execute_redmine_sql_query(
    sql: str,
    limit: int = 100,
    validate: bool = True
) -> dict
```

**安全限制**:
- 仅允许 SELECT 语句
- 自动拒绝 DDL/DML
- 默认 LIMIT 100
- 最大 LIMIT 1000

---

### save_redmine_report_template

```python
async def save_redmine_report_template(
    code_content: str,
    description: str = "",
    is_public: bool = False,
    version_comment: str = ""
) -> dict
```

**返回**:
```json
{
  "success": true,
  "template": {
    "template_id": "tpl_name",
    "name": "Template Name",
    "version": 1
  },
  "version_bumped": true,
  "code_hash": "abc123..."
}
```

---

### preview_redmine_template

```python
async def preview_redmine_template(
    template_id: str,
    params: dict = None,
    limit: int = 10,
    output_format: str = "markdown",
    version_type: str = "latest",
    version: int = None
) -> dict
```

**输出格式**:
- `html` - 现代化 HTML（Web 浏览）
- `email` - 邮件兼容 HTML（内联 CSS + CID 图片）
- `markdown` - Markdown（终端显示）
- `plain` - 纯文本

---

### subscribe_redmine_template

```python
async def subscribe_redmine_template(
    template_id: str,
    channel: str = "email",
    report_type: str = "daily",
    send_time: str = "09:00",
    send_day_of_week: str = None,
    send_day_of_month: int = None,
    language: str = "zh_CN",
    user_name: str = None,
    user_email: str = None
) -> dict
```

**推送渠道**:
- `email` - 电子邮件
- `dingtalk` - 钉钉
- `telegram` - Telegram

**报告频率**:
- `daily` - 每日
- `weekly` - 每周（需 `send_day_of_week`）
- `monthly` - 每月（需 `send_day_of_month`）

---

## 数据仓库 Schema

### Schema 层级

| Schema | 描述 | 示例表 |
|--------|------|--------|
| `ods` | 原始数据层（与 Redmine API 同步） | `ods_issues`, `ods_projects` |
| `dwd` | 明细数据层（清洗/标准化） | `dwd_issues_full`, `dwd_projects` |
| `dws` | 汇总数据层（聚合统计） | `dws_project_daily_summary` |
| `ads` | 应用数据层（报表专用） | `ads_issue_metrics`, `ads_user_stats` |

### 常用表

#### dwd_issues_full
```sql
-- 问题明细表
id, project_id, tracker_id, status_id, priority_id,
subject, description, assigned_to_id, author_id,
due_date, start_date, estimated_hours, total_estimated_hours,
created_on, updated_on, closed_on, done_ratio
```

#### dws_project_daily_summary
```sql
-- 项目每日汇总
project_id, snapshot_date, total_issues, new_issues, closed_issues,
open_issues, total_hours, completed_hours
```

---

## 输出格式说明

### HTML 输出
- 现代化 Dashboard 风格
- 支持交互式图表（Chart.js）
- 响应式布局

### Email 输出
- 内联 CSS（邮件客户端兼容）
- CID 内嵌图片（绕过外链限制）
- 表格边框/样式内联

### Markdown 输出
- 终端友好格式
- 简单表格
- 无图片/图表
