import sys
from pathlib import Path

# Resolve the absolute path of the current test file (__file__ refers to this script itself)
# This ensures consistency even if the script is run from a different working directory
current_file = Path(__file__).resolve()
# Navigate up two directory levels to get the parent directory of the "tests" folder
# (e.g.: If current_file is "rms/tests/test_rms.py", rms_dir becomes "rms/")
# This points to the directory containing the "services.py" module we need to import
rms_dir = current_file.parent.parent
# Add the rms_dir to Python's system path (sys.path)
# This tells Python where to look for the "services" module when we use `from services import RMS`
sys.path.append(str(rms_dir))

import unittest
from datetime import datetime
from src.services import RMS


# 1. Unit test storage will use this class instead of affecting the actual files
class MockStorage:
    def __init__(self):
        self.clients = []
        self.airlines = []
        self.flights = []
    
    def load_all(self):
        return {
            "clients": self.clients,
            "airlines": self.airlines,
            "flights": self.flights
        }
    
    # Modify Write Action, and not write into actual files
    def write_clients(self, data):
        self.clients = data
    
    def write_airlines(self, data):
        self.airlines = data
    
    def write_flights(self, data):
        self.flights = data