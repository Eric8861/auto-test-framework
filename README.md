# 企业级接口自动化测试框架

基于 pytest 的前后台接口自动化测试框架，支持数据驱动、上下文管理、多环境切换。

## 目录结构

```
auto-test-framework/
├── config/                     # 环境配置
│   ├── config.yaml            # 主配置（预留）
│   ├── config_loader.py        # 配置加载器
│   ├── env/                   # 多环境配置
│   │   ├── dev.yaml          # 开发环境
│   │   ├── test.yaml         # 测试环境（默认）
│   │   └── prod.yaml         # 生产环境
│   └── accounts.yaml          # 测试账号（敏感信息）
│
├── test_data/                  # 测试数据（与测试脚本分离）
│   ├── admin/                # 后台测试数据
│   │   └── product/
│   │       ├── create.yaml   # 商品创建测试数据
│   │       └── list.yaml     # 商品列表测试数据
│   ├── portal/               # 前台测试数据
│   │   └── product/
│   │       └── detail.yaml
│   └── scenario/             # 业务流程测试数据
│       └── product_lifecycle.json
│
├── core/                      # 核心模块
│   ├── api_client.py        # HTTP 客户端封装
│   ├── context.py           # 测试上下文（存储 token 和跨接口数据）
│   └── data_loader.py       # YAML/JSON 数据加载器
│
├── auth/                      # 认证策略（可扩展）
│   ├── base.py              # 认证基类
│   ├── bearer_token.py      # Bearer Token 认证
│   ├── cookie_auth.py       # Cookie 认证
│   └── api_key.py           # API Key 认证
│
├── api/                       # 接口封装层
│   ├── base.py              # API 基类（预留）
│   ├── admin/               # 后台接口
│   │   ├── auth.py         # 登录认证
│   │   ├── product.py      # 商品管理
│   │   └── order.py        # 订单管理
│   └── portal/             # 前台接口
│       ├── auth.py
│       ├── product.py
│       └── order.py
│
├── tests/                     # 测试用例
│   ├── conftest.py         # pytest fixtures（会话级上下文、API客户端等）
│   ├── api/               # 单接口测试
│   │   ├── admin/
│   │   │   └── product/
│   │   │       ├── test_product_create.py
│   │   │       └── test_product_list.py
│   │   └── portal/
│   │       └── product/
│   │           └── test_product_detail.py
│   └── scenario/           # 业务流程测试
│       └── test_product_lifecycle.py
│
├── utils/                    # 工具类
│   ├── logger.py           # 日志工具
│   ├── random_data.py      # 随机数据生成
│   └── encrypt.py         # 加密工具
│
├── scripts/                 # 辅助脚本
│   ├── run_tests.py        # 测试运行脚本
│   ├── generate_report.py   # Allure 报告生成
│   └── lark_notify.py      # Lark 通知
│
├── requirements.txt          # 依赖列表
├── pytest.ini              # pytest 配置
└── README.md
```

---

## 一、核心概念与执行流程

### 1.1 测试上下文 (TestContext)

`core/context.py` 存储跨接口共享的数据：

```python
@dataclass
class TestContext:
    admin_token: str = None      # 后台 token
    portal_token: str = None     # 前台 token
    _data: dict = field(default_factory=dict)  # 业务数据

    def set_product_id(self, id): ...
    def get_product_id(self): ...
    def set(self, key, value): ...
    def get(self, key, default=None): ...
```

**作用**：在业务流程测试中，接口 A 创建的数据（如商品ID）需要传递给接口 B 使用。

### 1.2 执行流程图

```
┌─────────────────────────────────────────────────────────────────┐
│                         pytest 启动                              │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│  tests/conftest.py                                              │
│  1. scope="session" 的 fixtures 只执行一次                      │
│  2. 创建 TestContext（会话级上下文）                            │
│  3. 创建 ApiClient（HTTP 客户端）                                │
│  4. 创建 AdminAPIGroup / PortalAPIGroup（接口封装组）            │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│  测试用例执行                                                   │
│  fixtures/function 级 fixtures（每次测试前执行）                  │
│  └── admin_logged_in: 确保已登录                                │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│  单接口测试 (tests/api/admin/product/test_product_create.py)     │
│  ├── DataLoader 加载 YAML 测试数据                               │
│  ├── @pytest.mark.parametrize 驱动多组数据                      │
│  └── API 方法返回 dict，测试用例直接断言                         │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│  业务流程测试 (tests/scenario/test_product_lifecycle.py)         │
│  ├── Context 存储 product_id                                    │
│  ├── 后台创建商品 → 存储 ID                                     │
│  ├── 前台查询商品 → 使用 ID                                     │
│  └── teardown 清理测试数据                                      │
└─────────────────────────────────────────────────────────────────┘
```

