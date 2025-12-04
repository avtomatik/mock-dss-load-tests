import hashlib
import random
import string
from datetime import datetime


def generate_current_date_str() -> str:
    return datetime.now().strftime("%Y-%m-%d")


def generate_random_content() -> str:
    return hashlib.md5(str(random.random()).encode("utf-8")).hexdigest()


def generate_random_id(length: int = 8) -> str:
    return "".join(
        random.choices(string.ascii_letters + string.digits, k=length)
    )
