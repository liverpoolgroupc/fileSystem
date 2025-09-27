# tests/test_storage.py
import json
from pathlib import Path
from tempfile import TemporaryDirectory

from storage import JsonlStorage


def write_jsonl(path: Path, rows):
    with path.open("w", encoding="utf-8", newline="\n") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False))
            f.write("\n")


def test_storage_migration_adds_flight_id():
    with TemporaryDirectory() as td:
        st = JsonlStorage(root=td)

        # 写入旧格式（无 ID 的 flights）
        write_jsonl(st.clients_path, [{"ID": 1, "Type": "client", "Name": "A"}])
        write_jsonl(st.airlines_path, [{"ID": 1, "Type": "airline", "CompanyName": "B"}])
        write_jsonl(
            st.flights_path,
            [
                {"Client_ID": 1, "Airline_ID": 1, "Date": "2024-01-01", "StartCity": "X", "EndCity": "Y", "Type": "flight"},
                {"Client_ID": 1, "Airline_ID": 1, "Date": "2024-01-02", "StartCity": "X", "EndCity": "Z", "Type": "flight"},
            ],
        )

        data = st.load_all()
        flights = data["flights"]

        # 迁移后会自动补 ID
        assert len(flights) == 2
        assert all("ID" in f for f in flights)

        # 并回写到磁盘
        data2 = st.load_all()
        assert all("ID" in f for f in data2["flights"])


def test_atomic_save_overwrites_files():
    with TemporaryDirectory() as td:
        st = JsonlStorage(root=td)
        st.save_all({"clients": [], "airlines": [], "flights": []})

        # 第二次写入不同数据，应该覆盖
        st.save_all({
            "clients": [{"ID": 1, "Type": "client", "Name": "A"}],
            "airlines": [{"ID": 2, "Type": "airline", "CompanyName": "B"}],
            "flights": [{"ID": 3, "Type": "flight", "Client_ID": 1, "Airline_ID": 2, "Date": "2024-01-01",
                         "StartCity": "X", "EndCity": "Y"}],
        })

        data = st.load_all()
        assert len(data["clients"]) == 1
        assert len(data["airlines"]) == 1
        assert len(data["flights"]) == 1
