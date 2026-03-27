# 项目业务领域与开发规范指南

本指南明确了本项目（Redmine MCP Server）的核心业务矩阵与开发防呆限制。

## 项目功能领域描述 (Core Features)
本节明确了项目的四大核心业务能力。在进行系统修改或新增需求时，必须围绕以下功能矩阵展开：
1. **Redmine 业务管理**：直接与上游交互，管理 Issues、Wiki 等资源的增删改查。
2. **ETL 数仓同步引擎**：负责将 Redmine 原始数据全量/增量同步至本地的 PostgreSQL 数据仓库。
3. **数据清洗与分析平台**：实现项目状态统计、工作量排行、特定贡献者报表分析等 BI（商业智能）能力。
4. **MCP 桥接与工具化**：遵循 Python 和 MCP 规范，将上述所有操作封装为大模型可调用的工具接口。

## 语言要求
- **代码、注释、docstring、日志、标识符**：必须使用**英文**。
- **与用户的交互（包括向控制台或提问）**：必须使用**中文**。

## 代码风格与静态检查
- **Python 代码风格**：所有 Python 代码必须符合 `ruff` 的格式化与静态检查规范，特别是关于 Import 排序（`I001`）的要求，必须放在模块顶部统一引入。建议在代码提交或 PR 之前执行 `ruff check --fix .` 予以自动修复。
- **导入完整性检查**：在修改或新增 MCP 工具时，必须确保所有调用的函数都已正确导入。检查清单：
  - `handle_redmine_error`（装饰器）和 `handle_exception`（直接调用）是否都导入了？
  - 使用了 `logging` 模块是否导入了 `import logging`？
  - 使用了 `datetime`、`json` 等标准库是否导入了？
  - **ETL Task Consistency**: All task functions in `dws_tasks.py` MUST match the names used in `scheduler.py` (e.g., `transform_issue_contributors`).
- **Report Module Naming**: All report-related modules and files SHOULD use the `rpt_` prefix (e.g., `rpt_html_templates.py`, `rpt_generation_service.py`).
- **Defined vs. Hardcoded Reports**: New report logic SHOULD be implemented as "Defined Reports" (database templates) instead of hardcoding SQL in service methods.
  - 使用了 `_issue_to_dict`、`_resource_to_dict` 等辅助函数是否定义了或从 `infrastructure.converters` 导入了？
  - **辅助函数定义**：如使用 `IssueConverter.to_dict()` 等转换器类，需编写简单的包装函数如 `def _issue_to_dict(issue): return IssueConverter.to_dict(issue)` 以保持代码一致性。
- **Starlette 路由注册**：在为 Starlette 应用对象添加补充 HTTP 接口（如 debug、health 等）时，应优先使用 `app.add_route(path, handler, methods=[...])` 而非 `@app.route` 装饰器，以确保在不同环境和初始化状态下的最大兼容性。

## Git 操作红线
- **绝对禁止自动提交**：任何情况下不得在未经用户明确同意时执行 `git commit` 或 `git push` 命令。所有代码变更只在本地工作区完成。

## 部署规范 (Deploy Governance)
- **部署前检查清单**:
  - [ ] 所有 `pytest` 测试通过（零失败）
  - [ ] `.env` 配置确认正确（`REDMINE_URL`, `REDMINE_API_KEY`, `WAREHOUSE_DB_*`）
  - [ ] 数据库迁移脚本已确认（`deploy/init-scripts/v*.sql`）
  - [ ] `pyproject.toml` 变更同步到 `uv.lock`
- **本地部署**: `./deploy/deploy.sh --force-rebuild`
- **生产部署**: `./deploy/deploy.sh --release-prod`（需先配置 SSH 免密到 redmine-remote）
- **部署后验证**: 必须执行健康检查 `curl http://localhost:8000/health` 并查看日志

