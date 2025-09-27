# tests/test_storage.py
import logging
from pathlib import Path
from storage import JsonlStorage

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")

def test_storage_roundtrip(tmp_path):
    root = tmp_path / "data"
    st = JsonlStorage(str(root))
    # 初始写入
    st.write_clients([{"client_id": 1, "Type": "client", "Name": "A"}])
    st.write_airlines([{"airline_id": 1, "Type": "airline", "CompanyName": "X"}])
    st.write_flights([{"ID": 1, "Type": "flight", "client_id": 1, "airline_id": 1, "Date": "2030-01-01 10:00",
                       "StartCity": "Tokyo", "EndCity": "Osaka"}])
    logging.info("Wrote initial jsonl files")

    data = st.load_all()
    assert len(data["clients"]) == 1
    assert len(data["airlines"]) == 1
    assert len(data["flights"]) == 1
    logging.info("Loaded data sizes: c=%d a=%d f=%d",
                 len(data["clients"]), len(data["airlines"]), len(data["flights"]))

    # 迁移测试（老字段）
    st.write_clients([{"ID": 2, "Name": "B"}])
    st.write_airlines([{"ID": 3, "CompanyName": "Y"}])
    st.write_flights([{"Client_ID": 2, "Airline_ID": 3, "Date": "2031-02-02 12:30",
                       "StartCity": "Paris", "EndCity": "Berlin"}])
    logging.info("Wrote legacy schema rows")

    data2 = st.load_all()
    assert data2["clients"][0]["client_id"] == 2
    assert data2["airlines"][0]["airline_id"] == 3
    assert "ID" in data2["flights"][0]
    logging.info("Migration ensured: client_id=%s airline_id=%s flight_id=%s",
                 data2["clients"][0]["client_id"],
                 data2["airlines"][0]["airline_id"],
                 data2["flights"][0]["ID"])
