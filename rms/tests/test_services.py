# tests/test_services.py
import json
from pathlib import Path
from tempfile import TemporaryDirectory

import pytest

from services import RMS
from storage import JsonlStorage


def make_rms(tmpdir) -> RMS:
    storage = JsonlStorage(root=tmpdir)
    return RMS(storage=storage, autosave=True)


def read_jsonl(path: Path):
    rows = []
    if not path.exists():
        return rows
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rows.append(json.loads(line))
    return rows


def test_client_airline_flight_crud():
    with TemporaryDirectory() as td:
        rms = make_rms(td)

        # --- create client ---
        c = rms.create_client({
            "Type": "client",
            "Name": "Alice",
            "Address1": "A1",
            "City": "NYC",
            "State": "NY",
            "Zip": "10001",
            "Country": "US",
            "Phone": "123"
        })
        assert c["ID"] == 1
        assert c["Type"] == "client"
        assert rms.get_client(1)["Name"] == "Alice"

        # --- create airline ---
        a = rms.create_airline({"Type": "airline", "CompanyName": "UAL"})
        assert a["ID"] == 1
        assert a["CompanyName"] == "UAL"

        # --- create flight (will auto ID) ---
        f = rms.create_flight({
            "Client_ID": c["ID"],
            "Airline_ID": a["ID"],
            "Date": "2024-01-01",
            "StartCity": "NYC",
            "EndCity": "SFO",
        })
        assert "ID" in f and f["ID"] == 1
        assert f["Client_ID"] == c["ID"] and f["Airline_ID"] == a["ID"]

        # --- update client ---
        u = rms.update_client(c["ID"], {"Name": "Alice Chen"})
        assert u["Name"] == "Alice Chen"

        # --- update airline ---
        ua = rms.update_airline(a["ID"], {"CompanyName": "United"})
        assert ua["CompanyName"] == "United"

        # --- update flight (also change foreign keys to same for sanity) ---
        uf = rms.update_flight(f["ID"], {"StartCity": "JFK", "EndCity": "SFO"})
        assert uf["StartCity"] == "JFK"
        # make sure foreign key unchanged
        assert uf["Client_ID"] == c["ID"] and uf["Airline_ID"] == a["ID"]

        # --- delete flight by ID ---
        rms.delete_flight(f["ID"])
        assert rms.get_flight(f["ID"]) is None
        assert all(x["ID"] != f["ID"] for x in rms.flights)

        # --- delete client will cascade-delete its flights (none now) ---
        rms.delete_client(c["ID"])
        assert rms.get_client(c["ID"]) is None

        # --- delete airline will cascade-delete its flights (none now) ---
        rms.delete_airline(a["ID"])
        assert rms.get_airline(a["ID"]) is None

        # verify on-disk files exist and reflect empty data
        root = Path(td)
        clients = read_jsonl(root / "clients.jsonl")
        airlines = read_jsonl(root / "airlines.jsonl")
        flights = read_jsonl(root / "flights.jsonl")
        assert clients == []
        assert airlines == []
        assert flights == []


def test_search_apis():
    with TemporaryDirectory() as td:
        rms = make_rms(td)
        rms.create_client({"Type": "client", "Name": "Alice"})
        rms.create_client({"Type": "client", "Name": "Bob"})
        rms.create_airline({"Type": "airline", "CompanyName": "United"})
        rms.create_airline({"Type": "airline", "CompanyName": "Delta"})

        cs = rms.search_clients("al")
        assert len(cs) == 1 and cs[0]["Name"] == "Alice"
        as_ = rms.search_airlines("ta")
        # "Delta" & "United" -> only "Delta" contains "ta"
        assert len(as_) == 1 and as_[0]["CompanyName"] == "Delta"


def test_create_flight_fk_checks():
    with TemporaryDirectory() as td:
        rms = make_rms(td)
        c = rms.create_client({"Type": "client", "Name": "A"})
        a = rms.create_airline({"Type": "airline", "CompanyName": "B"})

        # ok
        rms.create_flight({
            "Client_ID": c["ID"],
            "Airline_ID": a["ID"],
            "Date": "2024-02-02",
            "StartCity": "X",
            "EndCity": "Y",
        })

        # bad client id
        with pytest.raises(ValueError):
            rms.create_flight({
                "Client_ID": 999,
                "Airline_ID": a["ID"],
                "Date": "2024-02-02",
                "StartCity": "X",
                "EndCity": "Y",
            })

        # bad airline id
        with pytest.raises(ValueError):
            rms.create_flight({
                "Client_ID": c["ID"],
                "Airline_ID": 999,
                "Date": "2024-02-02",
                "StartCity": "X",
                "EndCity": "Y",
            })
