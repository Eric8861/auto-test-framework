import pytest
import allure
from core.data_loader import DataLoader
from tests.scenario.actions.product_actions import ProductActions

loader = DataLoader()
scenario_data = loader.get("scenario/product_lifecycle.yaml")


@allure.feature("业务流程测试")
@allure.story("商品生命周期管理")
class TestProductLifecycle:

    @pytest.fixture(autouse=True)
    def setup(self, admin_api, portal_api, test_context):
        self.actions = ProductActions(admin_api, portal_api, test_context)
        self.admin_api = admin_api

    def teardown_method(self):
        self.actions.cleanup()

    @allure.title("完整生命周期：创建→上架→前台可见→下架→前台不可见")
    def test_lifecycle_complete(self):
        data = scenario_data["lifecycle"]
        create_data = data["create_data"]
        expected = data["expected"]

        pid = self.actions.create_product(create_data)
        self.actions.verify_in_admin_list(pid)
        self.actions.publish_product(pid)
        self.actions.verify_portal_status(
            pid,
            expected["portal_published"]["code"],
            expected["portal_published"]["publishStatus"],
        )
        self.actions.unpublish_product(pid)
        self.actions.verify_portal_status(
            pid,
            expected["portal_unpublished"]["code"],
            expected["portal_unpublished"]["publishStatus"],
        )

    @allure.title("创建未发布商品直接下架应拒绝")
    def test_unpublish_without_publish(self):
        data = scenario_data["unpublish_without_publish"]
        pid = self.actions.create_product(data["create_data"])
        result = self.admin_api.product.unpublish(pid)
        assert result["code"] == data["expected"]["unpublish_code"]

    @allure.title("重复删除应幂等")
    def test_delete_idempotent(self):
        data = scenario_data["delete_idempotent"]
        pid = self.actions.create_product(data["create_data"])
        assert self.admin_api.product.delete(pid)["code"] == data["expected"]["first_delete"]
        assert self.admin_api.product.delete(pid)["code"] == data["expected"]["second_delete"]
