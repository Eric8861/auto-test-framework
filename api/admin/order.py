import time
from typing import Optional, Dict, Any
from core.api_client import ApiClient
from core.context import TestContext


class AdminOrderAPI:
    """后台订单管理接口"""

    def __init__(self, client: ApiClient, context: TestContext):
        self.client = client
        self.context = context

    def list(
        self,
        status: int = None,
        order_sn: str = None,
        page_num: int = 1,
        page_size: int = 10
    ) -> Dict[str, Any]:
        """查询订单列表"""
        params = {"pageNum": page_num, "pageSize": page_size}
        if status is not None:
            params["status"] = status
        if order_sn:
            params["orderSn"] = order_sn

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

    def deliver(
        self,
        order_id: int = None,
        delivery_company: str = None,
        delivery_sn: str = None
    ) -> Dict[str, Any]:
        """订单发货"""
        order_id = order_id or self.context.get_order_id()
        data = {
            "orderId": order_id,
            "deliveryCompany": delivery_company or "顺丰速运",
            "deliverySn": delivery_sn or f"SF{int(time.time())}"
        }
        resp = self.client.post("/order/update/delivery", json=data)
        if resp.status_code == 200:
            return resp.json()
        try:
            return resp.json()
        except:
            return {"code": resp.status_code, "message": resp.text}

    def close(self, order_id: int = None, note: str = None) -> Dict[str, Any]:
        """关闭订单"""
        order_id = order_id or self.context.get_order_id()
        data = {"orderId": order_id}
        if note:
            data["note"] = note
        resp = self.client.post("/order/update/close", json=data)
        if resp.status_code == 200:
            return resp.json()
        try:
            return resp.json()
        except:
            return {"code": resp.status_code, "message": resp.text}
