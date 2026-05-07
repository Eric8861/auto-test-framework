import time
import random
import string
from datetime import datetime


def generate_unique_name(prefix: str = "TEST") -> str:
    """生成唯一的测试数据名称"""
    timestamp = int(time.time() * 1000) % 100000000
    random_str = "".join(random.choices(string.ascii_lowercase + string.digits, k=4))
    return f"{prefix}_{timestamp}_{random_str}"


def generate_random_phone() -> str:
    """生成随机手机号"""
    prefixes = ["130", "131", "132", "133", "134", "135", "136", "137", "138", "139",
                "150", "151", "152", "153", "155", "156", "157", "158", "159",
                "180", "181", "182", "183", "184", "185", "186", "187", "188", "189"]
    prefix = random.choice(prefixes)
    suffix = "".join(random.choices(string.digits, k=8))
    return f"{prefix}{suffix}"


def generate_random_email(domain: str = None) -> str:
    """生成随机邮箱"""
    if domain is None:
        domains = ["qq.com", "163.com", "126.com", "gmail.com", "outlook.com"]
        domain = random.choice(domains)

    username_length = random.randint(6, 12)
    username = "".join(random.choices(string.ascii_lowercase + string.digits, k=username_length))
    return f"{username}@{domain}"


def generate_random_int(min_val: int = 1, max_val: int = 100) -> int:
    """生成随机整数"""
    return random.randint(min_val, max_val)


def generate_random_float(min_val: float = 1.0, max_val: float = 100.0, decimals: int = 2) -> float:
    """生成随机浮点数"""
    value = random.uniform(min_val, max_val)
    return round(value, decimals)


def generate_random_string(length: int = 10, include_digits: bool = True) -> str:
    """生成随机字符串"""
    chars = string.ascii_letters
    if include_digits:
        chars += string.digits
    return "".join(random.choices(chars, k=length))


def generate_random_date(start_year: int = 2020, end_year: int = None) -> str:
    """生成随机日期字符串"""
    if end_year is None:
        end_year = datetime.now().year
    year = random.randint(start_year, end_year)
    month = random.randint(1, 12)
    day = random.randint(1, 28)  # 使用28避免月份天数问题
    return f"{year}-{month:02d}-{day:02d}"


def generate_random_address() -> str:
    """生成随机地址"""
    cities = ["北京", "上海", "广州", "深圳", "杭州", "成都", "武汉", "西安", "南京", "重庆"]
    streets = ["人民路", "解放路", "建设路", "文化路", "和平路", "中山路", "胜利路", "幸福路"]
    city = random.choice(cities)
    street = random.choice(streets)
    number = random.randint(1, 999)
    return f"{city}{street}{number}号"


def generate_order_sn() -> str:
    """生成订单号"""
    timestamp = int(time.time() * 1000) % 100000000000
    random_str = "".join(random.choices(string.digits, k=4))
    return f"ORDER{timestamp}{random_str}"


def generate_sku() -> str:
    """生成 SKU"""
    timestamp = int(time.time() * 1000) % 100000
    random_str = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f"SKU{timestamp}{random_str}"
