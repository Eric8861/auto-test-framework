from typing import Optional, Dict, Any, List
from core.api_client import ApiClient
from core.context import TestContext


class PortalProductAPI:
    """前台商品接口"""

    def __init__(self, client: ApiClient, context: TestContext):
        self.client = client
        self.context = context

    def detail(self, product_id: int = None) -> Dict[str, Any]:
        """查询商品详情"""
        product_id = product_id or self.context.get_product_id()
        resp = self.client.get(f"/product/detail/{product_id}")
        if resp.status_code == 200:
            return resp.json()
        try:
            return resp.json()
        except:
            return {"code": resp.status_code, "message": resp.text, "status": resp.status_code}

    def search(
        self,
        keyword: str = None,
        page: int = 1,
        page_size: int = 10,
        category_id: int = None
    ) -> Dict[str, Any]:
        """搜索商品"""
        params = {"pageNum": page, "pageSize": page_size}
        if keyword:
            params["keyword"] = keyword
        if category_id:
            params["categoryId"] = category_id

        resp = self.client.get("/product/search", params=params)
        if resp.status_code == 200:
            return resp.json()
        try:
            return resp.json()
        except:
            return {"code": resp.status_code, "message": resp.text}

    def list(
        self,
        page: int = 1,
        page_size: int = 10,
        sort: str = None
    ) -> Dict[str, Any]:
        """商品列表"""
        params = {"pageNum": page, "pageSize": page_size}
        if sort:
            params["sort"] = sort

        resp = self.client.get("/product/list", params=params)
        if resp.status_code == 200:
            return resp.json()
        try:
            return resp.json()
        except:
            return {"code": resp.status_code, "message": resp.text}

    def recommend(self, limit: int = 10) -> Dict[str, Any]:
        """推荐商品"""
        resp = self.client.get("/product/recommend", params={"limit": limit})
        if resp.status_code == 200:
            return resp.json()
        try:
            return resp.json()
        except:
            return {"code": resp.status_code, "message": resp.text}
