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