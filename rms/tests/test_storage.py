import os
import shutil
import tempfile
import unittest
import logging

from storage import JsonlStorage

logging.basicConfig(level=logging.INFO, format="[TEST %(levelname)s] %(message)s")


class TestStorage(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp(prefix="rms_storage_")
        logging.info("setup tmpdir=%s", self.tmpdir)
        self.st = JsonlStorage(root=self.tmpdir)

    def tearDown(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)
        logging.info("teardown tmpdir removed")

    def test_write_and_load(self):
        # 初次为空
        data = self.st.load_all()
        logging.info("initial load -> %s", {k: len(v) for k, v in data.items()})
        self.assertEqual(data["clients"], [])
        self.assertEqual(data["airlines"], [])
        self.assertEqual(data["flights"], [])

        # 写入
        clients = [{"client_id": 1, "Type": "client", "Name": "A", "Address1": "", "Address2": "", "Address3": "",
                    "City": "Tokyo", "State": "TK", "Zip": "100", "Country": "Japan", "Phone": "1"}]
        airlines = [{"airline_id": 1, "Type": "airline", "CompanyName": "X"}]
        flights = [{"ID": 1, "Type": "flight", "client_id": 1, "airline_id": 1, "Date": "2025-01-01 00:00",
                    "StartCity": "Tokyo", "EndCity": "Osaka"}]

        self.st.write_clients(clients)
        self.st.write_airlines(airlines)
        self.st.write_flights(flights)

        reloaded = self.st.load_all()
        logging.info("reloaded -> clients=%d airlines=%d flights=%d",
                     len(reloaded["clients"]), len(reloaded["airlines"]), len(reloaded["flights"]))
        self.assertEqual(reloaded["clients"][0]["client_id"], 1)
        self.assertEqual(reloaded["airlines"][0]["airline_id"], 1)
        self.assertEqual(reloaded["flights"][0]["ID"], 1)

    def test_migration_legacy_fields(self):
        # 人工写入老字段，测试迁移
        with open(os.path.join(self.tmpdir, "clients.jsonl"), "w", encoding="utf-8") as f:
            f.write('{"ID": 9, "Name":"OldC"}\n')
        with open(os.path.join(self.tmpdir, "airlines.jsonl"), "w", encoding="utf-8") as f:
            f.write('{"ID": 7, "CompanyName":"OldA"}\n')
        with open(os.path.join(self.tmpdir, "flights.jsonl"), "w", encoding="utf-8") as f:
            f.write('{"Client_ID": 9, "Airline_ID": 7, "Date":"2025-01-01 00:00"}\n')

        data = self.st.load_all()
        logging.info("migrated data -> %s", {k: len(v) for k, v in data.items()})
        self.assertEqual(data["clients"][0]["client_id"], 9)
        self.assertEqual(data["clients"][0]["Type"], "client")
        self.assertEqual(data["airlines"][0]["airline_id"], 7)
        self.assertEqual(data["airlines"][0]["Type"], "airline")
        self.assertEqual(data["flights"][0]["client_id"], 9)
        self.assertEqual(data["flights"][0]["airline_id"], 7)
        self.assertEqual(data["flights"][0]["Type"], "flight")
        self.assertIn("ID", data["flights"][0])  # 无 ID 会补发


if __name__ == "__main__":
    unittest.main()
