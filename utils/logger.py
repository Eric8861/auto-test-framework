import logging
import sys
from pathlib import Path


def get_logger(name: str = None, level: int = logging.INFO) -> logging.Logger:
    """获取日志记录器"""
    logger = logging.getLogger(name or "auto_test")

    if not logger.handlers:
        logger.setLevel(level)

        # 控制台处理器
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)

        # 格式化
        formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(name)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        console_handler.setFormatter(formatter)

        logger.addHandler(console_handler)

    return logger


# 默认日志记录器
logger = get_logger()
