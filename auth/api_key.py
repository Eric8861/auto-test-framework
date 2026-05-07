from typing import Optional, Dict
import requests
from auth.base import AuthStrategy


class ApiKeyAuth(AuthStrategy):
    """API Key 认证策略"""

    def __init__(self, api_key: str, header_name: str = "X-API-Key"):
        self._api_key = api_key
        self._header_name = header_name

    @property
    def api_key(self) -> str:
        return self._api_key

    @property
    def header_name(self) -> str:
        return self._header_name

    def apply(self, session: requests.Session) -> None:
        """将 API Key 添加到请求头"""
        session.headers[self._header_name] = self._api_key

    def from_login_response(self, response: requests.Response) -> dict:
        """API Key 通常不需要登录，直接返回"""
        return {}

    def get_token(self) -> Optional[str]:
        """API Key 即为凭证"""
        return self._api_key

    def __repr__(self):
        return f"ApiKeyAuth(header={self._header_name})"
