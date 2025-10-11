## Record Management System (RMS)

This README complements the technical documentation by providing practical details on system setup, structure, and execution.
It outlines the key steps required to install, run, and package the Record Management System (RMS) and serves as a technical reference for reproducing or evaluating the software.
---

## 1. Overview

The Record Management System (RMS) is a desktop application developed in Python using the **Tkinter** library. It is designed to manage three categories of records for a specialist travel agency:

- **Clients** – customer profiles
- **Airlines** – carrier records
- **Flights** – links between clients and airlines

Data are stored in **JSONL** format (one JSON object per line).
The application supports full **CRUD** (Create, Read, Update, Delete) functionality with immediate data persistence, foreign-key validation (ensuring flights reference existing clients and airlines), and confirmation dialogues for record creation and deletion. System logs are printed to the console.

## 2. Key Features

**Clients**
- Validation of required fields: *Name, Phone, Country, City, State, ZIP, Address1*

**Airlines**
- Basic CRUD functionality with search by *airline_id* or company name

**Flights**
- Date and time selectors (Year/Month/Day Hour:Minute)
- Drop-down menus for start and end cities
- Search by *client_id*, client name, or phone number

**Additional Features**
- Country list (50+ entries) sorted alphabetically
- Cities filtered according to selected country
- Read-only fields (IDs and Types) displayed in dark grey
- Automatic migration of legacy schemas (e.g. *ID → client_id / airline_id*)

## 3. Project Structure

rms
    ├── data
    │   ├── airlines.jsonl   #airline record
    │   ├── clients.jsonl    #client record
    │   └── flights.jsonl    #flight record
    ├── docs
    |
    |
    |---dist
    |    |__MacOS       #MacOS RMS.app
    |    |
    |    |__Windows     #Windows RMS.exe
    |
    ├── src
    │   ├── app.py       # GUI entry (Tkinter)
    │   ├── catalogs.py  # Country list (50+) and country→cities map
    │   ├── models.py    # Dataclasses for Client / Airline / Flight
    │   ├── services.py  # Business logic: CRUD / search / validation / dropdowns
    |   ├── validators.py#Field Normalization & Validation
    │   └── storage.py   # JSONL I/O + schema migration + bundle seeding
    └── tests  #unit test codes

**3.1 Data storage path**
- When run from an IDE, data are written to the local `rms/data` directory.
- When packaged:
  - macOS: `~/Library/Application Support/RMS`
  - Windows: `%APPDATA%/RMS`

---

## 4. Installation and Execution

** 4.1 Prerequisites
- Python **3.10 – 3.13**
- Tkinter (bundled with CPython)
- `pytest` for unit testing

** 4.2 Environment Setup and Execution
cd rms
python -m venv .venv
# macOS / Linux
source .venv/bin/activate
# Windows (PowerShell)
# .venv\Scripts\Activate.ps1

python -m pip install -U pip
python -m pip install pytest

python app.py

## Run Tests
- cd rms
- python -m tests.test_rms

## 6 Packing

** 6.1 MacOS
python -m pip install pyinstaller

pyinstaller \
  --clean --noconfirm \
  --windowed \
  --name RMS \
  --paths rms/src \
  --add-data "rms/data:data" \
  rms/src/app.py

** 6.2 Windows
python -m pip install pyinstaller

run command in the cmd.exe

<!-- pyinstaller ^
  --clean --noconfirm ^
  --windowed ^
  --name RMS ^
  --paths rms\src ^
  --add-data "rms\data;data" ^
  rms\src\app.py -->

run command in the PowerShell

<!-- pyinstaller `
  --clean --noconfirm `
  --windowed `
  --name RMS `
  --paths rms\src `
  --add-data "rms\data;data" `
  rms\src\app.py -->

  <!-- pyinstaller `
  --clean --noconfirm `
  --windowed `
  --name RMS `
  --paths src `
  --add-data "data;data" `
  src\app.py -->

Window build script :

pyinstaller ^
  --clean --noconfirm ^
  --onefile ^
  --name RMS ^
  --windowed ^
  --paths src ^
  --hidden-import services ^
  --hidden-import models ^
  --hidden-import storage ^
  --hidden-import catalogs ^
  --hidden-import validators ^
  --add-data "data;data" ^
  --hidden-import=tkinter ^
  --hidden-import=_tkinter ^
  --collect-all tkinter ^
  src\app.py

## 7 Troubleshooting

- **pyinstaller: command not found** → run `python -m pip install pyinstaller`
- **No GUI / Tk 8.5 warning on macOS** → use Python 3.10+ that ships with Tk 8.6+
- **attempted relative import with no known parent package** → imports in `app.py` are absolute (a small `sys.path` shim is included)
- **Data not updating** → check the effective data root in logs; packaged mode writes to the user directory listed above

## 8 !!!!!!!!!!!!!!!!! Important Notes !!!!!!!!!!!!!!!!!!!
## Alternative Solution when failed to run .exe file in window envoirnment

1.use terminal to change directory to rms folder

2.use the following command in terminal : python -m src.app

## 9 Run unit test

1 . cd to rms
2. use the following command python -m unittest tests.test_rms

## 10 Project Contributors

This project was developed collaboratively by **Group C** as part of the MSc Software Engineering Programme.
Team members (in alphabetical order): **Matteo Crotta, Ilona Diomidova, Liu Dushi, Kieran Karuna, and Yeung Ka Chun**.

---

## 11 License

This software was developed for educational purposes as part of the **MSc Data Science and Artificial Intelligence**
**Module CSCK541 – Software Development in Practice**. It is distributed under the **MIT License**, which permits reuse, modification, and distribution with appropriate attribution.

---

