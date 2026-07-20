import json as _json
from typing import Optional, Dict, Any, Union
import requests
from core.context import TestContext
from auth.base import AuthStrategy


class ApiClient:
    """统一 HTTP 客户端，支持多种认证策略"""

    def __init__(self, base_url: str, context: TestContext = None):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.context = context
        self._auth_strategy: Optional[AuthStrategy] = None

    def set_auth_strategy(self, strategy: AuthStrategy) -> None:
        """设置认证策略"""
        self._auth_strategy = strategy
        strategy.apply(self.session)

    def get_auth_strategy(self) -> Optional[AuthStrategy]:
        """获取当前认证策略"""
        return self._auth_strategy

    def request(
        self,
        method: str,
        path: str,
        params: Optional[Dict] = None,
        json: Optional[Dict] = None,
        data: Optional[Union[str, Dict]] = None,
        headers: Optional[Dict] = None,
        **kwargs
    ) -> requests.Response:
        """发送 HTTP 请求"""
        url = f"{self.base_url}{path}"
        default_headers = {"Content-Type": "application/json;charset=UTF-8"}
        if headers:
            default_headers.update(headers)

        response = self.session.request(
            method=method,
            url=url,
            params=params,
            json=json,
            data=data,
            headers=default_headers,
            **kwargs
        )
        print("===== 请求入参(可直接粘贴到 Postman) =====")
        print(f"method: {method}")
        print(f"full url: {url}")
        if params:
            print(f"params:\n{_json.dumps(params, indent=2, ensure_ascii=False)}")
        if json:
            print(f"Body(raw/JSON):\n{_json.dumps(json, indent=2, ensure_ascii=False)}")
        if data and isinstance(data, str):
            print(f"data: {data}")
        elif data:
            print(f"data:\n{_json.dumps(data, indent=2, ensure_ascii=False)}")
        print(f"headers: {_json.dumps(default_headers, indent=2, ensure_ascii=False)}")
        print(f"实际发送headers: {dict(response.request.headers)}")
        return response

    def get(self, path: str, **kwargs) -> requests.Response:
        """GET 请求"""
        return self.request("GET", path, **kwargs)

    def post(self, path: str, **kwargs) -> requests.Response:
        """POST 请求"""
        return self.request("POST", path, **kwargs)

    def put(self, path: str, **kwargs) -> requests.Response:
        """PUT 请求"""
        return self.request("PUT", path, **kwargs)

    def delete(self, path: str, **kwargs) -> requests.Response:
        """DELETE 请求"""
        return self.request("DELETE", path, **kwargs)

    def patch(self, path: str, **kwargs) -> requests.Response:
        """PATCH 请求"""
        return self.request("PATCH", path, **kwargs)

    def close(self) -> None:
        """关闭 session"""
        self.session.close()

    @staticmethod
    def parse_response(resp: requests.Response) -> dict:
        if resp.status_code == 200:
            return resp.json()
        try:
            return resp.json()
        except Exception:
            return {"code": resp.status_code, "message": resp.text}

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
