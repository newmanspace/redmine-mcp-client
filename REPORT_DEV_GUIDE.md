# Redmine 报表开发最佳实践

本文档总结 Redmine AI Report Builder 的最佳实践和改进方案。

## 改进方案总结

### 1. 表结构理解能力增强

#### 新增工具调用策略

```python
# 步骤 1：获取完整数据目录（一次性获取所有 schema）
catalog = get_redmine_data_catalog(schema="warehouse", limit=200)

# 步骤 2：按需获取特定 schema 详情
dwd_tables = [t for t in catalog["tables"] if t["schema"] == "dwd"]
dws_tables = [t for t in catalog["tables"] if t["schema"] == "dws"]

# 步骤 3：搜索相关字段
search_result = search_redmine_data_catalog(keyword="issue", schema="warehouse")
```

#### 表结构缓存

在 `.claude/projects/-docker-redmine-mcp-client/memory/` 中缓存表结构信息：

```markdown
---
name: dws_project_daily_summary
description: 项目每日汇总表结构
type: reference
---

**表**: dws_project_daily_summary
**Schema**: dws
**用途**: 存储每个项目每日的问题统计数据

**字段**:
- id (bigint) - 主键
- project_id (integer) - 项目 ID → dim_projects.id
- snapshot_date (date) - 快照日期
- total_issues (integer) - 问题总数
- new_issues (integer) - 新增问题数
- closed_issues (integer) - 关闭问题数
- status_new/in_progress/resolved/closed - 按状态统计
- priority_immediate/urgent/high/normal/low - 按优先级统计

**推荐使用场景**:
- 项目日报
- 趋势分析
- 仪表盘展示
```

### 2. 智能推荐引擎

#### 根据报表类型推荐表

| 报表需求 | 推荐表 | 理由 |
|----------|--------|------|
| 项目日报/趋势 | `dws_project_daily_summary` | 预聚合，查询快 |
| 开发者效率 | `dwd_issues_full` + `dim_users` | 需要明细 + 用户信息 |
| Issue 状态分布 | `dwd_issues_full` + `dim_status` | 完整数据 + 状态名称 |
| 负载分析 | `dws_user_loading_daily` | 用户负载汇总 |
| 质量指标 | `ads_issue_metrics` | 预计算指标 |

#### JOIN 路径推荐

```
当查询需要多表关联时，自动推荐最优路径：

示例：开发者效率报表
┌─────────────────────┐
│  dwd_issues_full    │
│  (Issue 明细)        │
└─────────┬───────────┘
          │ assigned_to_id
          ▼
┌─────────────────────┐
│    dim_users        │
│  (用户维度)          │
└─────────────────────┘

推荐 SQL:
SELECT u.name, COUNT(i.id) as total
FROM dwd_issues_full i
LEFT JOIN dim_users u ON i.assigned_to_id = u.id
GROUP BY u.id, u.name
```

### 3. SQL 生成模板库

#### 模板 1：项目日报
```sql
-- 推荐指数：★★★★★
-- 适用场景：项目每日统计、趋势分析
SELECT
    snapshot_date,
    total_issues,
    new_issues,
    closed_issues,
    status_new,
    status_in_progress
FROM dws_project_daily_summary
WHERE project_id = :project_id
  AND snapshot_date >= CURRENT_DATE - INTERVAL :days
ORDER BY snapshot_date DESC;
```

#### 模板 2：开发者效率
```sql
-- 推荐指数：★★★★☆
-- 适用场景：团队效率评估、绩效考核
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
  AND i.created_on >= DATE_TRUNC('month', CURRENT_DATE - INTERVAL :months)
GROUP BY u.id, u.login, u.name
ORDER BY closed_issues DESC;
```

#### 模板 3：Issue 状态分布
```sql
-- 推荐指数：★★★★☆
-- 适用场景：项目健康度监控
SELECT
    s.name as status_name,
    COUNT(i.id) as issue_count,
    ROUND(COUNT(i.id) * 100.0 / SUM(COUNT(i.id)) OVER (), 2) as percentage
FROM dwd_issues_full i
LEFT JOIN dim_status s ON i.status_id = s.id
WHERE i.project_id = :project_id
GROUP BY s.id, s.name
ORDER BY issue_count DESC;
```

### 4. 模板创建自动化

#### 代码生成器

```python
def generate_template_code(table_name, report_type, params):
    """根据表名和报表类型自动生成模板代码"""

    templates = {
        "project_daily": PROJECT_DAILY_TEMPLATE,
        "developer_efficiency": DEVELOPER_EFFICIENCY_TEMPLATE,
        "issue_status": ISSUE_STATUS_TEMPLATE,
    }

    base_template = templates.get(report_type, DEFAULT_TEMPLATE)

    return base_template.format(
        table_name=table_name,
        params=params,
        title=f"{report_type.replace('_', ' ').title()} Report"
    )

# 使用示例
code = generate_template_code(
    table_name="dws_project_daily_summary",
    report_type="project_daily",
    params={"project_id": 176, "days": 7}
)

save_redmine_report_template(
    code_content=code,
    description="项目日报报表",
    is_public=True
)
```

