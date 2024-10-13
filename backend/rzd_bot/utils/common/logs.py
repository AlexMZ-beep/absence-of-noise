from typing import Dict, Any
from uuid import uuid4

from rzd_bot.utils.documents import get_redis_client


def save_logs(_input: Dict[str, Any], _output: Dict[str, Any]):
    log_id = str(uuid4())
    redis_key = f"qna:{log_id}"

    log_data = {
        "input": _input,
        "output": _output
    }

    redis_client = get_redis_client()

    redis_client.json().set(redis_key, '$', log_data)
