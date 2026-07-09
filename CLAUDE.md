# CLAUDE.md — auto-test-framework 项目指引

## 项目概述
企业级接口自动化测试框架，pytest + requests 架构，PO 模式封装。
测试目标：mall 商城系统（演示环境 admin-api.macrozheng.com）

## 技术栈
- Python 3.10 + pytest + requests
- Allure 测试报告
- GitHub Actions CI/CD
- 数据驱动：YAML/JSON

## 目录结构
```
config/          环境配置（多环境切换 dev/test/prod）
test_data/       测试数据（YAML/JSON，与测试脚本分离）
core/            核心模块（api_client、context、data_loader）
auth/            认证策略（Bearer Token、Cookie、API Key）
api/             接口封装层（admin 后台、portal 前台）
tests/           测试用例（api 单接口、scenario 业务流程）
  scenario/actions  业务动作层（ProductActions）
utils/           工具类（logger、random_data、encrypt、retry）
scripts/         辅助脚本（run_tests、generate_report、lark_notify）
```

## 关键设计
- TestContext（core/context.py）：会话级上下文，存储 token 和跨接口数据
- ApiClient（core/api_client.py）：HTTP 客户端封装，支持认证策略切换
- Config（config/config_loader.py）：单例配置，优先读环境变量再读 YAML
- AdminAPIGroup / PortalAPIGroup：接口分组，在 conftest.py 注册
- ProductActions（tests/scenario/actions/product_actions.py）：业务动作层，封装 create/publish/unpublish/verify 等可复用步骤
- retry（utils/retry.py）：重试装饰器，网络波动时自动重试

## 敏感信息
- config/accounts.yaml 已加入 .gitignore，不提交到 Git
- CI 通过 GitHub Secrets 注入：ADMIN_BASE_URL、PORTAL_BASE_URL、ADMIN_USERNAME、ADMIN_PASSWORD

## 运行命令
```bash
pytest tests/                                    # 运行所有测试
pytest tests/api/admin/product/                  # 运行指定模块
pytest tests/scenario/                           # 运行业务流程测试
pytest tests/ -m smoke                           # 冒烟测试
pytest tests/ -n auto                            # 并行执行
python scripts/generate_report.py                # 生成 Allure 报告
```

## CI/CD
- GitHub Actions：.github/workflows/pytest.yml
- push/PR 到 master 自动触发
- CI 跑 smoke 冒烟测试（`pytest -m smoke`），只包含查询类接口（演示环境只读）
- allure-results 作为 artifact 上传（保留 30 天），本地 `allure serve` 查看
- 演示环境只有读权限，写入类测试（create/delete）会返回 500

## 注意事项
- allure-results 使用相对路径（pytest.ini + generate_report.py），基于项目根目录解析
- config_loader.py 支持环境变量覆盖，本地用 YAML，CI 用环境变量
