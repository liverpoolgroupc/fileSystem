import os
import shutil
import tempfile
import unittest
import logging

from services import RMS
from storage import JsonlStorage

logging.basicConfig(level=logging.INFO, format="[TEST %(levelname)s] %(message)s")


class TestRMS(unittest.TestCase):
    def setUp(self):
        # 为测试使用临时 data 目录，避免污染真实数据
        self.tmpdir = tempfile.mkdtemp(prefix="rms_test_")
        logging.info("setup tmpdir=%s", self.tmpdir)
        self.rms = RMS(storage=JsonlStorage(root=self.tmpdir))

    def tearDown(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)
        logging.info("teardown tmpdir removed")

    def test_client_crud_and_search(self):
        # Create client
        c = dict(
            Name="Alice", Phone="123456789",
            Country="Japan", City="Tokyo", State="Tokyo",
            Zip="100", Address1="Chiyoda 1-1", Address2="", Address3=""
        )
        created = self.rms.create_client(c)
        logging.info("created client=%s", created)
        self.assertEqual(created["client_id"], 1)

        # Update
        upd = self.rms.update_client(1, {"Phone": "999"})
        logging.info("updated client=%s", upd)
        self.assertEqual(upd["Phone"], "999")

        # Search by name
        found = self.rms.search_clients("ali")
        logging.info("search by name -> %s", found)
        self.assertTrue(any(r["client_id"] == 1 for r in found))

        # Delete
        self.rms.delete_client(1)
        self.assertFalse(any(r.get("client_id") == 1 for r in self.rms.clients))

    def test_airline_crud_and_search(self):
        a = self.rms.create_airline({"CompanyName": "SkyWays"})
        logging.info("created airline=%s", a)
        self.assertEqual(a["airline_id"], 1)

        upd = self.rms.update_airline(1, {"CompanyName": "SkyWays Intl"})
        logging.info("updated airline=%s", upd)
        self.assertEqual(upd["CompanyName"], "SkyWays Intl")

        found = self.rms.search_airlines("intl")
        logging.info("search airlines -> %s", found)
        self.assertTrue(any(r["airline_id"] == 1 for r in found))

        self.rms.delete_airline(1)
        self.assertFalse(any(r.get("airline_id") == 1 for r in self.rms.airlines))

    def test_flight_crud_and_search(self):
        c = self.rms.create_client(dict(
            Name="Bob", Phone="222",
            Country="United States", City="New York", State="NY",
            Zip="10001", Address1="5th Ave", Address2="", Address3=""
        ))
        a = self.rms.create_airline({"CompanyName": "BlueAir"})

        f = self.rms.create_flight(dict(
            client_id=c["client_id"], airline_id=a["airline_id"],
            Date="2025-01-02 08:30", StartCity="New York", EndCity="Los Angeles"
        ))
        logging.info("created flight=%s", f)
        self.assertEqual(f["ID"], 1)

        upd = self.rms.update_flight(1, {"Date": "2025-01-03 09:00"})
        logging.info("updated flight=%s", upd)
        self.assertEqual(upd["Date"], "2025-01-03 09:00")

        found = self.rms.search_flights("bob")
        logging.info("search flights -> %s", found)
        self.assertTrue(any(r["ID"] == 1 for r in found))

        self.rms.delete_flight(1)
        self.assertFalse(any(r.get("ID") == 1 for r in self.rms.flights))

    def test_list_cities_by_country(self):
        jp_cities = self.rms.list_cities_by_country("Japan")
        logging.info("Japan cities -> %s", jp_cities)
        self.assertIn("Tokyo", jp_cities)
        self.assertNotIn("New York", jp_cities)  # 证明做了过滤


if __name__ == "__main__":
    unittest.main()
