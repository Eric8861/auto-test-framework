from typing import Optional, Dict
import requests
from auth.base import AuthStrategy


class CookieAuth(AuthStrategy):
    """Cookie 认证策略"""

    def __init__(self, cookies: Dict[str, str] = None):
        self._cookies = cookies or {}

    @property
    def cookies(self) -> Dict[str, str]:
        return self._cookies

    def apply(self, session: requests.Session) -> None:
        """将 Cookie 添加到 session"""
        for name, value in self._cookies.items():
            session.cookies.set(name, value)

    def from_login_response(self, response: requests.Response) -> dict:
        """从响应 cookies 中提取认证信息"""
        self._cookies = dict(response.cookies)
        return {"cookies": self._cookies}

    def get_token(self) -> Optional[str]:
        """Cookie 认证没有 token，返回 None"""
        return None

    def __repr__(self):
        cookie_names = list(self._cookies.keys())
        return f"CookieAuth(cookies={cookie_names})"
