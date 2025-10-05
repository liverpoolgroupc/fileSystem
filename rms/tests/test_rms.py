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
        
# 3. Test Class: Client Management Functions (create/update/delete/search)
# Tests end-to-end client record operations
class TestRMSClient(unittest.TestCase):
    def setUp(self):
        self.mock_storage = MockStorage()
        self.rms = RMS(storage=self.mock_storage)
        print(f"\n=== Starting Test: {self._testMethodName} ===")

    def tearDown(self):
        print(f"=== Completed Test: {self._testMethodName} (PASSED) ===")

    # Test: Create a valid client record (all required fields provided)
    def test_create_client_valid(self):
        # Valid client data (includes all required fields)
        client_data = {
            "Name": "Bob",
            "Address1": "Street A",
            "City": "HK",
            "State": "HK",
            "Zip": "123",
            "Country": "HK",
            "Phone": "123456"
        }
        result = self.rms.create_client(client_data)
        
        # Validate return value and in-memory state
        self.assertEqual(result["Type"], "client", "Client record 'Type' should be 'client'")
        self.assertEqual(result["client_id"], 1, "First client created should have ID=1")
        self.assertEqual(result["Name"], "Bob", "Client name should match input")
        self.assertEqual(len(self.rms.clients), 1, "Client list should have 1 new record")
        
        print(f"Test Details: Created client with ID {result['client_id']} (Name: {result['Name']})")
        print(f"Client list size after creation: {len(self.rms.clients)} (expected 1)")

    # Test: Create client fails when required fields are missing (raises ValueError)
    def test_create_client_missing_fields(self):
        # Invalid data: missing required fields (Address1, City, Country)
        invalid_data = {"Name": "Bob", "Phone": "123456"}
        
        # Verify ValueError is raised with correct message
        with self.assertRaises(ValueError) as exc_context:
            self.rms.create_client(invalid_data)
        error_msg = str(exc_context.exception)
        self.assertIn("Missing required fields", error_msg, "Error should mention missing required fields")
        
        print(f"Test Details: Missing required fields → Error raised: '{error_msg}' (expected)")
        print(f"Client list size remains: {len(self.rms.clients)} (expected 0)")

    # Test: Update an existing client record with valid data
    def test_update_client_valid(self):
        # Step 1: Create a base client first
        self.rms.create_client({
            "Name": "Bob",
            "Address1": "Street A",
            "City": "HK",
            "State": "HK",
            "Zip": "123",
            "Country": "HK",
            "Phone": "123456"  # Original phone number
        })
        
        # Step 2: Update the client's phone number
        update_data = {"Phone": "654321"}  # New phone number
        result = self.rms.update_client(client_id=1, patch=update_data)
        
        # Validate update result
        self.assertEqual(result["Phone"], "654321", "Client phone number should be updated")
        self.assertEqual(self.rms.clients[0]["Phone"], "654321", "In-memory client list should sync the update")
        
        print(f"Test Details: Updated client ID 1 → New phone: {result['Phone']} (expected '654321')")

    # Test: Update fails when the client ID does not exist (raises KeyError)
    def test_update_client_not_exist(self):
        # Try to update client ID 999 (never created)
        with self.assertRaises(KeyError) as exc_context:
            self.rms.update_client(client_id=999, patch={"Name": "New Name"})
        error_msg = str(exc_context.exception)
        self.assertIn("Client 999 not found", error_msg, "Error should say client ID 999 is not found")
        
        print(f"Test Details: Update non-existent client 999 → Error raised: '{error_msg}' (expected)")

    # Test: Delete a client and all associated flights (referential integrity)
    def test_delete_client(self):
        # Step 1: Create dependent records (client → airline → flight linked to client)
        self.rms.create_client({
            "Name": "Bob",
            "Address1": "Street A",
            "City": "HK",
            "State": "HK",
            "Zip": "123",
            "Country": "HK",
            "Phone": "123456"
        })
        self.rms.create_airline({"CompanyName": "Cathay"})
        self.rms.create_flight({
            "client_id": 1,  # Linked to client ID 1
            "airline_id": 1,
            "Date": "2024-12-31 23:59",
            "StartCity": "HK",
            "EndCity": "London"
        })
        
        # Step 2: Delete the client (ID 1)
        self.rms.delete_client(client_id=1)
        
        # Validate deletion (client and associated flight are removed)
        self.assertEqual(len(self.rms.clients), 0, "Client should be deleted")
        self.assertEqual(len(self.rms.flights), 0, "Associated flights should be deleted too")
        
        print(f"Test Details: Deleted client ID 1 → Client list size: {len(self.rms.clients)} (0), Flight list size: {len(self.rms.flights)} (0)")

    # Test: Search clients by keyword (matches ID, Name, or Phone substring)
    def test_search_clients(self):
        # Create a test client for searching
        self.rms.create_client({
            "Name": "Alice",
            "Address1": "Street B",
            "City": "SH",
            "State": "SH",
            "Zip": "456",
            "Country": "CN",
            "Phone": "13800138000"
        })
        
        # Test different search keywords
        search_by_id = self.rms.search_clients("1")  # Search by client ID (1)
        search_by_name = self.rms.search_clients("ali")  # Search by name substring ("ali" in "Alice")
        search_by_phone = self.rms.search_clients("138")  # Search by phone substring ("138" in "13800138000")
        search_no_match = self.rms.search_clients("bob")  # No matching client
        
        # Validate search results
        self.assertEqual(len(search_by_id), 1, "Search by ID '1' should find 1 client")
        self.assertEqual(len(search_by_name), 1, "Search by name 'ali' should find 1 client")
        self.assertEqual(len(search_by_phone), 1, "Search by phone '138' should find 1 client")
        self.assertEqual(len(search_no_match), 0, "Search for 'bob' should return 0 results")
        
        print(f"Test Details: Search results → ID '1': {len(search_by_id)}, Name 'ali': {len(search_by_name)}, Phone '138': {len(search_by_phone)}, 'bob': {len(search_no_match)}")


