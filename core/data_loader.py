import os
import json
import yaml
from typing import Any, Dict, Optional
from pathlib import Path


class DataLoader:
    """数据加载器，支持 YAML 和 JSON"""

    _cache: Dict[str, Any] = {}

    def __init__(self, base_path: str = None):
        if base_path:
            self.base_path = Path(base_path)
        else:
            self.base_path = Path(__file__).parent.parent / "test_data"

    def _get_file_path(self, relative_path: str) -> Path:
        """获取文件完整路径"""
        path = Path(relative_path)
        if path.is_absolute():
            return path
        return self.base_path / path

    def _load_yaml(self, file_path: Path) -> Dict:
        """加载 YAML 文件"""
        with open(file_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}

    def _load_json(self, file_path: Path) -> Dict:
        """加载 JSON 文件"""
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def load(self, file_path: str, use_cache: bool = True) -> Dict:
        """加载数据文件"""
        if use_cache and file_path in self._cache:
            return self._cache[file_path]

        path = self._get_file_path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"数据文件不存在: {path}")

        if path.suffix in [".yaml", ".yml"]:
            data = self._load_yaml(path)
        elif path.suffix == ".json":
            data = self._load_json(path)
        else:
            raise ValueError(f"不支持的文件格式: {path.suffix}")

        if use_cache:
            self._cache[file_path] = data

        return data

    def get(self, file_path: str, key_path: str = None, use_cache: bool = True) -> Any:
        """获取指定 key 的数据

        Args:
            file_path: 文件路径
            key_path: 点分隔的 key 路径，如 "product.create.normal_cases"
            use_cache: 是否使用缓存
        """
        data = self.load(file_path, use_cache)

        if not key_path:
            return data

        keys = key_path.split(".")
        result = data
        for key in keys:
            if isinstance(result, dict):
                result = result.get(key)
            else:
                return None

        return result

    @classmethod
    def clear_cache(cls) -> None:
        """清空缓存"""
        cls._cache.clear()

    @classmethod
    def reload(cls, file_path: str) -> Dict:
        """重新加载文件（清除缓存后加载）"""
        cls._cache.pop(file_path, None)
        loader = cls()
        return loader.load(file_path, use_cache=False)
