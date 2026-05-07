import pytest
import allure
from core.data_loader import DataLoader


loader = DataLoader()
product_create_data = loader.get("admin/product/create.yaml", "product_create")


@allure.feature("后台-商品管理")
@allure.story("商品创建")
class TestProductCreate:
    """商品创建接口测试"""

    @pytest.fixture(autouse=True)
    def setup(self, admin_logged_in):
        """每个测试前确保登录"""
        self.admin_api = admin_logged_in

    @allure.title("正常场景-创建商品")
    @pytest.mark.admin
    @pytest.mark.normal
    @pytest.mark.parametrize("case", product_create_data["normal_cases"])
    def test_create_normal(self, case):
        """正常场景测试"""
        with allure.step(f"执行: {case['name']}"):
            result = self.admin_api.product.create(**case["data"])

        with allure.step("验证响应"):
            assert result["code"] == case["expected"]["code"], f"响应: {result}"
            if case["expected"].get("message"):
                assert case["expected"]["message"] in result.get("message", "")

        # 清理：删除测试创建的商品
        if result["code"] == 200 and result["data"].get("id"):
            product_id = result["data"]["id"]
            self.admin_api.product.delete(product_id)

    @allure.title("异常场景-创建商品")
    @pytest.mark.admin
    @pytest.mark.error
    @pytest.mark.parametrize("case", product_create_data["error_cases"])
    def test_create_error(self, case):
        """异常场景测试"""
        with allure.step(f"执行: {case['name']}"):
            result = self.admin_api.product.create(**case["data"])

        with allure.step("验证响应"):
            assert result["code"] == case["expected"]["code"], f"响应: {result}"

    @allure.title("边界值测试-创建商品")
    @pytest.mark.admin
    @pytest.mark.parametrize("case", product_create_data["boundary_cases"])
    def test_create_boundary(self, case):
        """边界值测试"""
        with allure.step(f"执行: {case['name']}"):
            result = self.admin_api.product.create(**case["data"])

        with allure.step("验证响应"):
            assert result["code"] == case["expected"]["code"], f"响应: {result}"

        # 清理
        if result["code"] == 200 and result["data"].get("id"):
            product_id = result["data"]["id"]
            self.admin_api.product.delete(product_id)
