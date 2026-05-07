from dataclasses import dataclass, field
from typing import Any, Optional
from datetime import datetime


@dataclass
class TestContext:
    """测试上下文：存储跨接口共享数据"""

    admin_token: Optional[str] = None
    portal_token: Optional[str] = None

    _data: dict = field(default_factory=dict)

    test_start_time: datetime = field(default_factory=datetime.now)
    test_name: str = ""

    def set(self, key: str, value: Any) -> None:
        """存储数据"""
        self._data[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        """获取数据"""
        return self._data.get(key, default)

    def set_product_id(self, product_id: int) -> None:
        self.set("product_id", product_id)

    def get_product_id(self) -> Optional[int]:
        return self.get("product_id")

    def set_order_id(self, order_id: int) -> None:
        self.set("order_id", order_id)

    def get_order_id(self) -> Optional[int]:
        return self.get("order_id")

    def set_created_ids(self, **kwargs) -> None:
        """批量存储创建的资源 ID"""
        for key, value in kwargs.items():
            self.set(key, value)

    def get_created_id(self, resource_type: str) -> Optional[int]:
        """获取指定类型创建的资源 ID"""
        return self.get(f"{resource_type}_id")

    def clear(self) -> None:
        """清空业务数据（保留 token）"""
        self._data.clear()

    def clear_all(self) -> None:
        """清空所有数据包括 token"""
        self._data.clear()
        self.admin_token = None
        self.portal_token = None
