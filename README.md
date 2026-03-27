# Redmine MCP Client

Claude Code 插件，用于与 Redmine MCP 服务器集成，提供 Issue 管理、Wiki 文档、项目搜索和 AI 报表构建功能。

## 功能特性

- **Issue 管理** - 创建/更新/查询/搜索 Redmine 问题
- **Wiki 管理** - 获取/创建/更新 Wiki 文档页面
- **项目管理** - 列出项目、搜索项目问题
- **全局搜索** - 跨 Issue 和 Wiki 搜索
- **AI 报表构建器** - 模板化报表生成（HTML/Email/Markdown）
- **订阅推送** - Email/DingTalk/Telegram 定期推送
- **ETL 管理** - 数据同步/ETL 监控

## 安装

详细安装说明请参考 [INSTALL.md](INSTALL.md)

### 快速开始

```bash
# 方式 1：临时加载（开发用）
claude --plugin-dir /docker/redmine-mcp-client

# 方式 2：永久安装
claude plugin marketplace add /docker/redmine-mcp-client
claude plugin install redmine-mcp-client
```

### 前置要求

- Node.js 18+
- Claude Code CLI: `npm install -g @anthropic-ai/claude-code`

## 配置

编辑 `.mcp.json` 文件配置 MCP 服务器地址：

```json
{
  "mcpServers": {
    "redmine": {
      "transport": {
        "type": "http",
        "url": "http://YOUR_SERVER_IP:8000/mcp"
      }
    }
  }
}
```

## 使用方法

### 命令入口

使用 `/redmine` 命令访问所有功能：

```
/redmine [command] [options]
```

### 常用命令

#### Issue 管理
```
/redmine issues list              # 列出我的问题
/redmine issues get <id>          # 获取 Issue 详情
/redmine issues search <query>    # 搜索 Issue
/redmine issues create ...        # 创建新 Issue
/redmine issues update ...        # 更新 Issue
```

#### Wiki 管理
```
/redmine wiki get <project> <title>    # 获取 Wiki 页面
/redmine wiki create ...               # 创建 Wiki 页面
/redmine wiki update ...               # 更新 Wiki 页面
```

#### 搜索
```
/redmine search <query>                # 全局搜索
/redmine search issues <query>         # 仅搜索 Issue
/redmine search wiki <query>           # 仅搜索 Wiki
```

#### 报表
```
/redmine reports catalog               # 查看数据目录
/redmine reports sql <query>           # 执行 SQL
/redmine reports templates list        # 列出模板
/redmine reports templates preview <id> # 预览模板
```

### 自动 Skill

`redmine-assistant` Skill 会在以下场景自动激活：

- "列出我的问题"
- "创建一个新的 Issue"
- "搜索 Redmine 中的 bug"
- "获取 Wiki 页面"
- "生成效率报表"
- "订阅周报推送"

## 可用的 MCP 工具

本插件通过 MCP 协议提供 38 个工具：

| 类别 | 工具数量 |
|------|----------|
| Issue 管理 | 5 |
| Wiki 管理 | 3 |
| 项目管理 | 2 |
| 全局搜索 | 1 |
| 报表构建器 | 10 |
| 模板版本管理 | 5 |
| 订阅管理 | 4 |
| ETL 管理 | 4 |

详细工具参考见 [skills/redmine-assistant/references/mcp-tools.md](skills/redmine-assistant/references/mcp-tools.md)

## 项目结构

```
redmine-mcp-client/
├── .claude-plugin/
│   └── plugin.json           # 插件清单
├── .mcp.json                 # MCP 服务器配置
├── commands/
│   └── redmine.md            # /redmine 命令
├── skills/
│   └── redmine-assistant/
│       ├── SKILL.md          # 自动触发技能
│       ├── references/
│       │   ├── mcp-tools.md  # 工具参考
│       │   └── workflows.md  # 工作流示例
│       └── examples/         # 示例代码
└── README.md
```

## 依赖

- Claude Code CLI
- Redmine MCP Server (运行在 http://YOUR_SERVER_IP:8000)
- Redmine 实例 (3.3.0+ 推荐)

## 开发

### 测试插件

```bash
# 方式 1：临时加载插件目录
claude --plugin-dir /docker/redmine-mcp-client

# 方式 2：安装后测试
/redmine projects list
/redmine issues list

# 测试 Skill 自动触发
"列出我所有的 Issue"
```

### 调试 MCP 连接

```bash
# 检查 MCP 服务器状态
curl http://YOUR_SERVER_IP:8000/health

# 测试 MCP 端点
curl -X POST http://YOUR_SERVER_IP:8000/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize"}'
```

## 许可证

MIT License

## 相关项目

- [Redmine MCP Server](https://github.com/newmanspace/redmine-mcp-server) - Redmine MCP 服务器实现