### 5. 数据字典集成

#### 字段解释器

```python
def explain_field(table, field):
    """解释字段的业务含义"""

    data_dictionary = {
        "dws_project_daily_summary": {
            "total_issues": "截止当日的问题总数",
            "new_issues": "当日新增问题数",
            "closed_issues": "当日关闭问题数",
            "status_new": "当前状态为'新建'的问题数",
            "status_in_progress": "当前状态为'进行中'的问题数",
        },
        "dwd_issues_full": {
            "done_ratio": "完成百分比 (0-100)",
            "estimated_hours": "预估工时",
            "closed_on": "关闭时间戳",
        }
    }

    return data_dictionary.get(table, {}).get(field, "未知字段")
```

## 开发工作流改进

### 原有流程（需要 5 步）

1. 手动查询 `get_redmine_data_catalog` 获取表列表
2. 使用 `search_redmine_data_catalog` 搜索相关表
3. 执行 SQL 查看表结构
4. 手动编写 SQL 查询
5. 保存为模板

### 改进后流程（只需 2 步）

1. 自然语言描述需求（如"我想看项目 176 最近 7 天的问题趋势"）
2. 自动获取表结构 → 生成 SQL → 创建模板

### 实现逻辑

```python
async def build_report_from_natural_language(user_query):
    # 步骤 1：解析意图
    intent = parse_intent(user_query)
    # 示例输出：
    # {
    #     "type": "project_daily_trend",
    #     "entities": {"project_id": 176, "days": 7}
    # }

    # 步骤 2：推荐数据源
    recommended_table = recommend_table(intent["type"])
    # 示例输出："dws_project_daily_summary"

    # 步骤 3：获取表结构（如果需要）
    if recommended_table not in schema_cache:
        catalog = get_redmine_data_catalog(schema="dws")
        schema_cache[recommended_table] = get_table_schema(catalog, recommended_table)

    # 步骤 4：生成 SQL
    sql = generate_sql(intent, schema_cache[recommended_table])

    # 步骤 5：执行并返回
    result = execute_redmine_sql_query(sql)

    # 步骤 6：询问是否保存为模板
    if user_wants_to_save:
        template_code = generate_template_code(intent, sql)
        save_redmine_report_template(code_content=template_code)

    return result
```

## 新增参考文档

| 文档 | 用途 |
|------|------|
| [`references/data-schema.md`](./references/data-schema.md) | 完整数据仓库 Schema 参考 |
| [`SKILL-report-builder.md`](./SKILL-report-builder.md) | 报表开发专用 Skill |
| [`REPORT_DEV_GUIDE.md`](./REPORT_DEV_GUIDE.md) | 本文档 |

## 使用示例

### 示例 1：项目日报

**用户输入**: "生成项目 176 的最近 7 天日报"

**自动执行流程**:

```python
# 1. 推荐表
# → 推荐：dws_project_daily_summary

# 2. 获取表结构（如果缓存中没有）
catalog = get_redmine_data_catalog(schema="dws")

# 3. 生成 SQL
sql = """
SELECT
    snapshot_date,
    total_issues,
    new_issues,
    closed_issues
FROM dws_project_daily_summary
WHERE project_id = 176
  AND snapshot_date >= CURRENT_DATE - INTERVAL '7 days'
ORDER BY snapshot_date DESC
"""

# 4. 执行
result = execute_redmine_sql_query(sql)

# 5. 展示结果（Markdown 表格）
print(generate_markdown_table(result))
```

### 示例 2：开发者效率

**用户输入**: "查看最近 3 个月开发者的问题关闭数排名"

**自动执行流程**:

```python
# 1. 推荐表
# → 推荐：dwd_issues_full + dim_users

# 2. 生成 SQL
sql = """
SELECT
    u.login,
    u.name,
    COUNT(i.id) as closed_count
FROM dwd_issues_full i
LEFT JOIN dim_users u ON i.assigned_to_id = u.id
WHERE i.status_id = 5
  AND i.closed_on >= DATE_TRUNC('month', CURRENT_DATE - INTERVAL '3 months')
GROUP BY u.id, u.login, u.name
ORDER BY closed_count DESC
"""

# 3. 执行并展示
result = execute_redmine_sql_query(sql)
```

## 检查清单

在发布报表前，检查以下项目：

- [ ] 使用 DWS 层汇总表（如果可用）以获得更好性能
- [ ] 添加适当的日期范围过滤
- [ ] 处理 NULL 值（使用 COALESCE）
- [ ] 添加 LIMIT 防止结果过大
- [ ] 测试多格式输出（HTML/Email/Markdown）
- [ ] 添加模板参数支持（project_id, days 等）
- [ ] 编写模板描述和版本说明

---

**最后更新**: 2026-03-26
**版本**: 1.0.0
