#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Lark（飞书）通知脚本

用法:
    python scripts/lark_notify.py --status passed
    python scripts/lark_notify.py --status failed --report_url http://xxx
"""

import os
import sys
import argparse
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import requests
from config.config_loader import Config


def send_lark_notification(status: str, report_url: str = None):
    """发送 Lark 通知"""
    config = Config()

    if not config.lark_enabled:
        print("Lark 通知未启用，跳过")
        return

    webhook = config.lark_webhook
    if not webhook:
        print("Lark webhook 未配置，跳过")
        return

    # 状态颜色映射
    status_colors = {
        "passed": "green",
        "failed": "red",
        "error": "orange",
    }
    color = status_colors.get(status.lower(), "grey")

    # 构建消息
    message = {
        "msg_type": "interactive",
        "card": {
            "header": {
                "title": {
                    "tag": "plain_text",
                    "content": f"自动化测试 {status.upper()}"
                },
                "template": color
            },
            "elements": [
                {
                    "tag": "markdown",
                    "content": f"**环境**: {config.current_env}\n**状态**: {status.upper()}"
                }
            ]
        }
    }

    # 添加报告链接
    if report_url:
        message["card"]["elements"].append({
            "tag": "markdown",
            "content": f"[查看测试报告]({report_url})"
        })

    # 发送请求
    try:
        response = requests.post(webhook, json=message, timeout=10)
        result = response.json()

        if result.get("code") == 0:
            print("Lark 通知发送成功")
        else:
            print(f"Lark 通知发送失败: {result}")
    except Exception as e:
        print(f"Lark 通知发送异常: {e}")


def main():
    parser = argparse.ArgumentParser(description="发送 Lark 测试结果通知")
    parser.add_argument("--status", "-s", required=True, help="测试状态 (passed/failed/error)")
    parser.add_argument("--report_url", "-u", help="报告 URL")

    args = parser.parse_args()
    send_lark_notification(args.status, args.report_url)


if __name__ == "__main__":
    main()
