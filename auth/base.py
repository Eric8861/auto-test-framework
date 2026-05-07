from abc import ABC, abstractmethod
from typing import Optional
import requests


class AuthStrategy(ABC):
    """认证策略基类，定义统一接口"""

    @abstractmethod
    def apply(self, session: requests.Session) -> None:
        """将认证信息应用到 session"""
        pass

    @abstractmethod
    def from_login_response(self, response: requests.Response) -> dict:
        """从登录响应中提取认证信息"""
        pass

    @abstractmethod
    def get_token(self) -> Optional[str]:
        """获取当前认证凭证"""
        pass
