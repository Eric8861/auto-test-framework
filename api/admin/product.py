from typing import Optional, Dict, List, Any
from core.api_client import ApiClient
from core.context import TestContext
from utils.random_data import generate_unique_name


class AdminProductAPI:
    """后台商品管理接口"""

    def __init__(self, client: ApiClient, context: TestContext):
        self.client = client
        self.context = context

    def create(
        self,
        name: str = None,
        price: float = 99.0,
        brand_id: int = 49,
        category_id: int = 7,
        stock: int = 100,
        publish_status: int = 0,
        **kwargs
    ) -> Dict[str, Any]:
        """创建商品"""
        product_data = {
            "name": name or generate_unique_name("TEST_PRODUCT"),
            "price": price,
            "brandId": brand_id,
            "brandName": "测试品牌",
            "productCategoryId": category_id,
            "productCategoryName": "外套",
            "publishStatus": publish_status,
            "stock": stock,
            "deleteStatus": 0,
            "description": "自动化测试商品",
            "giftPoint": 1,
            "giftGrowth": 2,
            "keywords": "测试",
            "lowStock": 10,
            "newStatus": 0,
            "originalPrice": price * 1.5,
            "recommandStatus": 1,
            "sale": 0,
            "sort": 0,
            "verifyStatus": 0,
            "weight": 0,
            "unit": "件",
            "memberPriceList": [
                {"memberLevelId": 1, "memberLevelName": "黄金会员"},
                {"memberLevelId": 2, "memberLevelName": "白金会员"},
            ],
            "productFullReductionList": [{"fullPrice": 0, "reducePrice": 0}],
            "productLadderList": [{"count": 0, "discount": 0, "price": 0}],
        }
        product_data.update(kwargs)

        resp = self.client.post("/product/create", json=product_data)

        if resp.status_code == 200:
            result = resp.json()
            if result.get("code") == 200:
                product_id = result["data"]["id"]
                self.context.set_product_id(product_id)
                self.context.set("product_name", product_data["name"])
            return result

        # 返回原始响应以便测试用例判断
        try:
            return resp.json()
        except:
            return {"code": resp.status_code, "message": resp.text}

    def list(
        self,
        keyword: str = None,
        page_num: int = 1,
        page_size: int = 10
    ) -> Dict[str, Any]:
        """查询商品列表"""
        params = {"pageNum": page_num, "pageSize": page_size}
        if keyword:
            params["keyword"] = keyword

        resp = self.client.get("/product/list", params=params)
        if resp.status_code == 200:
            return resp.json()
        try:
            return resp.json()
        except:
            return {"code": resp.status_code, "message": resp.text}

    def detail(self, product_id: int = None) -> Dict[str, Any]:
        """查询商品详情"""
        product_id = product_id or self.context.get_product_id()
        resp = self.client.get(f"/product/{product_id}")
        if resp.status_code == 200:
            return resp.json()
        try:
            return resp.json()
        except:
            return {"code": resp.status_code, "message": resp.text}

    def publish(self, product_id: int = None) -> Dict[str, Any]:
        """上架商品"""
        product_id = product_id or self.context.get_product_id()
        resp = self.client.post("/product/update/publishStatus", json={
            "ids": [product_id],
            "publishStatus": 1
        })
        if resp.status_code == 200:
            return resp.json()
        try:
            return resp.json()
        except:
            return {"code": resp.status_code, "message": resp.text}

    def unpublish(self, product_id: int = None) -> Dict[str, Any]:
        """下架商品"""
        product_id = product_id or self.context.get_product_id()
        resp = self.client.post("/product/update/publishStatus", json={
            "ids": [product_id],
            "publishStatus": 0
        })
        if resp.status_code == 200:
            return resp.json()
        try:
            return resp.json()
        except:
            return {"code": resp.status_code, "message": resp.text}

    def delete(self, product_id: int = None) -> Dict[str, Any]:
        """删除商品"""
        product_id = product_id or self.context.get_product_id()
        resp = self.client.post("/product/delete", json={"ids": [product_id]})
        if resp.status_code == 200:
            return resp.json()
        try:
            return resp.json()
        except:
            return {"code": resp.status_code, "message": resp.text}

    def update(
        self,
        product_id: int = None,
        **kwargs
    ) -> Dict[str, Any]:
        """更新商品"""
        product_id = product_id or self.context.get_product_id()
        data = {"id": product_id}
        data.update(kwargs)
        resp = self.client.post("/product/update", json=data)
        if resp.status_code == 200:
            return resp.json()
        try:
            return resp.json()
        except:
            return {"code": resp.status_code, "message": resp.text}
