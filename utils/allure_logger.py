"""请求/响应日志工具 - 双通道输出（控制台 + Allure）"""
import os
import json
import shlex
from typing import Optional, Dict, Any
import logging
import allure

# 环境变量控制开关
ENABLE_CONSOLE_LOG = os.getenv("ENABLE_CONSOLE_LOG", "true").lower() == "true"
ENABLE_ALLURE_LOG = os.getenv("ENABLE_ALLURE_LOG", "true").lower() == "true"
ENABLE_REDACT_LOG = os.getenv("ENABLE_REDACT_LOG", "true").lower() == "true"

_DIVIDER = "=" * 50


def log_request_response(
    method: str,
    url: str,
    request_headers: Dict,
    request_params: Optional[Dict] = None,
    request_body: Optional[Any] = None,
    response_status: int = None,
    response_headers: Optional[Dict] = None,
    response_body: Any = None,
    name: str = "API Request/Response"
) -> None:
    """记录请求和响应信息（控制台 + Allure）"""
    # 构建数据结构（用于 Allure）
    data = _build_data(method, url, request_headers, request_params,
                       request_body, response_status, response_headers, response_body)

    # 生成 curl 命令
    curl_cmd = _to_curl(method, url, request_headers, request_params, request_body)

    # 通道1: 控制台输出
    if ENABLE_CONSOLE_LOG:
        _log_to_console(data, curl_cmd, name)

    # 通道2: Allure 附件
    if ENABLE_ALLURE_LOG:
        _attach_to_allure(data, curl_cmd, name)


def _to_curl(
    method: str,
    url: str,
    headers: Dict,
    params: Optional[Dict] = None,
    body: Optional[Any] = None
) -> str:
    """将请求转换为 curl 命令格式"""
    parts = ["curl"]

    # 请求方法
    if method.upper() != "GET":
        parts.append(f"-X {method.upper()}")

    # URL（拼接 query params）
    if params:
        query_string = "&".join(f"{k}={v}" for k, v in params.items())
        url = f"{url}?{query_string}"
    parts.append(f"'{url}'")

    # 只保留有意义的 headers
    important_keys = {"content-type", "authorization", "cookie", "accept"}
    for key, value in headers.items():
        if key.lower() in important_keys:
            # 脱敏处理（受环境变量控制）
            if ENABLE_REDACT_LOG and key.lower() in ("authorization", "cookie"):
                value = "REDACTED"
            parts.append(f"-H '{key}: {value}'")

    # Body
    if body:
        body_json = json.dumps(body, ensure_ascii=False) if isinstance(body, dict) else str(body)
        # 使用 shlex.quote 处理特殊字符
        parts.append(f"-d {shlex.quote(body_json)}")

    return " \\\n  ".join(parts)


def _build_data(
    method: str, url: str, headers: Dict, params: Optional[Dict],
    body: Optional[Any], status: int, resp_headers: Optional[Dict],
    resp_body: Any
) -> Dict:
    """构建数据结构"""
    data = {
        "request": {
            "method": method,
            "url": url,
            "headers": _sanitize_headers(headers),
        },
        "response": {}
    }
    if params:
        data["request"]["params"] = params
    if body:
        data["request"]["body"] = _parse_body(body)
    if status is not None:
        data["response"]["status_code"] = status
    if resp_headers:
        data["response"]["headers"] = _sanitize_headers(dict(resp_headers))
    if resp_body is not None:
        data["response"]["body"] = _parse_body(resp_body)
    return data


def _log_to_console(data: Dict, curl_cmd: str, name: str) -> None:
    """输出到控制台"""
    logger = logging.getLogger("auto_test.api")
    resp = data["response"]

    logger.info(f"\n{_DIVIDER}")
    logger.info(f"[REQUEST] {name}")
    logger.info(f"curl command:\n{curl_cmd}")

    if resp:
        logger.info(f"\n[RESPONSE] Status: {resp.get('status_code', 'N/A')}")
        if "body" in resp:
            body_str = json.dumps(resp['body'], ensure_ascii=False, indent=2)
            if len(body_str) > 1000:
                body_str = body_str[:1000] + "\n... (truncated)"
            logger.info(f"Body:\n{body_str}")
    logger.info(f"{_DIVIDER}\n")


def _attach_to_allure(data: Dict, curl_cmd: str, name: str) -> None:
    """附加到 Allure 报告"""
    # 将 curl 命令添加到数据中
    data["curl"] = curl_cmd
    json_str = json.dumps(data, indent=2, ensure_ascii=False)
    allure.attach(
        json_str,
        name=name,
        attachment_type=allure.attachment_type.JSON
    )


def _sanitize_headers(headers: Dict) -> Dict:
    """脱敏 headers 中的敏感信息（受环境变量控制）"""
    if not ENABLE_REDACT_LOG:
        return headers
    sensitive_keys = {"authorization", "cookie", "set-cookie"}
    return {
        k: "***REDACTED***" if k.lower() in sensitive_keys else v
        for k, v in headers.items()
    }


def _parse_body(body: Any) -> Any:
    """解析请求/响应 body"""
    if isinstance(body, str):
        try:
            return json.loads(body)
        except json.JSONDecodeError:
            return body
    return body
