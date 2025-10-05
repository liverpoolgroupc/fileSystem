import sys
from pathlib import Path

# Resolve the absolute path of the current test file (__file__ refers to this script itself)
# Ensures consistency even if the script is run from a different working directory
current_file = Path(__file__).resolve()

# Navigate up two directory levels to get the parent directory of the "tests" folder
# Example: If current_file is "rms/tests/test_rms.py", rms_dir becomes "rms/"
# This points to the directory containing the "services.py" module needed for import
rms_dir = current_file.parent.parent
# Add rms_dir to Python's system path (sys.path)
# Tells Python where to locate the "services" module when using `from src.services import RMS`
sys.path.append(str(rms_dir))

import unittest
from datetime import datetime
from src.services import RMS  # Import the RMS class from the services module

# 1. Mock Storage Class (matches the logic of the original storage module)
# Isolates real file operations to avoid modifying actual disk data during testing
class MockStorage:
    def __init__(self):
        # Initialize empty in-memory lists for each record type
        self.clients = []
        self.airlines = []
        self.flights = []
    
    def load_all(self):
        # Simulate loading data: return current in-memory records
        return {
            "clients": self.clients,
            "airlines": self.airlines,
            "flights": self.flights
        }
    
    # Simulate write operations (only update in-memory data, no disk interaction)
    def write_clients(self, data):
        self.clients = data
    
    def write_airlines(self, data):
        self.airlines = data
    
    def write_flights(self, data):
        self.flights = data
        
        
# 2. Test Class: RMS Utility Methods (_next_id, _find, _index_of)
# Tests helper functions that support core CRUD operations
class TestRMSUtils(unittest.TestCase):
    # Runs before EVERY test method: Initialize a clean RMS instance with MockStorage
    def setUp(self):
        self.mock_storage = MockStorage()
        self.rms = RMS(storage=self.mock_storage)
        print(f"\n=== Starting Test: {self._testMethodName} ===")  # Log test start

    # Runs after EVERY test method: Log test completion
    def tearDown(self):
        print(f"=== Completed Test: {self._testMethodName} (PASSED) ===")

    # Test: _next_id returns 1 when the list is empty
    def test_next_id_empty(self):
        result = self.rms._next_id([], "client_id")
        self.assertEqual(result, 1, "Empty list should return ID=1")
        print(f"Test Details: Empty list → _next_id returned {result} (expected 1)")

    # Test: _next_id returns "max ID + 1" when the list has valid records
    def test_next_id_with_data(self):
        rows = [{"client_id": 3}, {"client_id": 5}]  # Max ID = 5
        result = self.rms._next_id(rows, "client_id")
        self.assertEqual(result, 6, "Non-empty list should return (max ID + 1)")
        print(f"Test Details: Rows with max ID 5 → _next_id returned {result} (expected 6)")

    # Test: _next_id ignores non-numeric IDs and uses the highest valid ID
    def test_next_id_ignore_invalid(self):
        rows = [{"client_id": "abc"}, {"client_id": 2}]  # Invalid ID ("abc") is ignored
        result = self.rms._next_id(rows, "client_id")
        self.assertEqual(result, 3, "Should ignore non-numeric IDs and return (valid max ID + 1)")
        print(f"Test Details: Rows with invalid ID 'abc' → _next_id returned {result} (expected 3)")

    # Test: _find returns the matching record when the target ID exists
    def test_find_exist(self):
        rows = [{"client_id": 2, "Name": "Alice"}]
        result = self.rms._find(rows, "client_id", 2)
        self.assertEqual(result, rows[0], "Should find the record with the target ID")
        print(f"Test Details: Found record for ID 2 → {result} (matches expected record)")

    # Test: _find returns None when the target ID does not exist
    def test_find_not_exist(self):
        rows = [{"client_id": 2}]
        result = self.rms._find(rows, "client_id", 999)  # ID 999 does not exist
        self.assertIsNone(result, "Should return None when the record is not found")
        print(f"Test Details: Search for non-existent ID 999 → _find returned {result} (expected None)")

    # Test: _index_of returns the correct index and record when the target ID exists
    def test_index_of_exist(self):
        rows = [{"airline_id": 5}, {"airline_id": 8}]  # Target ID 8 is at index 1
        index, record = self.rms._index_of(rows, "airline_id", 8)
        self.assertEqual(index, 1, "Should return the correct index of the target record")
        self.assertEqual(record, rows[1], "Should return the record matching the target ID")
        print(f"Test Details: Found ID 8 at index {index} → Record: {record} (expected)")

    # Test: _index_of returns (-1, None) when the target ID does not exist
    def test_index_of_not_exist(self):
        rows = [{"airline_id": 5}]
        index, record = self.rms._index_of(rows, "airline_id", 10)  # ID 10 does not exist
        self.assertEqual(index, -1, "Should return index -1 when record is not found")
        self.assertIsNone(record, "Should return None when record is not found")
        print(f"Test Details: Search for non-existent ID 10 → Index: {index}, Record: {record} (expected (-1, None))")