---

## 二、如何添加新接口

### 2.1 步骤一：创建接口封装

在 `api/admin/` 或 `api/portal/` 下创建文件：

```python
# api/admin/category.py
from core.api_client import ApiClient
from core.context import TestContext

class AdminCategoryAPI:
    """后台分类管理接口"""

    def __init__(self, client: ApiClient, context: TestContext):
        self.client = client
        self.context = context

    def list(self, parent_id: int = 0, page_num: int = 1, page_size: int = 10):
        """查询分类列表"""
        params = {"parentId": parent_id, "pageNum": page_num, "pageSize": page_size}
        resp = self.client.get("/category/list", params=params)
        if resp.status_code == 200:
            return resp.json()
        return {"code": resp.status_code, "message": resp.text}

    def create(self, name: str, parent_id: int = 0, **kwargs):
        """创建分类"""
        data = {"name": name, "parentId": parent_id}
        data.update(kwargs)
        resp = self.client.post("/category/create", json=data)
        if resp.status_code == 200:
            result = resp.json()
            if result.get("code") == 200:
                self.context.set("category_id", result["data"]["id"])
            return result
        return {"code": resp.status_code, "message": resp.text}
```

### 2.2 步骤二：注册到 APIGroup

在 `tests/conftest.py` 中添加：

```python
from api.admin.category import AdminCategoryAPI

class AdminAPIGroup:
    def __init__(self, client, context):
        self.client = client
        self.context = context
        self.auth = AdminAuthAPI(client, context)
        self.product = AdminProductAPI(client, context)
        self.category = AdminCategoryAPI(client, context)  # 新增
        self.order = AdminOrderAPI(client, context)
```

### 2.3 步骤三：创建测试数据

在 `test_data/admin/category/` 下创建 YAML 文件：

```yaml
# test_data/admin/category/list.yaml
category_list:
  normal_cases:
    - name: "查询顶级分类"
      params:
        parent_id: 0
        page_num: 1
        page_size: 10
      expected:
        code: 200
```

### 2.4 步骤四：创建测试用例

```python
# tests/api/admin/category/test_category_list.py
import pytest
import allure
from core.data_loader import DataLoader

loader = DataLoader()
data = loader.get("admin/category/list.yaml", "category_list")

@allure.feature("后台-分类管理")
@allure.story("分类列表查询")
class TestCategoryList:

    @pytest.fixture(autouse=True)
    def setup(self, admin_logged_in):
        self.admin_api = admin_logged_in

    @pytest.mark.parametrize("case", data["normal_cases"])
    def test_list(self, case):
        result = self.admin_api.category.list(**case["params"])
        assert result["code"] == case["expected"]["code"]
```

---

## 三、如何运行测试

### 3.1 安装依赖

```bash
cd auto-test-framework
pip install -r requirements.txt
```

### 3.2 配置账号

编辑 `config/accounts.yaml`：

```yaml
admin:
  - username: "admin"
    password: "your_password"

portal:
  - username: "member"
    password: "member123"
```

### 3.3 运行命令

```bash
# 运行所有测试
pytest tests/

# 运行特定模块
pytest tests/api/admin/product/

# 运行业务流程测试
pytest tests/scenario/

# 按标记运行
pytest -m smoke        # 冒烟测试
pytest -m regression   # 回归测试

# 并行执行（加速）
pytest tests/ -n auto

# 生成 Allure 报告
pytest tests/ --alluredir=allure-results
python scripts/generate_report.py    # 自动启动 allure serve 并打开浏览器
```

### 3.4 查看 CI 测试报告

GitHub Actions 完成后，在 run 页面底部 **Artifacts** 区域下载 `allure-results.zip`，解压后本地查看：

```bash
allure serve /path/to/allure-results
```

---

## 四、模块协作关系

### 4.1 数据流

```
YAML 测试数据
    │
    ▼
DataLoader.load()
    │
    ▼
pytest.mark.parametrize
    │
    ▼
测试用例（断言）
    │
    ├──► ApiClient.request()
    │         │
    │         ▼
    │    HTTP 请求 → 服务器
    │
    └──► TestContext.set()  ← 存储 product_id
```

