# storage.py
import io
import json
import logging
import os
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Dict, List, Optional

log = logging.getLogger(__name__)

def _default_data_dir() -> str:
    """
    Return path when a user saved the file：
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
    Resource locator compatible with both packaging and development modes:
      - PyInstaller onefile: sys._MEIPASS is the temporary extraction directory
      - PyInstaller onedir/.app: same directory as the executable
      - Source code execution: directory of the current script
    """
    base = Path(getattr(sys, "_MEIPASS", Path(sys.executable).parent))
    if not getattr(sys, "frozen", False):  
        base = Path(__file__).resolve().parent
    return (base / rel).resolve()


def _dev_project_data_dir(max_up: int = 5) -> Optional[str]:
    """
    When running from source code, starting from the location of storage.py, check in order:
    The data/ directory in the current folder (usually src/).

    Then the parent folder, grandparent folder, and so on—up to max_up levels—for a data/ directory.

    If a data/ directory is found, return its path; otherwise return None.
    """
    here = Path(__file__).resolve().parent
    candidates = [here] + list(here.parents[:max_up])
    for base in candidates:
        cand = base / "data"
        log.debug("probe data dir: %s", cand)
        if cand.exists() and cand.is_dir():
            log.info("Dev mode: use project data dir: %s", cand)
            return str(cand)
    return None


class JsonlStorage:
    """
    Simple JSONL saving. Provides:
    - Stores data in a user-writable directory (to avoid read-only .app contents)
    - Uses atomic write operations
    - On first run, copies template from packaged resource directory `data/`
    - Migrates legacy fields on startup:
        clients: ID -> client_id
        airlines: ID -> airline_id
        flights: Client_ID/Airline_ID -> client_id/airline_id; generates missing IDs if absent
    """

    def __init__(self, root: Optional[str] = None):
        # Priority order: explicit root > (not frozen and project data/ exists) > user-level directory.
        if root:
            self.root = str(Path(root).expanduser().resolve())
            log.info("JsonlStorage root (explicit): %s", self.root)
        else:
            if getattr(sys, "frozen", False):
                # Packaged mode: always write to the user-level directory.
                self.root = _default_data_dir()
            else:
                # Source mode: if the project’s data/ is found, use it; otherwise use the user-level directory.
                dev = _dev_project_data_dir()
                self.root = dev if dev else _default_data_dir()

        os.makedirs(self.root, exist_ok=True)

        self.clients_path = os.path.join(self.root, "clients.jsonl")
        self.airlines_path = os.path.join(self.root, "airlines.jsonl")
        self.flights_path = os.path.join(self.root, "flights.jsonl")

        # First run: If the user's directory doesn't contain the file, attempt to copy the template from the packaged resource folder data/ (if available).
        self._seed_from_bundle_if_empty()

        log.info("JsonlStorage data root: %s", self.root)

    # --------------------- Firt Model ---------------------
    def _seed_from_bundle_if_empty(self):
        if not getattr(sys, "frozen", False):
            return

        need = []
        for name in ("clients.jsonl", "airlines.jsonl", "flights.jsonl"):
            dst = os.path.join(self.root, name)
            if not os.path.exists(dst):
                need.append(name)

        if not need:
            return

        bundle_data_dir = _resource_path("data")  # Needed when you package --add-data "data:data" contains
        if not bundle_data_dir.exists() or not bundle_data_dir.is_dir():
            # No bundled template? No problem — an empty file will be created during future writes.
            return

        for name in need:
            src = bundle_data_dir / name
            dst = os.path.join(self.root, name)
            if src.exists():
                shutil.copy2(str(src), dst)
                log.info("Seeded %s from bundle", name)

    # --------------------- Basic I/O ---------------------
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

    # --------------------- Read + Move ---------------------
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

        # flights: Client_ID/Airline_ID -> client_id/airline_id；If No Id, then Fill it
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

    # --------------------- Write into Json ---------------------
    def write_clients(self, rows: List[dict]):
        self._write_jsonl_atomic(self.clients_path, rows)

    def write_airlines(self, rows: List[dict]):
        self._write_jsonl_atomic(self.airlines_path, rows)

    def write_flights(self, rows: List[dict]):
        self._write_jsonl_atomic(self.flights_path, rows)