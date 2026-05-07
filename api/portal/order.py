from typing import Optional, Dict, Any
from core.api_client import ApiClient
from core.context import TestContext


class PortalOrderAPI:
    """前台订单接口"""

    def __init__(self, client: ApiClient, context: TestContext):
        self.client = client
        self.context = context

    def list(
        self,
        status: int = -1,
        page: int = 1,
        page_size: int = 10
    ) -> Dict[str, Any]:
        """查询订单列表"""
        params = {"status": status, "pageNum": page, "pageSize": page_size}
        resp = self.client.get("/order/list", params=params)
        if resp.status_code == 200:
            return resp.json()
        try:
            return resp.json()
        except:
            return {"code": resp.status_code, "message": resp.text}

    def detail(self, order_id: int = None) -> Dict[str, Any]:
        """查询订单详情"""
        order_id = order_id or self.context.get_order_id()
        resp = self.client.get(f"/order/{order_id}")
        if resp.status_code == 200:
            return resp.json()
        try:
            return resp.json()
        except:
            return {"code": resp.status_code, "message": resp.text}

    def cancel(self, order_id: int = None, reason: str = None) -> Dict[str, Any]:
        """取消订单"""
        order_id = order_id or self.context.get_order_id()
        data = {"orderId": order_id}
        if reason:
            data["reason"] = reason
        resp = self.client.post("/order/cancel", json=data)
        if resp.status_code == 200:
            return resp.json()
        try:
            return resp.json()
        except:
            return {"code": resp.status_code, "message": resp.text}