## 数据库迁移规范 (Database Migration)
- **init-scripts 限制**: `deploy/init-scripts/` 目录中的 SQL 脚本**仅在数据库首次初始化时执行**，已有数据库不会自动执行新增的迁移脚本
- **迁移执行流程** (自 Issue-046 起):
  1. 新增迁移脚本必须命名为 `v<主版本>.<次版本>.<修订版本>_<描述>.sql`（如 `v0.21.0_add_next_send_at.sql`）
  2. 部署后**必须手动执行迁移**：
     - 本地：`docker compose exec warehouse-db psql -U redmine_warehouse -d redmine_warehouse -f /docker-entrypoint-initdb.d/vXXX.sql`
     - 生产：`ssh redmine-remote "cat /docker/redmine-mcp-server/deploy/init-scripts/vXXX.sql | docker exec -i redmine-mcp-warehouse-db psql -U redmine_warehouse -d redmine_warehouse"`
  3. 执行后**必须重启应用容器**以加载新代码：`docker compose restart redmine-mcp-server`
- **改进建议**: 未来应引入迁移管理工具（如 `alembic` 或 `flyway`）实现自动迁移检测与执行

## 数仓分层与数据流向
该项目具有严格的 PostgreSQL 数仓分层机制，任何分析脚本、SQL 工具必须按流向执行，**禁止跨层调用**：
- **ODS** -> **DWD** -> **DWS** -> **ADS**
- ❌ 不要跳过 ODS 直接在 DWD 计算；
- ❌ 不要从 ODS 或 DWD 提取数据供应用层(ADS)直接使用。

## MCP 工具与安全开发规范
- **命名**：`mcp` 工具命名采用 `<verb>_redmine_<noun>` 格式。
- **配置与安全**：API Key 等敏感数据一律从环境变量读取，绝不可硬编码。
- **数据库查询**：所有基于 Python 或其他脚本的 SQL 执行操作必须使用参数化机制防止注入。
- **SQL NULL Handling**: When using parameterization with optional filters (e.g., `project_id`), ALWAYS handle `NULL` cases explicitly in the SQL (using `(%s IS NULL OR column = %s)`) or use conditional Python logic to branch different SQL statements. Never use `WHERE column = %s` when `%s` can be `None`, as `column = NULL` is always false in SQL and will not match any rows.
- **测试覆盖率**：改动或新增模块需确保通过 `pytest` 测试，核心覆盖率要求在 80% 以上。
- **审计日志**：所有使用 `@mcp.tool()` 定义的工具必须同步添加 `@mcp_tool_audit(name, category)` 装饰器，确保所有调用均被记录至 `logs/mcp-audit.log`。
- **任务命名一致性**：所有在 `redmine_mcp_server.scheduler` 中注册的任务函数，其定义的函数名必须与调度层注册时的调用名称完全一致。

## MCP 分层架构规范 (自 refactor-001 起生效)
- **MCP 工具层** (`mcp/tools/`):
  - 只保留 `@mcp.tool()` 装饰的接口函数
  - 单层函数不得超过 50 行（业务逻辑必须下沉到服务层）
  - 工具文件按功能域组织，禁止跨域代码混杂
- **服务层** (`*/services/`):
  - 所有业务逻辑必须位于服务层
  - Redmine 业务逻辑统一放入 `redmine/services/`
  - ETL/数仓逻辑位于 `dws/services/`
  - 报表逻辑位于 `rpt/services/`
- **文件归类**:
  - 工具文件行数建议 < 500 行
  - 函数移动需同步更新 `mcp/tools/__init__.py` 导入
- **Code Review 检查项**:
  - [ ] MCP 工具层函数是否只包含接口注册，不包含业务逻辑？
  - [ ] 业务逻辑是否已下沉到对应的服务层？
  - [ ] 文件归类是否正确（按功能域组织）？
  - [ ] 工具文件行数是否合理？

