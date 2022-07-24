from __future__ import annotations

from threading import Lock
from typing import Any, Dict, Type


class Singleton(type):
    """Credits go to https://www.linkedin.com/pulse/writing-thread-safe-singleton-class-python-saurabh-singh/"""

    _instances: Dict[Type, Any] = {}

    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]
