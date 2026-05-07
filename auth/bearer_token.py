from typing import Optional
import requests
from auth.base import AuthStrategy


class BearerTokenAuth(AuthStrategy):
    """Bearer Token 认证策略"""

    def __init__(self, token: str = None):
        self._token = token

    @property
    def token(self) -> Optional[str]:
        return self._token

    @token.setter
    def token(self, value: str):
        self._token = value

    def apply(self, session: requests.Session) -> None:
        """将 Bearer Token 添加到请求头"""
        if self._token:
            session.headers["Authorization"] = f"Bearer {self._token}"

    def from_login_response(self, response: requests.Response) -> dict:
        """从 JSON 响应中提取 token"""
        data = response.json()
        token = data.get("data", {}).get("token")
        if token:
            self._token = token
        return {"token": token}

    def get_token(self) -> Optional[str]:
        """获取当前 token"""
        return self._token

    def __repr__(self):
        return f"BearerTokenAuth(token={'***' if self._token else None})"
