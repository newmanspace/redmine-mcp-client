---
name: test
description: 运行 Redmine MCP Client 的全量工具诊断测试
---

# 自动化诊断测试 (Test)

本技能负责对 Redmine MCP Client 及其关联的所有 MCP 工具执行全量诊断测试，确保功能连通性和数据交互正常。

## 前置约束
- 需要环境中已设置 `REDMINE_MCP_TOKEN` 环境变量（或手动在脚本中配置）。
- 确保 MCP Server（192.168.0.108:8000）处于运行状态。
- 测试结果会持久化到 `tests/diagnostic_results.json`。

## 测试命令

### 运行全量工具诊断
```bash
python3 tests/run_all_tests.py
```

### 查看测试结果
```bash
cat tests/diagnostic_results.json | jq .
```

## 失败处理策略
当测试执行过程中出现 `FAIL` 时，按以下分类排查：
1. **[CODE_BUG]**: 脚本执行出错，检查 Python 代码逻辑或 Traceback。
2. **[PERMISSION]**: 权限不足，检查对应的 Redmine 用户是否有执行该操作的权限。
3. **[VALIDATION]**: 参数验证失败，检查 MCP Schema 定义与实际传递的参数是否匹配。
4. **[INTERNAL]**: 网络或服务器内部错误，检查 MCP Server 是否在线及网络连通性。

## 测试结果解读
- ✅ **[PASS]**: 工具调用正常，返回预期内容。
- ❌ **[FAIL]**: 必须通过 `tests/diagnostic_results.json` 查看具体的错误详情并修复。

---
最后更新: 2026-03-28
