import os
import yaml
from typing import Any, Dict, Optional
from pathlib import Path


class Config:
    """配置加载器，支持多环境切换"""

    _instance: Optional["Config"] = None
    _config: Dict[str, Any] = {}
    _accounts: Dict[str, Any] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load_config()
        return cls._instance

    def _load_config(self) -> None:
        """加载配置文件"""
        config_dir = Path(__file__).parent

        env = os.getenv("ENV", "test")
        config_file = config_dir / "config.yaml"
        env_file = config_dir / "env" / f"{env}.yaml"
        accounts_file = config_dir / "accounts.yaml"

        self._config = {}

        if config_file.exists():
            with open(config_file, "r", encoding="utf-8") as f:
                self._config = yaml.safe_load(f) or {}

        if env_file.exists():
            with open(env_file, "r", encoding="utf-8") as f:
                env_config = yaml.safe_load(f) or {}
                self._config.update(env_config)

        self._accounts = {}
        if accounts_file.exists():
            with open(accounts_file, "r", encoding="utf-8") as f:
                self._accounts = yaml.safe_load(f) or {}

    def get(self, key: str, default: Any = None) -> Any:
        """获取配置值，支持点分隔路径"""
        keys = key.split(".")
        value = self._config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
        return value if value is not None else default

    @property
    def admin_base_url(self) -> str:
        return self.get("admin.base_url", "https://admin-api.macrozheng.com")

    @property
    def portal_base_url(self) -> str:
        return self.get("portal.base_url", "https://portal-api.macrozheng.com")

    @property
    def admin_username(self) -> str:
        accounts = self._accounts.get("admin", [])
        if accounts:
            return accounts[0].get("username", "admin")
        return "admin"

    @property
    def admin_password(self) -> str:
        accounts = self._accounts.get("admin", [])
        if accounts:
            return accounts[0].get("password", "macro123")
        return "macro123"

    @property
    def portal_username(self) -> str:
        accounts = self._accounts.get("portal", [])
        if accounts:
            return accounts[0].get("username", "member")
        return "member"

    @property
    def portal_password(self) -> str:
        accounts = self._accounts.get("portal", [])
        if accounts:
            return accounts[0].get("password", "member123")
        return "member123"

    @property
    def admin_accounts(self) -> list:
        return self._accounts.get("admin", [])

    @property
    def portal_accounts(self) -> list:
        return self._accounts.get("portal", [])

    @property
    def timeout(self) -> int:
        return self.get("timeout", 30)

    @property
    def allure_results_dir(self) -> str:
        return self.get("allure.results_dir", "allure-results")

    @property
    def allure_report_dir(self) -> str:
        return self.get("allure.report_dir", "allure-report")

    @property
    def enable_console_log(self) -> bool:
        """是否启用控制台请求日志"""
        return self.get("log.enable_console", True)

    @property
    def enable_allure_log(self) -> bool:
        """是否启用 Allure 请求日志"""
        return self.get("log.enable_allure", True)

    @property
    def enable_redact_log(self) -> bool:
        """是否启用日志脱敏（关闭后 curl 命令包含真实 token）"""
        return self.get("log.enable_redact", True)

    @property
    def lark_webhook(self) -> str:
        return self.get("lark.webhook", "")

    @property
    def lark_enabled(self) -> bool:
        return self.get("lark.enabled", False)

    @property
    def current_env(self) -> str:
        return os.getenv("ENV", "test")

    def reload(self) -> None:
        """重新加载配置"""
        self._load_config()

    @classmethod
    def reset(cls) -> None:
        """重置单例（用于测试或切换环境）"""
        cls._instance = None


def get_config() -> Config:
    """获取配置实例"""
    return Config()
