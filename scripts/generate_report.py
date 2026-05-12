#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
生成并预览 Allure 报告

用法:
    python scripts/generate_report.py
"""

import subprocess
import sys
from pathlib import Path

RESULTS_DIR = "allure-results"


def main():
    project_root = Path(__file__).parent.parent

    results_path = project_root / RESULTS_DIR

    if not any(results_path.glob("*-result.json")):
        print("allure-results 中没有测试数据，请先运行: pytest tests/")
        sys.exit(1)

    print("启动 Allure 报告服务...")
    result = subprocess.run(
        f"allure serve {results_path}",
        cwd=project_root,
        shell=True
    )

    if result.returncode != 0:
        print("报告启动失败")
        sys.exit(1)


if __name__ == "__main__":
    main()
