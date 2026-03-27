---
name: redmine-report-builder
description: Redmine AI Report Builder - 智能报表开发助手，支持表结构探索、SQL 生成、模板创建
version: 1.0.0
---

# Redmine AI Report Builder

## 概述

本 Skill 提供智能化的报表开发能力，包括：

1. **表结构探索** - 自动获取并解释数据仓库 schema
2. **智能推荐** - 根据报表类型推荐表和字段
3. **SQL 生成** - 自动生成优化后的查询语句
4. **模板创建** - 一键保存为可复用模板

## 核心能力

### 1. 表结构探索

#### 获取完整数据目录
```python
# 获取所有 schema 的表
catalog = get_redmine_data_catalog(schema="warehouse", limit=200)

# 获取特定 schema
dwd_catalog = get_redmine_data_catalog(schema="dwd", limit=50)
dws_catalog = get_redmine_data_catalog(schema="dws", limit=50)
dim_catalog = get_redmine_data_catalog(schema="dim", limit=50)
```

#### 搜索相关表
```python
# 搜索 issue 相关的表
search_redmine_data_catalog(keyword="issue", schema="dwd")

# 搜索项目汇总相关的表
search_redmine_data_catalog(keyword="project summary", schema="dws")

# 搜索用户相关的字段
search_redmine_data_catalog(keyword="user", schema="dim")
```

#### 解释表结构
获取表结构后，自动解析并展示：
- 字段名称和类型
- 主键/外键关系
- 字段业务含义
- 推荐的 JOIN 路径

### 2. 智能推荐

#### 根据报表类型推荐表

| 报表类型 | 推荐表 | 理由 |
|----------|--------|------|
| 项目日报 | `dws_project_daily_summary` | 已预聚合，性能好 |
| 开发者效率 | `dwd_issues_full` + `dim_users` | 需要明细数据 |
| Issue 趋势 | `dwd_issue_daily_snapshot` | 每日快照适合趋势 |
| 负载分析 | `dws_user_loading_daily` | 用户负载汇总 |
| 质量指标 | `ads_issue_metrics` | 预计算指标 |

#### 推荐 JOIN 路径

当查询涉及多表时，自动推荐最优 JOIN 路径：

```
查询：开发者效率报表

推荐方案:
  FROM dwd_issues_full i
  LEFT JOIN dim_users u ON i.assigned_to_id = u.id

理由:
  - dwd_issues_full 包含完整的 Issue 明细
  - dim_users 提供开发者姓名等信息
  - 通过 assigned_to_id 直接关联，无需中间表
```

### 3. SQL 生成

#### 生成项目日报 SQL
```python
def generate_project_daily_sql(project_id, days=7):
    return f"""
    SELECT
        snapshot_date,
        total_issues,
        new_issues,
        closed_issues,
        status_new,
        status_in_progress,
        status_resolved,
        status_closed
    FROM dws_project_daily_summary
    WHERE project_id = {project_id}
      AND snapshot_date >= CURRENT_DATE - INTERVAL '{days} days'
    ORDER BY snapshot_date DESC
    """
```

#### 生成开发者效率 SQL
```python
def generate_developer_efficiency_sql(months=1):
    return f"""
    SELECT
        u.login,
        u.name,
        COUNT(i.id) as total_issues,
        COUNT(CASE WHEN i.status_id = 5 THEN 1 END) as closed_issues,
        SUM(i.estimated_hours) as total_hours,
        AVG(i.done_ratio) as avg_completion
    FROM dwd_issues_full i
    LEFT JOIN dim_users u ON i.assigned_to_id = u.id
    WHERE i.assigned_to_id IS NOT NULL
      AND i.created_on >= DATE_TRUNC('month', CURRENT_DATE - INTERVAL '{months} months')
      AND i.created_on < DATE_TRUNC('month', CURRENT_DATE)
    GROUP BY u.id, u.login, u.name
    ORDER BY closed_issues DESC
    """
```

### 4. 模板创建

