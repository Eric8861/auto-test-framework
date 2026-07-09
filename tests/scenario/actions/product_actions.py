import allure
from utils.retry import retry


class ProductActions:
    """商品生命周期业务动作层：封装可复用的业务操作步骤"""

    def __init__(self, admin_api, portal_api, test_context):
        self.admin = admin_api
        self.portal = portal_api
        self.ctx = test_context
        self._created_ids: list[int] = []

    def create_product(self, data: dict) -> int:
        with allure.step("创建商品"):
            self.admin.ensure_login()
            result = self.admin.product.create(**data)
            assert result["code"] == 200, f"创建商品失败: {result}"
            pid = result["data"]["id"]
            self._created_ids.append(pid)
            self.ctx.set_product_id(pid)
            allure.attach(str(pid), "商品ID")
            return pid

    def verify_in_admin_list(self, product_id: int, keyword: str = None) -> None:
        with allure.step("后台验证商品在列表中"):
            self.admin.ensure_login()
            keyword = keyword or self.ctx.get("product_name", "")
            result = self.admin.product.list(keyword=keyword)
            assert result["code"] == 200
            found = any(p["id"] == product_id for p in result["data"]["list"])
            assert found, f"商品 {product_id} 未在后台列表中找到"

    @retry(max_times=2, interval=1)
    def publish_product(self, product_id: int) -> None:
        with allure.step("后台上架商品"):
            self.admin.ensure_login()
            result = self.admin.product.publish(product_id)
            assert result["code"] == 200, f"上架失败: {result}"

    @retry(max_times=2, interval=1)
    def unpublish_product(self, product_id: int) -> None:
        with allure.step("后台下架商品"):
            self.admin.ensure_login()
            result = self.admin.product.unpublish(product_id)
            assert result["code"] == 200, f"下架失败: {result}"

    def verify_portal_status(self, product_id: int, expected_code: int, expected_status: int) -> None:
        with allure.step("前台验证商品状态"):
            self.portal.ensure_login()
            result = self.portal.product.detail(product_id)
            assert result["code"] == expected_code, f"预期状态码 {expected_code}，实际 {result.get('code')}"
            if result["code"] == 200:
                actual_status = result["data"].get("publishStatus")
                assert actual_status == expected_status, \
                    f"预期发布状态 {expected_status}，实际 {actual_status}"

    @retry(max_times=2, interval=1)
    def delete_product(self, product_id: int) -> dict:
        with allure.step("删除商品"):
            result = self.admin.product.delete(product_id)
            assert result["code"] == 200, f"删除失败: {result}"
            return result

    def cleanup(self) -> None:
        for pid in self._created_ids:
            try:
                self.admin.ensure_login()
                self.admin.product.delete(pid)
            except Exception:
                pass
