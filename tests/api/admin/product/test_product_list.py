import pytest
import allure
from core.data_loader import DataLoader


loader = DataLoader()
product_list_data = loader.get("admin/product/list.yaml", "product_list")


@allure.feature("后台-商品管理")
@allure.story("商品列表查询")
class TestProductList:
    """商品列表接口测试"""

    @pytest.fixture(autouse=True)
    def setup(self, admin_logged_in):
        self.admin_api = admin_logged_in

    @allure.title("查询商品列表-正常场景")
    @pytest.mark.admin
    @pytest.mark.normal
    @pytest.mark.parametrize("case", product_list_data["normal_cases"])
    def test_list_normal(self, case):
        """正常场景测试"""
        with allure.step(f"执行: {case['name']}"):
            result = self.admin_api.product.list(**case["params"])

        with allure.step("验证响应"):
            assert result["code"] == case["expected"]["code"], f"响应: {result}"
            if case["expected"].get("has_data"):
                assert "data" in result

    @allure.title("查询商品列表-异常场景")
    @pytest.mark.admin
    @pytest.mark.error
    @pytest.mark.parametrize("case", product_list_data["error_cases"])
    def test_list_error(self, case):
        """异常场景测试"""
        with allure.step(f"执行: {case['name']}"):
            result = self.admin_api.product.list(**case["params"])

        with allure.step("验证响应"):
            assert result["code"] == case["expected"]["code"], f"响应: {result}"
