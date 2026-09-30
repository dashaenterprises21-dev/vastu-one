import json
from functools import lru_cache
from api.config import DEVATAS_FILE, ELEMENTS_FILE


@lru_cache(maxsize=1)
def get_devatas_data():
    with open(DEVATAS_FILE, "r", encoding="utf-8-sig") as f:
        return json.load(f)


@lru_cache(maxsize=1)
def get_elements_data():
    with open(ELEMENTS_FILE, "r", encoding="utf-8-sig") as f:
        return json.load(f)


@lru_cache(maxsize=1)
def get_all_devatas():
    data = get_devatas_data()
    return data["outer_devatas"] + data["inner_devatas"]