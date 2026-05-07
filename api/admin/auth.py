from typing import Optional
from core.api_client import ApiClient
from core.context import TestContext
from config.config_loader import Config
from auth.bearer_token import BearerTokenAuth


class AdminAuthAPI:
    """后台认证接口"""

    def __init__(self, client: ApiClient, context: TestContext):
        self.client = client
        self.context = context
        self.config = Config()

    def login(self, username: str = None, password: str = None) -> str:
        """登录并存储 token"""
        username = username or self.config.admin_username
        password = password or self.config.admin_password

        resp = self.client.post(
            "/admin/login",
            json={"username": username, "password": password}
        )

        if resp.status_code == 200:
            data = resp.json()
            if data.get("code") == 200:
                token = data["data"]["token"]
                self.context.admin_token = token
                auth = BearerTokenAuth(token)
                self.client.set_auth_strategy(auth)
                return token

        raise Exception(f"登录失败: {resp.status_code} - {resp.text}")

    def logout(self) -> dict:
        """登出"""
        resp = self.client.post("/admin/logout")
        if resp.status_code == 200:
            self.context.admin_token = None
        return resp.json()

    def is_logged_in(self) -> bool:
        """检查是否已登录"""
        return self.context.admin_token is not None

    def get_token(self) -> Optional[str]:
        """获取当前 token"""
        return self.context.admin_token
