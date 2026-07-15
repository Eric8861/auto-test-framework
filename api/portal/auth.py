from typing import Optional
import requests
from core.api_client import ApiClient
from core.context import TestContext
from config.config_loader import Config
from auth.bearer_token import BearerTokenAuth


class PortalAuthAPI:
    """前台认证接口"""

    def __init__(self, client: ApiClient, context: TestContext):
        self.client = client
        self.context = context
        self.config = Config()

    def login(self, username: str = None, password: str = None) -> str:
        """前台登录（使用 form-data）"""
        username = username or self.config.portal_username
        password = password or self.config.portal_password

        resp = self.client.post(
            "/sso/login",
            data=f"username={username}&password={password}",
            headers={"Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"}
        )

        if resp.status_code == 200:
            data = resp.json()
            if data.get("code") == 200:
                token = data["data"]["token"]
                self.context.portal_token = token
                auth = BearerTokenAuth(token)
                self.client.set_auth_strategy(auth)
                return token

        raise Exception(f"登录失败: {resp.status_code} - {resp.text}")

    def logout(self) -> dict:
        """登出"""
        resp = self.client.post("/sso/logout")
        result = self.client.parse_response(resp)
        if resp.status_code == 200:
            self.context.portal_token = None
        return result
