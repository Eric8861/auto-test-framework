#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
生成 Allure 报告

用法:
    python scripts/generate_report.py
"""

import subprocess
import sys
from pathlib import Path


def main():
    project_root = Path(__file__).parent.parent

    print("生成 Allure 报告...")

    # 生成报告
    result = subprocess.run(
        ["allure", "generate", "D:/Code/codex/auto-test-framework/allure-results", "-o", "D:/Code/codex/auto-test-framework/allure-report", "--clean"],
        cwd=project_root
    )

    if result.returncode == 0:
        print("报告生成成功: allure-report/index.html")
        print("启动服务预览: allure serve allure-results")
    else:
        print("报告生成失败")
        sys.exit(1)


if __name__ == "__main__":
    main()
