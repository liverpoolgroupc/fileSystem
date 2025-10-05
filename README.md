#fileSystem

1) Overview

RMS is a small desktop GUI app (Tkinter) for managing three record types:

Clients (customer profiles)

Airlines (carrier list)

Flights (links a client to an airline)

Data is stored as JSONL (one JSON per line). The app supports Create / Update / Delete / Search, immediate persistence (save on every change), FK validation (flight must reference existing client & airline), and confirm dialogs for create/delete. Logs are printed to the console.

2) Key Features

Clients: required fields validation (Name, Phone, Country, City, State, Zip, Address1).

Airlines: simple CRUD with search by airline_id / company name.

Flights: date/time pickers (Y/M/D H:M), city drop-downs, and search by client_id / client name / phone.

Drop-downs:

Countries (50+), alphabetically sorted.

Cities filtered by selected country.

Read-only fields (IDs and Types) are displayed in darker gray.

Data files auto-migrate older schemas (e.g., ID → client_id / airline_id).

3) Project Structure

rms
    ├── data
    │   ├── airlines.jsonl   #airline record
    │   ├── clients.jsonl    #client record
    │   └── flights.jsonl    #flight record
    ├── docs
    ├── src
    │   ├── app.py       # GUI entry (Tkinter)
    │   ├── catalogs.py  # Country list (50+) and country→cities map
    │   ├── models.py    # Dataclasses for Client / Airline / Flight
    │   ├── services.py  # Business logic: CRUD / search / validation / dropdowns
    │   └── storage.py   # JSONL I/O + schema migration + bundle seeding
    └── tests  #unit test codes

4) Getting Started
4.1 Requirements

Python 3.10 – 3.13 recommended

Tkinter (ships with CPython on most systems)

pytest for tests

4.2 Setup & Run
cd rms
python -m venv .venv
# macOS / Linux
source .venv/bin/activate
# Windows (PowerShell)
# .venv\Scripts\Activate.ps1

python -m pip install -U pip
python -m pip install pytest

python app.py


5) Run Tests



6) Troubleshooting

pyinstaller: command not found → python -m pip install pyinstaller

No GUI / Tk 8.5 warning on macOS → use Python 3.10+ that ships with Tk 8.6+

attempted relative import with no known parent package → imports in app.py are absolute (a small sys.path shim is included).

Data not updating → check effective data root in logs; packaged mode writes to user directory listed above.