## 代码复用与 DRY 原则 (自 Issue-047 起生效)
- **重复代码检测**: 当同一段逻辑在代码中出现 **2 次或以上** 时，必须提取为独立函数或工具方法。
- **提取时机**: 在写第二遍相似代码时，立即停下来思考是否可以复用已有函数。
- **工具函数命名**: 模块内私有工具函数使用 `_` 前缀（如 `_calculate_next_send_at`），公共工具函数放入 `utils.py` 或 `infrastructure/`。
- **函数提取标准**:
  - 代码重复出现 2 次或以上
  - 逻辑复杂超过 10 行
  - 具有独立功能可复用
  - 可编写单元测试
- **Docstring 要求**: 提取的工具函数必须包含完整的 docstring，描述功能、参数和返回值。
- **分层职责**:
  - **Repository 层**: 只负责 CRUD 操作，不包含业务逻辑
  - **Service 层**: 负责业务逻辑和计算（如 `_calculate_next_send_at`）
- **Code Review 检查项**:
  - [ ] 是否存在重复代码块（超过 5 行相似逻辑）？
  - [ ] 重复逻辑是否已提取为公共函数？
  - [ ] 工具函数是否有完整的 docstring？
  - [ ] Repository 层是否包含业务逻辑（应下沉到 Service 层）？
 
## 核心能力下沉规范 (Core Infrastructure Placement)
- **基础能力定义**：所有与业务领域（Redmine, ETL, Stats）无关的通用技术能力，如 **Email 发送**、**Redis/Cache**、**Message Queue**、**HTTP Client 封装** 等，必须放置在 `infrastructure/` 目录下。
- **调用关系**：业务服务层（`*/services/`）应调用 `infrastructure/` 中的通用接口，严禁将此类底层实现逻辑直接混合在业务服务代码中。
- **解耦要求**：基础设施层代码不应感知具体的业务报表格式或业务实体，应只负责数据的传输或存储。

## 文档与缺陷排查治理 (Documentation & Issue Governance)
- **新增功能 (Feature)**：开发任何新功能前，必须事先编写 Feature 文档，并集中存放在 `docs/development/features/` 目录下。
- **缺陷修复 (Bug/Issue)**：一旦出现问题并在修改代码前，**一定必须先提交 Issue Report**，将其记录在 `docs/development/issues/` 目录下。
- **防呆闭环 (Mitigation)**：每一份 Issue Report 在制定规避措施时，不能止步于代码修复，**必须**包含向 `.agents/rules.md` 增加约束法则，或去完善 `.agents/workflows/` 工作流的防御卡点动作。
- **绝对从属**：上述所有新增的 Feature 与 Issue 文档，在编写与存放时**严禁违反** `docs/development/issues/README.md` 与 `docs/development/features/README.md` 里面所描述的排版要求和流转要求。
- **文档命名规范**：除项目与技能根目录的主入口文件强制全大写（如 `README.md`、`SKILL.md`）以外，所有常规技术文档（如 `summary.md`、`issue-xxx.md`）一律**强制前缀小写**。后缀描述部分主要推荐小写和 kebab-case 结合的风格，但允许保留特定的英文缩略词或专有名词的大写。

## 重构规范 (Refactor Governance)
- **先立案后重构**: 重构前必须创建 `docs/development/refactoring/REFACTOR-XXX-*.md` 文档。
- **测试先行**: 重构前必须确保目标模块测试覆盖率 >80%。
- **分层顺序**: 遵循 Repository→Service→API→MCP Tools 自下而上顺序。
- **审查闭环**: 重构完成后必须通过 `refactor-review` 技能审查。

## Workflow 使用规范
| Workflow | 触发命令 | 使用场景 |
|----------|----------|----------|
| Feature | `/feature` | 开发全新业务模块或独立接口 |
| Issue | `/issue` | 修复线上 Bug、报错或功能异常 |
| Refactor | `/refactor` | 清理技术债务、优化架构、消除代码坏味道 |