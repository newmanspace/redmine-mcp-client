---
name: release
description: 执行 Redmine MCP Client 的版本发布与打包流程
---

# 版本发布 (Release)

本技能负责执行 Redmine MCP Client 的版本发布流程，确保版本号同步更新并生成可分发的成果物（ZIP 包）。

## 发布流程 (Release Workflow)

### 1. 版本号确认 (Version Check)
确认本次发布的版本号遵循 `MAJOR.MINOR.PATCH` 规范。

**涉及文件及字段**:
- `scripts/package.sh` 中的 `VERSION` 变量。
- `.claude-plugin/plugin.json` 中的 `version` 字段。

---

### 2. 生成 Release Notes
在 `CHANGELOG.md` 中记录本次变更。

---

### 3. 发布前验证 (Pre-release Checklist)
**必须全部满足**:
- [ ] 运行全量诊断测试通过：`python3 tests/run_all_tests.py`
- [ ] 检查 `tests/diagnostic_results.json` 中无 Failure。
- [ ] 确保关键文件完整（参考 `scripts/package.sh` 中的 `REQUIRED_FILES`）。

---

### 4. 执行打包 (Execution)
使用打包脚本生成 ZIP 文件：

```bash
./scripts/package.sh
```

**产物验证**:
- 检查 `scripts/dist/` 目录下是否生成了对应的 `.zip` 文件。
- 验证 ZIP 包内容是否包含所有必需的插件文件。

---

### 5. Git Tag
```bash
git tag -a vX.Y.Z -m "Release version X.Y.Z"
git push origin vX.Y.Z
```

## 输出动作
1. **版本同步**：引导用户或自动更新 `package.sh` 和 `plugin.json`。
2. **运行测试**：执行诊断测试并展示概要。
3. **打包**：执行 `./scripts/package.sh`。
4. **结果报告**：展示生成的 ZIP 文件名和大小。

---
最后更新: 2026-03-28
 -U <user> -d <db> -f /docker-entrypoint-initdb.d/seed-xxx.sql

# 生产
ssh <host> "cat /path/to/seed-xxx.sql | docker exec -i <container> psql -U <user> -d <db>"
```

**检查项**:
- [ ] 基础数据已插入
- [ ] 数据字典已更新
- [ ] 无重复数据冲突

---

### 9. 应用部署 (Deploy Application)

**执行部署**:
```bash
./deploy/deploy.sh --release-prod
```

**部署后验证**:
- [ ] 健康检查通过：`curl http://localhost:8000/health`
- [ ] 容器正常运行：`docker compose ps`
- [ ] 日志无 ERROR：`docker compose logs -f redmine-mcp-server`
- [ ] MCP 工具调用正常
- [ ] 新功能验证通过

---

### 10. Git Tag 与 Release

**打 Tag**:
```bash
git tag -a vX.Y.Z -m "Release version X.Y.Z"
git push origin vX.Y.Z
```

**发布检查**:
- [ ] Git tag 已创建并推送
- [ ] GitHub Release 已创建（如适用）
- [ ] CHANGELOG.md 已推送

---

## 输出动作

触发 `/release` 技能后，将依次执行：

1. **版本确认** - 询问用户本次发布类型和版本号
2. **生成 Release Notes** - 输出 CHANGELOG 更新内容
3. **SQL 脚本检查** - 列出迁移脚本及生产执行命令
4. **配置文件检查** - 列出需更新的文件和当前版本号
5. **发布前验证** - 运行测试和检查清单
6. **SQL 迁移执行** - 执行数据库迁移脚本（本地 + 生产）
7. **配置文件更新** - 更新版本号和新增环境变量
8. **基础数据初始化** - 执行 seed 数据脚本（如有）
9. **等待用户 Approve** - 所有准备完成后等待确认
10. **应用部署** - 用户确认后执行部署
11. **Git Tag** - 打 tag 并推送

---

## ⛔ 红线约束

- **禁止跳过检查**: 任何一项检查不通过都不得继续
- **禁止自动推送**: Git push 和部署必须等待用户明确确认
- **执行顺序严格**: 必须按 SQL→配置→数据→应用 顺序执行
- **回滚预案**: 发布前必须确认回滚方案可用

---

## 回滚操作

```bash
# 停止当前容器
docker compose down

# 回退到上一个版本
git checkout HEAD~1 -- .
./deploy/deploy.sh
```
