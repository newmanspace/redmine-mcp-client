# Redmine MCP Client 安装指南

本文档提供详细的安装和配置说明。

## 前置要求

1. **Node.js 18+**
   ```bash
   node --version  # 应显示 v18.x.x 或更高
   ```

2. **Claude Code CLI**
   ```bash
   npm install -g @anthropic-ai/claude-code
   ```

3. **MCP 服务器访问权限**
   - 确保可以访问 `http://YOUR_SERVER_IP:8000/mcp`
   - 如需修改服务器地址，编辑 `.mcp.json` 文件

---

## 安装方式

### 方式 1：本地目录加载（推荐开发使用）

**优点**：修改代码后立即生效，无需重新安装
**缺点**：每次启动需要指定参数

```bash
# 启动时加载插件
claude --plugin-dir /docker/redmine-mcp-client

# 或者创建别名方便使用
alias redmine='claude --plugin-dir /docker/redmine-mcp-client'
redmine  # 启动并自动加载插件
```

---

### 方式 2：添加为本地市场（永久安装）

**优点**：一次安装，永久使用
**缺点**：修改代码后需要重新安装

```bash
# 1. 添加本地市场
claude plugin marketplace add /docker/redmine-mcp-client

# 2. 安装插件
claude plugin install redmine-mcp-client

# 3. 验证安装
claude plugin list

# 4. 启动 Claude Code
claude
# 然后输入：/redmine projects list
```

---

### 方式 3：打包分发（用于其他客户端）

**适用场景**：将插件分发给团队成员或其他客户端（如 OpenClaw）

#### 步骤 1：打包

```bash
cd /docker/redmine-mcp-client

# 使用打包脚本（推荐）
./scripts/package.sh

# 或者手动打包
zip -r redmine-mcp-client.zip \
    .claude-plugin/ \
    commands/ \
    skills/ \
    .mcp.json \
    README.md \
    CLAUDE.md
```

#### 步骤 2：分发

将生成的 `redmine-mcp-client.zip` 文件发送给目标用户。

#### 步骤 3：安装（接收方）

```bash
# 解压 ZIP 包
unzip redmine-mcp-client.zip -d ~/redmine-mcp-client

# 添加为本地市场
claude plugin marketplace add ~/redmine-mcp-client

# 安装插件
claude plugin install redmine-mcp-client
```

---

## 配置

### 修改 MCP 服务器地址

编辑 `.mcp.json` 文件：

```json
{
  "mcpServers": {
    "redmine": {
      "transport": {
        "type": "http",
        "url": "http://YOUR_SERVER:PORT/mcp"
      }
    }
  }
}
```

### 配置环境变量（可选）

某些环境可能需要设置代理或认证：

```bash
# 如果需要 HTTP 代理
export HTTP_PROXY=http://proxy.example.com:8080
export HTTPS_PROXY=http://proxy.example.com:8080

# 如果需要 API Key
export REDMINE_API_KEY=your_api_key_here
```

---

## 验证安装

### 1. 检查插件状态

```bash
claude plugin list
```

应显示 `redmine-mcp-client` 在已安装插件列表中。

### 2. 测试基本命令

启动 Claude Code 后，输入以下命令：

```
/redmine projects list
```

预期输出：项目列表

### 3. 测试 Skill 自动触发

输入自然语言请求：

```
列出我的问题
```

预期：自动激活 `redmine-assistant` skill 并调用 MCP 工具

---

## 常见问题

### Q: "Plugin not found in any configured marketplace"

**原因**：尝试直接安装 ZIP 文件而非目录

**解决方案**：
```bash
# 先解压
unzip redmine-mcp-client.zip -d ~/redmine-mcp-client

# 添加市场
claude plugin marketplace add ~/redmine-mcp-client

# 安装
claude plugin install redmine-mcp-client
```

### Q: "MCP server requires network access approval"

**原因**：Claude Code 默认限制网络访问

**解决方案**：
- 在交互模式下来自批准网络请求
- 或在沙盒环境中使用 `--dangerously-skip-permissions`（仅信任环境）

### Q: "Failed to connect to MCP server"

**原因**：MCP 服务器未运行或不可达

**解决方案**：
```bash
# 检查服务器状态
curl http://YOUR_SERVER_IP:8000/health

# 如果服务器未运行，启动它
# （参考 Redmine MCP Server 的启动说明）
```

---

## 卸载

```bash
# 禁用插件
claude plugin disable redmine-mcp-client

# 卸载插件
claude plugin uninstall redmine-mcp-client

# 移除市场源
claude plugin marketplace remove redmine-mcp-client
```

---

## 更新

```bash
# 如果使用 Git 安装
cd ~/redmine-mcp-client
git pull

# 如果使用 ZIP 包安装
# 重新执行安装步骤
```
