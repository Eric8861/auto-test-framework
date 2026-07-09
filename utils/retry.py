import time
import functools


def retry(max_times=3, interval=1, exceptions=(AssertionError,)):
    """重试装饰器：业务操作（如上下架/删除）失败时自动重试"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, max_times + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exc = e
                    if attempt < max_times:
                        time.sleep(interval)
            raise last_exc
        return wrapper
    return decorator