### 4.2 Fixture 层级

| Fixture | Scope | 作用 |
|---------|-------|------|
| `test_context` | session | 存储 token 和业务数据 |
| `admin_client` | session | HTTP 客户端（复用连接） |
| `admin_api` | session | 接口封装组 |
| `admin_logged_in` | function | 确保已登录 |
| `cleanup_context` | function | 测试后清理 |

### 4.3 Token 传递流程

```
登录接口
    │
    ▼
AdminAuthAPI.login()
    │
    ├──► 存入 context.admin_token
    │
    └──► ApiClient.set_auth_strategy(BearerTokenAuth(token))
              │
              ▼
         后续所有请求自动带上 Authorization header
```

---

## 五、代码执行示例

### 5.1 单接口测试

```python
# 1. DataLoader 加载 YAML
product_data = loader.get("admin/product/create.yaml", "product_create")
# 结果: {"normal_cases": [{"name": "正常创建", "data": {...}, ...}]}

# 2. pytest.mark.parametrize 生成多组测试
@pytest.mark.parametrize("case", product_data["normal_cases"])

# 3. 执行时，case 就是一组测试数据
def test_create_normal(self, case):
    # case = {"name": "正常创建", "data": {"price": 99.0, ...}}
    result = self.admin_api.product.create(**case["data"])
    # API 返回: {"code": 200, "data": {"id": 123}, "message": "success"}

    # 4. 断言验证
    assert result["code"] == case["expected"]["code"]
```

### 5.2 业务流程测试

```python
def test_lifecycle(self, admin_api, portal_api, test_context):
    # 1. 后台创建商品
    result = admin_api.product.create(name="测试商品", price=99.0)
    product_id = result["data"]["id"]

    # 2. Context 存储 ID
    test_context.set_product_id(product_id)

    # 3. 后台上架
    admin_api.product.publish(product_id)

    # 4. 前台查询（自动使用 Context 中的 ID）
    result = portal_api.product.detail()  # 无参时自动取 Context 中的 ID
    assert result["code"] == 200

    # 5. teardown 清理
    admin_api.product.delete(product_id)
```

---

## 六、常见问题

### Q1: 如何处理不同的认证方式？

框架使用策略模式，支持多种认证：

```python
# 当前项目使用 Bearer Token
from auth.bearer_token import BearerTokenAuth

# 其他项目可能用 Cookie 或 API Key
from auth.cookie_auth import CookieAuth
from auth.api_key import ApiKeyAuth
```

### Q2: 如何处理前后台不同的响应格式？

```python
# 后台返回 {"code": 200, "data": {...}}
# 前台返回 {"status": 500, "error": "Internal Server Error"}

# 测试中统一处理
actual_code = result.get("code", result.get("status", 200))
assert actual_code == expected_code
```

### Q3: 如何处理测试数据隔离？

```python
# 1. 使用时间戳生成唯一名称
unique_name = f"TEST_PRODUCT_{int(time.time())}"

# 2. teardown 中清理
def teardown_method(self):
    if self.created_product_id:
        admin_api.product.delete(self.created_product_id)
```

---

## 七、技术栈

| 组件 | 版本 | 用途 |
|------|------|------|
| pytest | >=7.4 | 测试框架 |
| requests | >=2.31 | HTTP 客户端 |
| pyyaml | >=6.0 | YAML 解析 |
| allure-pytest | >=2.13 | 测试报告 |
| pytest-xdist | >=3.5 | 并行执行 |
| pytest-order | >=1.1 | 测试顺序 |

---

## 八、扩展

### 添加新模块

```
1. api/admin/new_module.py     # 接口封装
2. test_data/admin/new_module/ # 测试数据
3. tests/api/admin/new_module/  # 测试用例
4. tests/conftest.py           # 注册 APIGroup
```

### CI/CD 集成

GitHub Actions 配置（`.github/workflows/pytest.yml`）：

```yaml
name: API Test CI/CD

on:
  push:
    branches: [ master ]
  pull_request:
    branches: [ master ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.10'
      - run: pip install -r requirements.txt
      - run: pytest tests/ -m smoke --alluredir=allure-results
      - name: Upload Allure results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: allure-results
          path: allure-results
          retention-days: 30
```

CI 跑 smoke 冒烟测试（只含查询类接口），allure-results 作为 artifact 上传供下载。
