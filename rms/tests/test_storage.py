# tests/test_storage.py
import os
import tempfile
from storage import JsonlStorage


def test_roundtrip_jsonl():
    with tempfile.TemporaryDirectory() as d:
        st = JsonlStorage(base_dir=d)
        data = {
            "clients": [{"ID": 1, "Type": "client", "Name": "Alice"}],
            "airlines": [{"ID": 10, "Type": "airline", "CompanyName": "ACME Air"}],
            "flights": [
                {
                    "Client_ID": 1,
                    "Airline_ID": 10,
                    "Date": "2024-01-02",
                    "StartCity": "LON",
                    "EndCity": "NYC",
                    "Type": "flight",
                }
            ],
        }
        st.save_all(data)
        out = st.load_all()
        assert out == data
        # 文件存在
        for f in ("clients.jsonl", "airlines.jsonl", "flights.jsonl"):
            assert os.path.exists(os.path.join(d, f))
