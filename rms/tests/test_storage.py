# test_storage.py
import json
from storage import JsonlStorage


def write_jsonl(p, rows):
    with open(p, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def read_all(path):
    with open(path, "r", encoding="utf-8") as f:
        return [json.loads(x) for x in f.read().splitlines() if x.strip()]


def test_load_all_migrates_legacy_fields(tmp_path):
    # 构造 legacy 数据
    root = tmp_path / "data"
    root.mkdir()

    clients_path = root / "clients.jsonl"
    airlines_path = root / "airlines.jsonl"
    flights_path = root / "flights.jsonl"

    write_jsonl(clients_path, [
        {"ID": 1, "Type": "client", "Name": "Alice", "Phone": "111"}
    ])
    write_jsonl(airlines_path, [
        {"ID": 9, "Type": "airline", "CompanyName": "UA"}
    ])
    write_jsonl(flights_path, [
        {
            "Type": "flight",
            "Client_ID": 1,
            "Airline_ID": 9,
            "Date": "2025-01-02 08:30",
            "StartCity": "New York",
            "EndCity": "Tokyo"
        }
    ])

    st = JsonlStorage(root=str(root))
    data = st.load_all()

    # 已迁移：ID->client_id / airline_id；航班补了 ID
    cl = data["clients"][0]
    al = data["airlines"][0]
    fl = data["flights"][0]

    assert cl["client_id"] == 1 and cl["Type"] == "client"
    assert al["airline_id"] == 9 and al["Type"] == "airline"
    assert fl["client_id"] == 1 and fl["airline_id"] == 9 and fl["Type"] == "flight"
    assert "ID" in fl and isinstance(fl["ID"], int)

    # 文件应被写回为新字段，再读验证
    clients2 = read_all(clients_path)
    airlines2 = read_all(airlines_path)
    flights2 = read_all(flights_path)

    assert "client_id" in clients2[0] and "ID" not in clients2[0]
    assert "airline_id" in airlines2[0] and "ID" not in airlines2[0]
    assert "client_id" in flights2[0] and "Client_ID" not in flights2[0]
    assert "airline_id" in flights2[0] and "Airline_ID" not in flights2[0]
    assert "ID" in flights2[0]  # 航班自身 ID 持久化
