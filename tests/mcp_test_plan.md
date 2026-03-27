# Redmine MCP 全量接口测试方案 (v2.0)

本项目旨在对 Redmine MCP 服务器（http://192.168.0.107:8000/）提供的 **38 个核心接口** 进行覆盖率 100% 的连通性与功能测试。测试将以项目 **myCIM2+ DevOps (ID: 176)** 作为核心数据源。

## 测试目标
1. **全量覆盖**: 逐一验证 `mcp_redmine_` 前缀下的所有可用工具。
2. **深度测试报表系统**: 验证模板管理、版本控制及自动化执行能力。
3. **数据链路校验**: 确保 ODS -> DWD -> ADS 的数据仓库链路及 SQL 执行正常。
4. **异常归档**: 记录具体的代码缺陷（如导入缺失、函数未定义等）。

---

## 测试用例设计

### 1. 核心内容管理接口 (Redmine Content)
| 测试项 (Tool) | 测试内容 | 预期结果 |
| :--- | :--- | :--- |
| `list_redmine_projects` | 检索全量项目 | 成功返回 JSON 列表 (已验证: OK) |
| `list_my_redmine_issues`| 获取分配给我的任务 | 成功返回任务列表 |
| `search_redmine_issues` | 搜索项目 176 内的任务 | 成功返回搜索结果 |
| `get_redmine_issue` | 获取任务详情 (ID: 77867) | 成功返回任务描述及详情 |
| `create_redmine_issue` | 在项目 243 创建测试任务 | 验证写操作权限 |
| `update_redmine_issue` | 更新测试任务状态 | 验证写操作权限 |
| `get_redmine_wiki_page` | 获取 Wiki 页面 (Project 176) | 成功取得页面 Markdown/Textile 正文 |
| `create_redmine_wiki_page`| 创建测试 Wiki 页面 | 验证写操作权限 |
| `update_redmine_wiki_page`| 更新 Wiki 内容 | 验证写操作权限 |
| `search_entire_redmine` | 全局搜索 "DevOps" | 成功取得搜索合集 |
| `get_attachment_url` | 获取特定附件下载地址 | 验证存储服务连通性 |

### 2. ETL 与数据仓库接口 (ETL & Warehouse)
| 测试项 (Tool) | 测试内容 | 预期结果 |
| :--- | :--- | :--- |
| `get_etl_dashboard` | 获取监控面板数据 | 成功返回 (已验证: OK) |
| `get_etl_history` | 获取最近 10 条执行记录 | 验证历史流水查询 |
| `trigger_scheduled_sync`| 触发增量同步 (increment) | 验证任务调度权限 |
| `etl_project_backfill` | 针对特定项目执行回填 | 验证历史数据拉取 |
| `etl_project_rerun` | 重新运行特定项目 ETL | 验证数据修正功能 |
| `get_redmine_data_catalog`| 查询 `warehouse` 架构 | 成功返回表映射 (已验证: OK) |
| `search_data_catalog` | 搜索 `ods_issues` 相关列 | 验证元数据检索 (已验证: OK) |
| `execute_redmine_sql_query`| 执行复杂聚合 SQL | 成功返回数据 (已验证: OK) |

### 3. 报表与数据透视接口 (Reporting System) - *重点测试*
| 测试项 (Tool) | 测试内容 | 预期结果 |
| :--- | :--- | :--- |
| `list_report_templates` | 获取可用模板列表 | 已验证: OK |
| `get_report_template` | 获取“项目日报”源代码 | 验证模板逻辑读取 |
| `save_report_template` | 尝试保存一个测试 Python 模板 | 验证报表开发权限 |
| `run_report_template_now`| 手动触发一个已存在的模板 | 验证后端渲染能力 |
| `preview_report_template`| 预览“项目周报” (html/txt) | 验证转换器 (Converter) 正常 |
| `execute_report_template`| 获取“项目周报” Markdown | 成功输出格式化文本 (已验证: OK) |
| `get_template_versions` | 查询模板版本历史 | 验证版本快照功能 |
| `compare_template_versions`| 对比 V1 与 V2 的差异 | 验证 Diff 引擎正常 |
| `get_active_template_version`| 查看当前生产环境版本 | 验证版本标记 |
| `activate_template_version`| 切换模板到特定版本 | 验证发布流程 |
| `rollback_template_version`| 滚回到上一个版本 | 验证灾备机制 |

### 4. 订阅与推送接口 (Subscription & Delivery)
| 测试项 (Tool) | 测试内容 | 预期结果 |
| :--- | :--- | :--- |
| `list_my_subscriptions` | 获取当前用户的订阅列表 | 验证订阅配置读取 |
| `subscribe_project` | 订阅项目 176 的日报 (Email) | 验证订阅写入 |
| `subscribe_template` | 订阅特定报表模板 | 验证订阅关联 |
| `unsubscribe_project` | 取消对特定项目的订阅 | 验证清理逻辑 |
| `send_subscription_reports`| 手动触发订阅邮件发送 | 验证推送引擎 |
| `send_project_report_email`| 单次发送项目报告到指定邮箱 | 验证即时发送功能 |
| `get_scheduler_status` | 查看订阅调度器运行状态 | 验证 APScheduler 状态 |
| `test_email_service` | 发送测试邮件验证 SMTP | 验证邮件网关连通性 |

---

## 测试流程
1. **顺序执行**: 按照上述分类，从“基础治理”开始，最终到“订阅推送”。
2. **详细日志记录**: 针对每个工具记录：
    - 是否成功 (PASS/FAIL)
    - 报错信息 (Error Message)
    - 潜在原因分析
3. **成果输出**: 最终在 `redmine_mcp_health_report.md` 中进行总结。

---
