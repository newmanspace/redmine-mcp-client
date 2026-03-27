# Redmine 数据仓库 Schema 参考

本文档提供数据仓库完整表结构、字段说明和表关系，帮助快速开发报表。

## Schema 层级

| Schema | 层级 | 描述 | 用途 |
|--------|------|------|------|
| `ods` | 原始数据层 | 与 Redmine API 同步的原始数据 | 数据源 |
| `dwd` | 明细数据层 | 清洗、标准化后的明细数据 | 查询分析 |
| `dws` | 汇总数据层 | 按主题聚合的汇总数据 | 报表展示 |
| `ads` | 应用数据层 | 面向特定应用的指标数据 | 定制化报表 |
| `dim` | 维度数据层 | 维度表（用户、项目等） | JOIN 查询 |

---

## 核心表结构

### ODS 层 - 原始数据

#### ods_issues
```sql
-- Redmine Issue 原始数据
id, project_id, tracker_id, status_id, priority_id, author_id, assigned_to_id,
subject, description, due_date, start_date, estimated_hours, total_estimated_hours,
done_ratio, category_id, fixed_version_id, parent_id, root_id, lock_version,
created_on, updated_on, closed_on
```

#### ods_projects
```sql
-- 项目原始数据
id, name, identifier, description, status, is_public, created_on, updated_on
```

#### ods_users
```sql
-- 用户原始数据
id, login, firstname, lastname, mail, admin, status, last_login_on, created_on
```

---

### DWD 层 - 明细数据

#### dwd_issues_full
```sql
-- Issue 完整明细表（推荐用于复杂查询）
id, project_id, tracker_id, status_id, priority_id,
subject, description, assigned_to_id, author_id,
due_date, start_date, estimated_hours, total_estimated_hours,
created_on, updated_on, closed_on, done_ratio
```

**字段说明**:
| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | bigint | Issue ID |
| `project_id` | integer | 项目 ID |
| `tracker_id` | integer | 跟踪类型 (1=Bug, 2=功能，3=任务...) |
| `status_id` | integer | 状态 (1=新建，2=进行中，3=已解决，4=已关闭，5=已完成) |
| `priority_id` | integer | 优先级 (1=低，2=普通，3=高，4=紧急，5=最高) |
| `assigned_to_id` | integer | 指派人 ID |
| `author_id` | integer | 作者 ID |
| `estimated_hours` | numeric | 预估工时 |
| `done_ratio` | integer | 完成百分比 (0-100) |

#### dwd_issue_daily_snapshot
```sql
-- Issue 每日快照表（用于趋势分析）
issue_id, snapshot_date, status_id, done_ratio, assigned_to_id, ...
```

---

### DWS 层 - 汇总数据

#### dws_project_daily_summary
```sql
-- 项目每日汇总表（推荐用于项目报表）
id, project_id, snapshot_date,
total_issues, new_issues, closed_issues,
status_new, status_in_progress, status_resolved, status_closed,
priority_immediate, priority_urgent, priority_high, priority_normal, priority_low,
created_at_snapshot, updated_issues
```

**使用示例**:
```sql
-- 获取项目 176 最近 7 天的汇总数据
SELECT * FROM dws_project_daily_summary
WHERE project_id = 176
  AND snapshot_date >= CURRENT_DATE - INTERVAL '7 days'
ORDER BY snapshot_date DESC;
```

#### dws_project_weekly_summary
```sql
-- 项目每周汇总
project_id, snapshot_week, total_issues, new_issues, closed_issues, ...
```

#### dws_project_monthly_summary
```sql
-- 项目每月汇总
project_id, snapshot_month, total_issues, new_issues, closed_issues, ...
```

#### dws_issue_contributor_summary
```sql
-- 贡献者汇总表
user_id, project_id, period, issues_created, issues_closed, issues_updated
```

#### dws_user_loading_daily
```sql
-- 用户每日负载
user_id, snapshot_date, assigned_issues, completed_issues, total_hours
```

#### dws_user_progress_daily
```sql
-- 用户每日进度
user_id, snapshot_date, issues_done, done_ratio_change
```