#### 完整模板示例
```python
template_code = '''
def run(params, output_format="html"):
    """项目日报报表"""

    project_id = params.get("project_id", 176)
    days = params.get("days", 7)

    # 查询项目日报数据
    sql = f"""
    SELECT
        snapshot_date,
        total_issues,
        new_issues,
        closed_issues,
        status_new,
        status_in_progress,
        status_resolved,
        status_closed,
        priority_immediate,
        priority_urgent,
        priority_high
    FROM dws_project_daily_summary
    WHERE project_id = {project_id}
      AND snapshot_date >= CURRENT_DATE - INTERVAL '{days} days'
    ORDER BY snapshot_date DESC
    """

    data = execute_sql(sql)

    # 获取项目名称
    project = execute_sql(f"SELECT name FROM dim_projects WHERE id = {project_id}")
    project_name = project[0]["name"] if project else f"Project #{project_id}"

    # 计算汇总统计
    if data:
        latest = data[0]
        total_new = sum(r.get("new_issues", 0) or 0 for r in data)
        total_closed = sum(r.get("closed_issues", 0) or 0 for r in data)
    else:
        latest = {}
        total_new = 0
        total_closed = 0

    # 渲染输出
    if output_format == "html":
        return render_html({
            "data": data,
            "summary": {
                "project_name": project_name,
                "total_issues": latest.get("total_issues", 0),
                "total_new": total_new,
                "total_closed": total_closed
            }
        }, title=f"{project_name} - 项目日报")

    elif output_format == "email":
        return render_mail({
            "data": data,
            "summary": {
                "project_name": project_name,
                "total_issues": latest.get("total_issues", 0),
                "total_new": total_new,
                "total_closed": total_closed
            }
        }, title=f"{project_name} - 项目日报")

    elif output_format == "markdown":
        md = f"# {project_name} - 项目日报 (最近{days}天)\\n\\n"
        md += f"- 问题总数：{latest.get('total_issues', 0)}\\n"
        md += f"- 新增：{total_new}\\n"
        md += f"- 关闭：{total_closed}\\n\\n"
        md += "| 日期 | 总数 | 新增 | 关闭 |\\n"
        md += "|------|------|------|------|\\n"
        for row in data:
            md += f"| {row.get('snapshot_date')} | {row.get('total_issues')} | {row.get('new_issues')} | {row.get('closed_issues')} |\\n"
        return md

    return {"data": data}
'''

save_redmine_report_template(
    code_content=template_code,
    description="项目日报报表 - 显示最近 N 天的问题统计",
    is_public=True,
    version_comment="初始版本"
)
```

## 工作流

### 工作流 1：从零开始开发报表

```python
# 步骤 1：探索可用数据
catalog = get_redmine_data_catalog(schema="dws")
print("可用表:", [t["table_name"] for t in catalog["tables"]])

# 步骤 2：搜索相关表
search = search_redmine_data_catalog(keyword="daily project")
print("推荐表:", search["matching_tables"])

# 步骤 3：查看表结构
sample_sql = "SELECT * FROM dws_project_daily_summary LIMIT 1"
sample_data = execute_redmine_sql_query(sample_sql)
print("字段:", list(sample_data["data"][0].keys()))

# 步骤 4：编写并测试 SQL
test_sql = """
SELECT snapshot_date, total_issues, new_issues, closed_issues
FROM dws_project_daily_summary
WHERE project_id = 176
  AND snapshot_date >= CURRENT_DATE - INTERVAL '7 days'
ORDER BY snapshot_date DESC
"""
result = execute_redmine_sql_query(test_sql)
print(f"返回 {result['row_count']} 行数据")

# 步骤 5：保存为模板
template = generate_template_code(result, "项目日报")
save_redmine_report_template(
    code_content=template,
    description="项目日报报表"
)
```

### 工作流 2：基于自然语言生成

```python
# 用户输入："我想看项目 176 最近 7 天的问题趋势"

# 自动解析意图
intent = "project_daily_trend"
entities = {
    "project_id": 176,
    "days": 7
}

# 推荐数据源
recommended_table = "dws_project_daily_summary"

# 生成 SQL
sql = f"""
SELECT
    snapshot_date as 日期，
    total_issues as 问题总数，
    new_issues as 新增，
    closed_issues as 关闭
FROM dws_project_daily_summary
WHERE project_id = {entities['project_id']}
  AND snapshot_date >= CURRENT_DATE - INTERVAL '{entities['days']} days'
ORDER BY snapshot_date
"""

# 执行并展示
result = execute_redmine_sql_query(sql)
display_chart(result, type="line", x="日期", y=["问题总数", "新增", "关闭"])
```

## 常用报表模板库

### 模板 1：项目日报
- **表**: `dws_project_daily_summary`
- **参数**: project_id, days
- **输出**: 每日问题统计趋势

### 模板 2：开发者效率
- **表**: `dwd_issues_full` + `dim_users`
- **参数**: months, project_id (可选)
- **输出**: 开发者问题关闭数排名

### 模板 3:Issue 状态分布
- **表**: `dwd_issues_full` + `dim_status`
- **参数**: project_id
- **输出**: 饼图展示各状态占比

### 模板 4：项目健康度
- **表**: `dws_project_health_daily`
- **参数**: project_id, days
- **输出**: 健康评分趋势

## 参考文档

- [数据仓库 Schema](./data-schema.md) - 完整表结构和字段说明
- [MCP 工具参考](./mcp-tools.md) - 报表工具 API
- [工作流示例](./workflows.md) - 报表开发工作流
