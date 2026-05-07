#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试运行脚本

用法:
    python scripts/run_tests.py                    # 运行所有测试
    python scripts/run_tests.py --env test         # 指定环境
    python scripts/run_tests.py --tag admin        # 按标记运行
    python scripts/run_tests.py --scenario        # 仅运行场景测试
"""

import os
import sys
import argparse
import subprocess
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def main():
    parser = argparse.ArgumentParser(description="运行自动化测试")
    parser.add_argument("--env", "-e", default="test", help="运行环境 (dev/test/prod)")
    parser.add_argument("--tag", "-t", help="按标记过滤 (smoke/regression/scenario)")
    parser.add_argument("--scenario", "-s", action="store_true", help="仅运行场景测试")
    parser.add_argument("--admin", action="store_true", help="仅运行后台测试")
    parser.add_argument("--portal", action="store_true", help="仅运行前台测试")
    parser.add_argument("--parallel", "-p", action="store_true", help="并行执行")
    parser.add_argument("--workers", "-w", type=int, default=4, help="并行worker数量")
    parser.add_argument("--report", "-r", action="store_true", help="生成HTML报告")
    parser.add_argument("--verbose", "-v", action="store_true", help="详细输出")

    args = parser.parse_args()

    # 设置环境变量
    os.environ["ENV"] = args.env

    # 构建 pytest 命令
    pytest_args = []

    # 测试路径
    if args.scenario:
        pytest_args.append("tests/scenario")
    elif args.admin:
        pytest_args.append("tests/api/admin")
    elif args.portal:
        pytest_args.append("tests/api/portal")
    else:
        pytest_args.append("tests")

    # 标记过滤
    if args.tag:
        pytest_args.extend(["-m", args.tag])

    # 详细输出
    if args.verbose:
        pytest_args.append("-v")

    # Allure 结果目录
    pytest_args.extend(["--alluredir", "allure-results"])

    # 并行执行
    if args.parallel:
        pytest_args.extend(["-n", str(args.workers)])

    # HTML 报告
    if args.report:
        pytest_args.append("--html=reports/report.html")
        pytest_args.append("--self-contained-html")

    # 运行测试
    print(f"运行测试，环境: {args.env}")
    print(f"命令: pytest {' '.join(pytest_args)}")

    result = subprocess.run(["pytest"] + pytest_args, cwd=project_root)