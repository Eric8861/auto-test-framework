import time
import pytest
import allure
from core.data_loader import DataLoader


@allure.feature("业务流程测试")
@allure.story("商品生命周期管理")
class TestProductLifecycle:
    """商品生命周期测试：从创建到上下架"""

    @pytest.fixture(autouse=True)
    def setup(self, admin_api, portal_api):
        """初始化 API"""
        self.admin_api = admin_api
        self.portal_api = portal_api
        self.created_product_id = None

    def teardown_method(self):
        """测试后清理：删除商品"""
        if self.created_product_id:
            try:
                self.admin_api.ensure_login()
                self.admin_api.product.delete(self.created_product_id)
            except Exception:
                pass

    @allure.title("完整生命周期：创建 → 上架 → 前台可见 → 下架 → 前台不可见")
    @pytest.mark.scenario
    @pytest.mark.order(1)
    def test_product_lifecycle_complete(self, test_context):
        """
        测试步骤：
        1. 后台登录
        2. 创建商品（获取商品ID）
        3. 后台查询商品，确认创建成功
        4. 后台上架商品
        5. 前台查询商品，确认上架后可见
        6. 后台下架商品
        7. 前台查询商品，确认下架后不可见
        """
        unique_name = f"TEST_PRODUCT_{int(time.time())}"

        # Step 1: 后台登录
        with allure.step("后台登录"):
            self.admin_api.ensure_login()
            assert test_context.admin_token is not None, "后台登录失败"
            allure.attach(f"Token: {test_context.admin_token[:20]}...", "登录信息")

        # Step 2: 创建商品
        with allure.step("后台创建商品"):
            result = self.admin_api.product.create(
                name=unique_name,
                price=199.0,
                brand_id=49,
                category_id=7,
                stock=100,
                publish_status=0
            )
            assert result["code"] == 200, f"创建失败: {result}"

            self.created_product_id = result["data"]["id"]
            test_context.set_product_id(self.created_product_id)
            test_context.set("product_name", unique_name)
            allure.attach(f"商品ID: {self.created_product_id}, 名称: {unique_name}", "创建结果")

        # Step 3: 后台查询商品
        with allure.step("后台查询商品列表"):
            result = self.admin_api.product.list(keyword=unique_name)
            assert result["code"] == 200, f"查询失败: {result}"

            products = result["data"]["list"]
            found = any(p["id"] == self.created_product_id for p in products)
            assert found, f"商品列表中未找到ID={self.created_product_id}的商品"
            allure.attach(f"列表中找到 {len(products)} 条记录", "查询结果")

        # Step 4: 上架商品
        with allure.step("后台上架商品"):
            result = self.admin_api.product.publish(self.created_product_id)
            assert result["code"] == 200, f"上架失败: {result}"
            allure.attach("上架成功", "操作结果")

        # Step 5: 前台查询（上架后应该可见）
        with allure.step("前台查询上架商品"):
            self.portal_api.ensure_login()
            result = self.portal_api.product.detail(self.created_product_id)
            assert result["code"] == 200, f"前台查询失败: {result}"
            assert result["data"]["id"] == self.created_product_id, "商品ID不匹配"
            assert result["data"]["publishStatus"] == 1, "商品状态应为上架"
            allure.attach(f"商品名称: {result['data']['name']}, 状态: {result['data']['publishStatus']}", "前台商品信息")

        # Step 6: 下架商品
        with allure.step("后台下架商品"):
            self.admin_api.ensure_login()
            result = self.admin_api.product.unpublish(self.created_product_id)
            assert result["code"] == 200, f"下架失败: {result}"
            allure.attach("下架成功", "操作结果")

        # Step 7: 前台查询（下架后应该不可见或状态为下架）
        with allure.step("前台查询下架商品"):
            result = self.portal_api.product.detail(self.created_product_id)
            # 下架后前台可能返回 404 或 publishStatus=0
            assert result["code"] in [200, 404], f"响应异常: {result}"
            if result["code"] == 200:
                assert result["data"]["publishStatus"] == 0, "商品状态应为下架"
            allure.attach(f"响应码: {result['code']}", "前台查询结果")

    @allure.title("创建后直接删除")
    @pytest.mark.scenario
    @pytest.mark.order(2)
    def test_product_delete_after_create(self, test_context):
        """测试创建商品后直接删除"""
        unique_name = f"TEST_PRODUCT_DELETE_{int(time.time())}"

        # 创建商品
        with allure.step("创建商品"):
            self.admin_api.ensure_login()
            result = self.admin_api.product.create(
                name=unique_name,
                price=99.0,
                brand_id=49,
                category_id=7
            )
            assert result["code"] == 200

            self.created_product_id = result["data"]["id"]
            allure.attach(f"商品ID: {self.created_product_id}", "创建结果")

        # 删除商品
        with allure.step("删除商品"):
            result = self.admin_api.product.delete(self.created_product_id)
            assert result["code"] == 200, f"删除失败: {result}"
            allure.attach("删除成功", "操作结果")

        # 验证商品不可查询
        with allure.step("验证商品已删除"):
            result = self.admin_api.product.list(keyword=unique_name)
            assert result["code"] == 200
            products = result["data"]["list"]
            found = any(p["id"] == self.created_product_id for p in products)
            assert not found, "商品应该已被删除"
