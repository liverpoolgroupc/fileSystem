# storage.py
from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Dict, List

log = logging.getLogger(__name__)


class JsonlStorage:
    """
    简单 JSONLines 存储：
      - data/clients.jsonl
      - data/airlines.jsonl
      - data/flights.jsonl
    提供：
      - load_all()  -> {"clients": [...], "airlines": [...], "flights": [...]}
      - save_all(d) -> 覆盖写入三份文件（原子写，避免中途损坏）
    额外：
      - 自动迁移：若历史 flights 记录缺少 ID，会在 load 时补齐递增 ID 并落盘。
    """

    def __init__(self, root: str | Path = "data"):
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)
        self.clients_path = self.root / "clients.jsonl"
        self.airlines_path = self.root / "airlines.jsonl"
        self.flights_path = self.root / "flights.jsonl"

        # 确保文件存在
        for p in (self.clients_path, self.airlines_path, self.flights_path):
            if not p.exists():
                p.write_text("", encoding="utf-8")
        log.info("JsonlStorage initialized at %s", self.root.resolve())

    # ----------------- 公共 API -----------------

    def load_all(self) -> Dict[str, List[dict]]:
        clients = self._read_jsonl(self.clients_path)
        airlines = self._read_jsonl(self.airlines_path)
        flights = self._read_jsonl(self.flights_path)

        # 迁移：给没有 ID 的旧 flight 记录补 ID（与我们新版 Flight.ID 保持一致）
        changed = False
        next_id = 1
        # 先找已有最大 ID
        for f in flights:
            try:
                next_id = max(next_id, int(f.get("ID", 0)) + 1)
            except Exception:
                pass

        for f in flights:
            if "ID" not in f:
                f["ID"] = next_id
                next_id += 1
                changed = True

        if changed:
            log.warning("Migrated flights: missing ID assigned; saving back to disk")
            self._write_jsonl_atomic(self.flights_path, flights)

        log.info("Loaded: clients=%d airlines=%d flights=%d",
                 len(clients), len(airlines), len(flights))
        return {"clients": clients, "airlines": airlines, "flights": flights}

    def save_all(self, data: Dict[str, List[dict]]) -> None:
        self._write_jsonl_atomic(self.clients_path, data.get("clients", []))
        self._write_jsonl_atomic(self.airlines_path, data.get("airlines", []))
        self._write_jsonl_atomic(self.flights_path, data.get("flights", []))
        log.info("Saved: clients=%d airlines=%d flights=%d",
                 len(data.get("clients", [])),
                 len(data.get("airlines", [])),
                 len(data.get("flights", [])))

    # ----------------- 内部工具 -----------------

    @staticmethod
    def _read_jsonl(path: Path) -> List[dict]:
        rows: List[dict] = []
        if not path.exists():
            return rows
        with path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    rows.append(json.loads(line))
                except Exception as e:
                    log.error("Bad JSON line in %s: %r (%s)", path, line, e)
        return rows

    @staticmethod
    def _write_jsonl_atomic(path: Path, rows: List[dict]) -> None:
        """
        原子写：先写到 .tmp，再 replace 到目标文件，避免中途崩溃损坏。
        """
        tmp = path.with_suffix(path.suffix + ".tmp")
        with tmp.open("w", encoding="utf-8", newline="\n") as f:
            for r in rows:
                f.write(json.dumps(r, ensure_ascii=False))
                f.write("\n")
        tmp.replace(path)
