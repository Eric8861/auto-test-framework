import hashlib
import hmac
import base64
from typing import Optional


def md5(text: str) -> str:
    """MD5 加密"""
    return hashlib.md5(text.encode("utf-8")).hexdigest()


def sha256(text: str) -> str:
    """SHA256 加密"""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def hmac_sha256(key: str, message: str) -> str:
    """HMAC-SHA256 加密"""
    return hmac.new(
        key.encode("utf-8"),
        message.encode("utf-8"),
        hashlib.sha256
    ).hexdigest()


def base64_encode(text: str) -> str:
    """Base64 编码"""
    return base64.b64encode(text.encode("utf-8")).decode("utf-8")


def base64_decode(encoded: str) -> str:
    """Base64 解码"""
    return base64.b64decode(encoded.encode("utf-8")).decode("utf-8")


def encode_password(password: str, salt: str = "") -> str:
    """密码加密（简单示例，实际项目可能更复杂）"""
    combined = f"{password}{salt}"
    return sha256(combined)
