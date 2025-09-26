# tests/test_services.py
import tempfile
from storage import JsonlStorage
from services import RMS


def make_rms():
    tmp = tempfile.TemporaryDirectory()
    st = JsonlStorage(base_dir=tmp.name)
    rms = RMS(storage=st)
    return rms, tmp


def test_crud_and_fk():
    rms, tmp = make_rms()

    c = rms.create_client({"Name": "Alice", "Type": "client"})
    a = rms.create_airline({"CompanyName": "ACME Air", "Type": "airline"})
    assert c["ID"] == 1 and a["ID"] == 1

    # 有效外键
    f = rms.create_flight(
        {
            "Client_ID": c["ID"],
            "Airline_ID": a["ID"],
            "Date": "2024-01-01",
            "StartCity": "LHR",
            "EndCity": "JFK",
        }
    )
    assert f["Client_ID"] == 1

    # 搜索
    res = rms.search_clients("ali")
    assert len(res) == 1

    # 删除 client 会清理相关 flight
    rms.delete_client(1)
    assert rms.flights == []
