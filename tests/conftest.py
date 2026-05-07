import pytest
from core.api_client import ApiClient
from core.context import TestContext
from config.config_loader import Config
from api.admin.auth import AdminAuthAPI
from api.admin.product import AdminProductAPI
from api.admin.order import AdminOrderAPI
from api.portal.auth import PortalAuthAPI
from api.portal.product import PortalProductAPI
from api.portal.order import PortalOrderAPI


config = Config()


class AdminAPIGroup:
    """后台接口分组"""

    def __init__(self, client: ApiClient, context: TestContext):
        self.client = client
        self.context = context
        self.auth = AdminAuthAPI(client, context)
        self.product = AdminProductAPI(client, context)
        self.order = AdminOrderAPI(client, context)

    def ensure_login(self):
        """确保已登录"""
        if not self.context.admin_token:
            self.auth.login()


class PortalAPIGroup:
    """前台接口分组"""

    def __init__(self, client: ApiClient, context: TestContext):
        self.client = client
        self.context = context
        self.auth = PortalAuthAPI(client, context)
        self.product = PortalProductAPI(client, context)
        self.order = PortalOrderAPI(client, context)

    def ensure_login(self):
        """确保已登录"""
        if not self.context.portal_token:
            self.auth.login()


@pytest.fixture(scope="session")
def test_context():
    """会话级测试上下文"""
    return TestContext()


@pytest.fixture(scope="session")
def admin_client(test_context):
    """后台 API 客户端（会话级）"""
    client = ApiClient(config.admin_base_url, test_context)
    yield client
    client.close()


@pytest.fixture(scope="session")
def portal_client(test_context):
    """前台 API 客户端"""
    client = ApiClient(config.portal_base_url, test_context)
    yield client
    client.close()


@pytest.fixture(scope="session")
def admin_api(admin_client, test_context):
    """后台接口封装"""
    return AdminAPIGroup(admin_client, test_context)


@pytest.fixture(scope="session")
def portal_api(portal_client, test_context):
    """前台接口封装"""
    return PortalAPIGroup(portal_client, test_context)


@pytest.fixture(scope="function")
def admin_logged_in(admin_api):
    """确保后台已登录"""
    admin_api.ensure_login()
    yield admin_api


@pytest.fixture(scope="function")
def portal_logged_in(portal_api):
    """确保前台已登录"""
    portal_api.ensure_login()
    yield portal_api


@pytest.fixture(autouse=True)
def cleanup_context(test_context):
    """每个测试后清理上下文数据"""
    yield
    test_context.clear()