---

### ADS 层 - 应用数据

#### ads_issue_metrics
```sql
-- Issue 指标表
project_id, metric_date,
avg_resolution_days, reopen_rate, on_time_rate, ...
```

#### ads_user_stats
```sql
-- 用户统计表
user_id, period, efficiency_score, quality_score, workload_index
```

---

### DIM 层 - 维度表

#### dim_users
```sql
-- 用户维度表
id, login, name, email, department, role, is_active
```

#### dim_projects
```sql
-- 项目维度表
id, name, identifier, parent_id, status, created_date
```

#### dim_trackers
```sql
-- 跟踪类型维度表
id, name, is_default, position
```

#### dim_status
```sql
-- 状态维度表
id, name, is_closed, color
```

---

## 表关系图

```
dwd_issues_full
├── JOIN dim_users ON assigned_to_id = dim_users.id
├── JOIN dim_users ON author_id = dim_users.id
├── JOIN dim_projects ON project_id = dim_projects.id
├── JOIN dim_trackers ON tracker_id = dim_trackers.id
└── JOIN dim_status ON status_id = dim_status.id

dws_project_daily_summary
├── JOIN dim_projects ON project_id = dim_projects.id
└── (无需其他 JOIN，已预聚合)

dws_user_loading_daily
├── JOIN dim_users ON user_id = dim_users.id
└── JOIN dwd_issues_full ON assigned_to_id = user_id
```

---

## 常用报表 SQL 模板

### 1. 项目效率报表
```sql
SELECT
    p.name as project_name,
    COUNT(i.id) as total_issues,
    COUNT(CASE WHEN i.status_id = 5 THEN 1 END) as closed_issues,
    AVG(i.estimated_hours) as avg_hours,
    AVG(i.done_ratio) as avg_completion
FROM dwd_issues_full i
LEFT JOIN dim_projects p ON i.project_id = p.id
WHERE i.created_on >= :start_date
  AND i.created_on < :end_date
GROUP BY p.id, p.name
ORDER BY closed_issues DESC;
```

### 2. 开发者效率报表
```sql
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
  AND i.created_on >= :start_date
GROUP BY u.id, u.login, u.name
ORDER BY closed_issues DESC;
```

### 3. 项目趋势报表（使用 DWS 层）
```sql
SELECT
    snapshot_date,
    total_issues,
    new_issues,
    closed_issues,
    status_new,
    status_in_progress
FROM dws_project_daily_summary
WHERE project_id = :project_id
  AND snapshot_date >= :start_date
ORDER BY snapshot_date;
```

### 4. Issue 状态分布
```sql
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

---

## 数据质量提示

1. **时间字段**: 所有时间字段均为 `timestamp` 或 `date` 类型，可直接使用日期函数
2. **NULL 值**: 聚合查询时使用 `COALESCE()` 处理 NULL
3. **去重**: `dwd_issues_full` 可能有重复记录，使用 `DISTINCT` 或 `GROUP BY`
4. **性能**: 优先使用 DWS 层汇总表，避免全表扫描

---

## 快速探索命令

```sql
-- 查看表行数
SELECT
    schemaname,
    tablename,
    n_tup_ins as row_count
FROM pg_stat_user_tables
WHERE schemaname IN ('dwd', 'dws', 'ads', 'dim')
ORDER BY n_tup_ins DESC;

-- 查看表列
SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_schema = 'dwd'
  AND table_name = 'issues_full'
ORDER BY ordinal_position;

-- 查看外键关系
SELECT
    tc.table_name,
    kcu.column_name,
    ccu.table_name AS foreign_table_name,
    ccu.column_name AS foreign_column_name
FROM information_schema.table_constraints AS tc
JOIN information_schema.key_column_usage AS kcu
  ON tc.constraint_name = kcu.constraint_name
JOIN information_schema.constraint_column_usage AS ccu
  ON ccu.constraint_name = tc.constraint_name
WHERE tc.constraint_type = 'FOREIGN KEY';
```
