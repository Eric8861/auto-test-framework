import pytest
import allure
from core.data_loader import DataLoader


loader = DataLoader()
product_detail_data = loader.get("portal/product/detail.yaml", "product_detail")


@allure.feature("前台-商品")
@allure.story("商品详情查询")
class TestProductDetail:
    """商品详情接口测试"""

    @pytest.fixture(autouse=True)
    def setup(self, portal_logged_in):
        self.portal_api = portal_logged_in

    @allure.title("查询商品详情-正常场景")
    @pytest.mark.portal
    @pytest.mark.normal
    @pytest.mark.parametrize("case", product_detail_data["normal_cases"])
    def test_detail_normal(self, case):
        """正常场景测试"""
        with allure.step(f"执行: {case['name']}"):
            result = self.portal_api.product.detail(case["product_id"])

        with allure.step("验证响应"):
            actual_code = result.get("code", result.get("status", 200))
            assert actual_code == case["expected"].get("code", 200), f"响应: {result}"

    @allure.title("查询商品详情-异常场景")
    @pytest.mark.portal
    @pytest.mark.error
    @pytest.mark.parametrize("case", product_detail_data["error_cases"])
    def test_detail_error(self, case):
        """异常场景测试"""
        with allure.step(f"执行: {case['name']}"):
            result = self.portal_api.product.detail(case["product_id"])

        with allure.step("验证响应"):
            # 优先检查 code 字段，否则检查 status 字段
            if "code" in case["expected"]:
                actual_code = result.get("code", result.get("status", 200))
                assert actual_code == case["expected"]["code"], f"响应: {result}"
            elif "status" in case["expected"]:
                actual_status = result.get("status", 200)
                assert actual_status == case["expected"]["status"], f"响应: {result}"
