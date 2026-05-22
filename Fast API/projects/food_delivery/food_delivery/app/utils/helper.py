from datetime import datetime


def current_timestamp() -> datetime:
    return datetime.utcnow()


def paginate(query_list: list, skip: int = 0, limit: int = 10) -> list:
    return query_list[skip: skip + limit]


def normalize_string(value: str) -> str:
    return value.strip().lower() if value else value
