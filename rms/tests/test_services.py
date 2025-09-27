# tests/test_services.py
import logging
from storage import JsonlStorage
from services import RMS

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")

def make_rms(tmp_path) -> RMS:
    root = tmp_path / "data"
    st = JsonlStorage(str(root))
    return RMS(storage=st)

def test_clients_crud_and_search(tmp_path):
    rms = make_rms(tmp_path)

    # create
    c = rms.create_client({
        "Name": "Alice", "Phone": "18800001111",
        "Country": "United States", "City": "New York",
        "State": "NY", "Zip": "10000", "Address1": "addr 1",
        "Address2": "", "Address3": ""
    })
    logging.info("Created client: %s", c)
    assert c["client_id"] == 1

    # update
    updated = rms.update_client(1, {"Phone": "18800002222"})
    logging.info("Updated client: %s", updated)
    assert updated["Phone"] == "18800002222"

    # search (by id / name / phone)
    assert len(rms.search_clients("1")) == 1
    assert len(rms.search_clients("ali")) == 1
    assert len(rms.search_clients("002222")) == 1

    # delete
    rms.delete_client(1)
    logging.info("Deleted client 1")
    assert rms.search_clients("1") == []

def test_airlines_and_flights(tmp_path):
    rms = make_rms(tmp_path)

    c1 = rms.create_client({
        "Name": "Bob", "Phone": "19900001111",
        "Country": "United States", "City": "San Francisco",
        "State": "CA", "Zip": "94016", "Address1": "addr",
        "Address2": "", "Address3": ""
    })
    a1 = rms.create_airline({"CompanyName": "Dream Air"})
    logging.info("Create airline: %s", a1)

    f1 = rms.create_flight({
        "client_id": c1["client_id"],
        "airline_id": a1["airline_id"],
        "Date": "2030-01-02 12:30",
        "StartCity": "San Francisco",
        "EndCity": "New York",
    })
    logging.info("Create flight: %s", f1)
    assert f1["ID"] == 1

    # flights search by name / phone / id
    r_by_name = rms.search_flights("bob")
    logging.info("Search flights by name: %s", r_by_name)
    assert len(r_by_name) == 1

    r_by_phone = rms.search_flights("19900001111")
    logging.info("Search flights by phone: %s", r_by_phone)
    assert len(r_by_phone) == 1

    r_by_id = rms.search_flights(str(c1["client_id"]))
    logging.info("Search flights by client_id: %s", r_by_id)
    assert len(r_by_id) == 1

    # airline search
    r_air = rms.search_airlines("dream")
    logging.info("Search airlines by name: %s", r_air)
    assert len(r_air) == 1
    r_air_id = rms.search_airlines(str(a1["airline_id"]))
    assert len(r_air_id) == 1

    # update + delete
    rms.update_airline(a1["airline_id"], {"CompanyName": "Dream Air Intl"})
    logging.info("Airline after update: %s", rms.search_airlines("intl"))
    rms.delete_airline(a1["airline_id"])
    logging.info("Deleted airline (flights should be removed)")
    assert rms.search_flights("bob") == []
