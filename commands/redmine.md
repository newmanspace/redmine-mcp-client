---
name: redmine
description: Redmine MCP client - access issues, wiki, projects, search, and reports
version: 1.1.0
---

# /redmine - Redmine MCP Command

## 使用方法

```
/redmine [command] [options]
```

## 可用子命令

### Issues

| 命令 | 描述 |
|------|------|
| `/redmine issues list` | 列出分配给我的问题 |
| `/redmine issues get <id>` | 获取指定问题详情 |
| `/redmine issues search <query>` | 搜索问题 |
| `/redmine issues create <project> <subject>` | 创建新问题 |
| `/redmine issues update <id> <fields>` | 更新问题 |

### Wiki

| 命令 | 描述 |
|------|------|
| `/redmine wiki get <project> <title>` | 获取 Wiki 页面 |
| `/redmine wiki create <project> <title> <text>` | 创建 Wiki 页面 |
| `/redmine wiki update <project> <title> <text>` | 更新 Wiki 页面 |

### Projects

| 命令 | 描述 |
|------|------|
| `/redmine projects list` | 列出所有项目 |
| `/redmine projects search <query>` | 搜索项目内问题 |

### Search

| 命令 | 描述 |
|------|------|
| `/redmine search <query>` | 全局搜索（Issue + Wiki） |
| `/redmine search issues <query>` | 仅搜索 Issue |
| `/redmine search wiki <query>` | 仅搜索 Wiki |

### Reports

| 命令 | 描述 |
|------|------|
| `/redmine reports catalog` | 查看数据仓库目录 |
| `/redmine reports search <keyword>` | 搜索表/字段 |
| `/redmine reports sql <query>` | 执行 SQL 查询 |
| `/redmine reports templates list` | 列出报表模板 |
| `/redmine reports templates preview <id>` | 预览模板 |
| `/redmine reports templates run <id>` | 执行模板 |
| `/redmine reports templates save <name> <code>` | 保存模板 |

### Subscriptions

| 命令 | 描述 |
|------|------|
| `/redmine subscriptions list` | 列出我的订阅 |
| `/redmine subscriptions add <template> <channel>` | 订阅模板 |
| `/redmine subscriptions remove <id>` | 取消订阅 |

### ETL

| 命令 | 描述 |
|------|------|
| `/redmine etl dashboard` | 查看 ETL 监控看板 |
| `/redmine etl history` | 查看 ETL 执行历史 |
| `/redmine etl backfill [project_ids]` | 回填历史数据 |
| `/redmine etl rerun [project_ids]` | 重新执行 ETL |

## 示例

### 查询我的问题
```
/redmine issues list limit=10
```

### 搜索特定问题
```
/redmine issues search "bug login" project_id=176
```

### 创建问题
```
/redmine issues create project_id=176 subject="Fix bug" description="Details..."
```

### 获取 Wiki 页面
```
/redmine wiki get project_id=176 title="Installation_Guide"
```

### 执行 SQL 查询
```
/redmine reports sql "SELECT * FROM dwd_issues_full LIMIT 10"
```

### 预览报表模板
```
/redmine reports templates preview tpl_dev_efficiency_weekly
```

## MCP 服务器状态

- **服务器地址**: `http://YOUR_SERVER_IP:8000/mcp`
- **服务器名称**: Redmine MCP Server
- **版本**: 1.26.0

## 可用工具

本插件通过 MCP 协议提供 38 个工具：

- **Issue 管理**: 5 个工具
- **Wiki 管理**: 3 个工具
- **项目管理**: 2 个工具
- **搜索**: 1 个工具
- **报表构建器**: 10 个工具
- **模板版本管理**: 5 个工具
- **订阅管理**: 4 个工具
- **ETL 管理**: 4 个工具

详细工具参考见 `skills/redmine-assistant/references/mcp-tools.md`
