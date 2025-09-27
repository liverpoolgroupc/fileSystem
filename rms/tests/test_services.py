# test_services.py
import json
import os
import pytest

from storage import JsonlStorage
from services import RMS


def load_jsonl(path):
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return [json.loads(x) for x in f.read().splitlines() if x.strip()]


def mk_rms(tmp_path):
    st = JsonlStorage(root=str(tmp_path / "data"))
    return RMS(st)


def valid_client(**kw):
    base = dict(
        Name="Alice",
        Address1="A-1",
        Address2="A-2",
        Address3="A-3",
        City="Tokyo",
        State="TY",
        Zip="100-0001",
        Country="JP",
        Phone="090-0000-0000",
    )
    base.update(kw)
    return base


def test_client_crud_and_persistence(tmp_path):
    rms = mk_rms(tmp_path)

    # create -> 立刻写盘
    c1 = rms.create_client(valid_client())
    assert c1["client_id"] == 1

    clients_path = rms.st.clients_path
    on_disk = load_jsonl(clients_path)
    assert len(on_disk) == 1 and on_disk[0]["client_id"] == 1

    # update -> 立刻写盘
    rms.update_client(1, valid_client(Name="Alice X", Phone="123"))
    on_disk = load_jsonl(clients_path)
    assert on_disk[0]["Name"] == "Alice X" and on_disk[0]["Phone"] == "123"

    # delete -> 同时删除其 flights
    a1 = rms.create_airline({"CompanyName": "UA"})
    f1 = rms.create_flight({
        "client_id": 1,
        "airline_id": a1["airline_id"],
        "Date": "2025-01-02 08:30",
        "StartCity": "Tokyo",
        "EndCity": "New York",
    })
    assert f1["ID"] == 1

    rms.delete_client(1)
    # 客户被删
    assert load_jsonl(clients_path) == []
    # 名下航班被删
    assert load_jsonl(rms.st.flights_path) == []


def test_client_required_validation(tmp_path):
    rms = mk_rms(tmp_path)
    with pytest.raises(ValueError):
        rms.create_client(valid_client(Name=""))   # Name 为空
    with pytest.raises(ValueError):
        rms.create_client(valid_client(City=""))   # City 为空


def test_airline_and_flight_crud(tmp_path):
    rms = mk_rms(tmp_path)
    c = rms.create_client(valid_client())
    a = rms.create_airline({"CompanyName": "DL"})

    # create flight
    f = rms.create_flight({
        "client_id": c["client_id"],
        "airline_id": a["airline_id"],
        "Date": "2026-05-06 13:35",
        "StartCity": "Tokyo",
        "EndCity": "Paris",
    })
    assert f["ID"] == 1

    # update flight
    f2 = rms.update_flight(1, {
        "client_id": c["client_id"],
        "airline_id": a["airline_id"],
        "Date": "2026-05-06 14:00",
        "StartCity": "Tokyo",
        "EndCity": "London",
    })
    assert f2["EndCity"] == "London"

    # delete flight
    rms.delete_flight(1)
    assert load_jsonl(rms.st.flights_path) == []


def test_flight_fk_validation(tmp_path):
    rms = mk_rms(tmp_path)
    c = rms.create_client(valid_client())
    a = rms.create_airline({"CompanyName": "LH"})

    # 错的 client_id
    with pytest.raises(ValueError):
        rms.create_flight({
            "client_id": 999,
            "airline_id": a["airline_id"],
            "Date": "2025-01-01 00:00",
            "StartCity": "A",
            "EndCity": "B",
        })
    # 错的 airline_id
    with pytest.raises(ValueError):
        rms.create_flight({
            "client_id": c["client_id"],
            "airline_id": 999,
            "Date": "2025-01-01 00:00",
            "StartCity": "A",
            "EndCity": "B",
        })


def test_client_search(tmp_path):
    rms = mk_rms(tmp_path)
    c1 = rms.create_client(valid_client(Name="Alice", Phone="1111"))
    c2 = rms.create_client(valid_client(Name="Bob", Phone="2222"))

    # by id
    rs = rms.search_clients(str(c1["client_id"]))
    assert len(rs) == 1 and rs[0]["Name"] == "Alice"

    # by phone
    rs = rms.search_clients("2222")
    assert len(rs) == 1 and rs[0]["Name"] == "Bob"

    # by name (lowercase)
    rs = rms.search_clients("alice")
    assert len(rs) == 1 and rs[0]["Phone"] == "1111"


def test_flight_search_and_search_by_fk(tmp_path):
    rms = mk_rms(tmp_path)
    c1 = rms.create_client(valid_client(Name="Alice", Phone="1111"))
    c2 = rms.create_client(valid_client(Name="Bob", Phone="2222"))
    a1 = rms.create_airline({"CompanyName": "UA"})
    a2 = rms.create_airline({"CompanyName": "DL"})

    rms.create_flight({
        "client_id": c1["client_id"], "airline_id": a1["airline_id"],
        "Date": "2025-01-01 08:00", "StartCity": "Tokyo", "EndCity": "NY"
    })
    rms.create_flight({
        "client_id": c1["client_id"], "airline_id": a2["airline_id"],
        "Date": "2025-01-02 09:00", "StartCity": "Tokyo", "EndCity": "LA"
    })
    rms.create_flight({
        "client_id": c2["client_id"], "airline_id": a2["airline_id"],
        "Date": "2025-02-03 10:00", "StartCity": "Paris", "EndCity": "London"
    })

    # 普通搜索：按 client name / phone / id
    rs = rms.search_flights("alice")
    assert len(rs) == 2 and all(r["ClientName"] == "Alice" for r in rs)

    rs = rms.search_flights("2222")
    assert len(rs) == 1 and rs[0]["ClientName"] == "Bob"

    # 按 client_id + airline_id 搜索
    rs = rms.search_flights_by_fk(c1["client_id"], a2["airline_id"])
    assert len(rs) == 1 and rs[0]["Airline"] == "DL"
