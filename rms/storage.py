# storage.py
import io
import json
import logging
import os
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Dict, List

log = logging.getLogger(__name__)


def _default_data_dir() -> str:
    """
    返回用户可写的数据目录：
      - macOS: ~/Library/Application Support/RMS
      - Windows: %APPDATA%/RMS
      - Linux: ~/.local/share/RMS
    """
    home = Path.home()
    if sys.platform == "darwin":
        return str(home / "Library" / "Application Support" / "RMS")
    elif os.name == "nt":
        appdata = os.environ.get("APPDATA", str(home / "AppData" / "Roaming"))
        return str(Path(appdata) / "RMS")
    else:
        return str(home / ".local" / "share" / "RMS")


def _resource_path(rel: str) -> Path:
    """
    打包/开发均可用的资源定位：
      - PyInstaller onefile: sys._MEIPASS 为临时解压目录
      - PyInstaller onedir/.app: 可执行同级目录
      - 源码运行: 当前文件所在目录
    """
    base = Path(getattr(sys, "_MEIPASS", Path(sys.executable).parent))
    if not getattr(sys, "frozen", False):  # 源码模式
        base = Path(__file__).resolve().parent
    return (base / rel).resolve()


class JsonlStorage:
    """
    简单 JSONL 存储。提供：
      - 数据放用户可写目录（避免 .app 内只读）
      - 首次运行可从打包资源 data/ 拷贝模板
      - 原子写
      - 启动时一次性迁移老字段：
        clients: ID -> client_id
        airlines: ID -> airline_id
        flights: Client_ID/Airline_ID -> client_id/airline_id；无 ID 时补发
    """

    def __init__(self, root=None):
        # 若未显式传入，使用用户数据目录；兼容传入 "data" 等相对路径
        self.root = str(Path(root).expanduser().resolve()) if root else _default_data_dir()
        os.makedirs(self.root, exist_ok=True)

        self.clients_path = os.path.join(self.root, "clients.jsonl")
        self.airlines_path = os.path.join(self.root, "airlines.jsonl")
        self.flights_path = os.path.join(self.root, "flights.jsonl")

        # 第一次运行：如用户目录没有文件，尝试从打包资源 data/ 里拷贝模板（如果有）
        self._seed_from_bundle_if_empty()

        log.info("JsonlStorage data root: %s", self.root)

    # --------------------- 首次拷贝模板 ---------------------
    def _seed_from_bundle_if_empty(self):
        need = []
        for name in ("clients.jsonl", "airlines.jsonl", "flights.jsonl"):
            dst = os.path.join(self.root, name)
            if not os.path.exists(dst):
                need.append(name)

        if not need:
            return

        bundle_data_dir = _resource_path("data")  # 需要你打包时用 --add-data "data:data" 携带
        if not bundle_data_dir.exists() or not bundle_data_dir.is_dir():
            # 没有随包模板也没关系：后续写入会创建空文件
            return

        for name in need:
            src = bundle_data_dir / name
            dst = os.path.join(self.root, name)
            if src.exists():
                shutil.copy2(str(src), dst)
                log.info("Seeded %s from bundle", name)

    # --------------------- 基础 I/O ---------------------
    def _read_jsonl(self, path: str) -> List[dict]:
        if not os.path.exists(path):
            return []
        out: List[dict] = []
        with io.open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    out.append(json.loads(line))
                except Exception as e:
                    log.warning("Bad jsonl line in %s: %s", path, e)
        return out

    def _write_jsonl_atomic(self, path: str, rows: List[dict]):
        tmp_fd, tmp_path = tempfile.mkstemp(prefix=".tmp_", dir=self.root)
        with os.fdopen(tmp_fd, "w", encoding="utf-8") as f:
            for r in rows:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        os.replace(tmp_path, path)

    # --------------------- 读取 + 迁移 ---------------------
    def load_all(self) -> Dict[str, List[dict]]:
        clients = self._read_jsonl(self.clients_path)
        airlines = self._read_jsonl(self.airlines_path)
        flights = self._read_jsonl(self.flights_path)

        migrated = False

        # clients: ID -> client_id
        for c in clients:
            if "client_id" not in c and "ID" in c:
                c["client_id"] = c.pop("ID")
                migrated = True
            c.setdefault("Type", "client")

        # airlines: ID -> airline_id
        for a in airlines:
            if "airline_id" not in a and "ID" in a:
                a["airline_id"] = a.pop("ID")
                migrated = True
            a.setdefault("Type", "airline")

        # flights: Client_ID/Airline_ID -> client_id/airline_id；无 ID 补
        next_fid = 1
        for f in flights:
            if "Client_ID" in f and "client_id" not in f:
                f["client_id"] = f.pop("Client_ID")
                migrated = True
            if "Airline_ID" in f and "airline_id" not in f:
                f["airline_id"] = f.pop("Airline_ID")
                migrated = True
            f.setdefault("Type", "flight")
            if "ID" in f:
                try:
                    n = int(f["ID"])
                    if n + 1 > next_fid:
                        next_fid = n + 1
                except Exception:
                    pass

        for f in flights:
            if "ID" not in f:
                f["ID"] = next_fid
                next_fid += 1
                migrated = True

        if migrated:
            log.warning("JsonlStorage: migrated legacy fields -> new schema")
            self._write_jsonl_atomic(self.clients_path, clients)
            self._write_jsonl_atomic(self.airlines_path, airlines)
            self._write_jsonl_atomic(self.flights_path, flights)

        log.info("Loaded: clients=%d airlines=%d flights=%d",
                 len(clients), len(airlines), len(flights))
        return {"clients": clients, "airlines": airlines, "flights": flights}

    # --------------------- 单表写入 ---------------------
    def write_clients(self, rows: List[dict]):
        self._write_jsonl_atomic(self.clients_path, rows)

    def write_airlines(self, rows: List[dict]):
        self._write_jsonl_atomic(self.airlines_path, rows)

    def write_flights(self, rows: List[dict]):
        self._write_jsonl_atomic(self.flights_path, rows)
