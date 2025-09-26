# storage.py
import json
import os
from typing import Dict, List


DEFAULT_DIR = os.path.join(os.path.dirname(__file__), "data")
FILES = {
    "clients": os.path.join(DEFAULT_DIR, "clients.jsonl"),
    "airlines": os.path.join(DEFAULT_DIR, "airlines.jsonl"),
    "flights": os.path.join(DEFAULT_DIR, "flights.jsonl"),
}


class JsonlStorage:
    """简单 JSONL 存储。每行一条 dict。"""

    def __init__(self, base_dir: str = DEFAULT_DIR):
        self.base_dir = base_dir
        if not os.path.isdir(base_dir):
            os.makedirs(base_dir, exist_ok=True)
        # 确保文件存在
        for path in FILES.values():
            if not os.path.exists(path):
                open(path, "a", encoding="utf-8").close()

    def load_all(self) -> Dict[str, List[dict]]:
        out = {"clients": [], "airlines": [], "flights": []}
        for key, path in FILES.items():
            with open(path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        out[key].append(json.loads(line))
        return out

    def save_all(self, data: Dict[str, List[dict]]) -> None:
        for key, path in FILES.items():
            items = data.get(key, [])
            with open(path, "w", encoding="utf-8") as f:
                for row in items:
                    f.write(json.dumps(row, ensure_ascii=False) + "\n")
