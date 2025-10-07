# services.py
from typing import Dict, List, Optional, Tuple
import logging
from datetime import datetime

from .models import Client, Airline, Flight
from .storage import JsonlStorage
from .catalogs import COUNTRY_CATALOG, CITY_CATALOG, COUNTRY_TO_CITIES

# import validators.py
from .validators import (
    validate_name,          # -> str
    validate_phone,         # -> str
    validate_zip,           # -> str
    validate_state,         # -> str
    validate_address,       # -> str
    validate_company_name,  # -> str
    validate_datetime,      # -> str（'YYYY-MM-DD HH:MM'）
    validate_country,       # -> str（COUNTRY_CATALOG）
    validate_city           # -> str
)

log = logging.getLogger(__name__)

REQUIRED_CLIENT_FIELDS = ("Name", "Address1", "City", "State", "Zip", "Country", "Phone")


class RMS:
    def __init__(self, storage: Optional[JsonlStorage] = None):
        self.st = storage or JsonlStorage()
        data = self.st.load_all()
        self.clients: List[dict] = data.get("clients", [])
        self.airlines: List[dict] = data.get("airlines", [])
        self.flights: List[dict] = data.get("flights", [])

    # ----------common tools ----------
    def _next_id(self, rows: List[dict], key: str) -> int:
        n = 1
        for r in rows:
            try:
                n = max(n, int(r.get(key, 0)) + 1)
            except Exception:
                pass
        return n

    def _find(self, rows: List[dict], key: str, val: int) -> Optional[dict]:
        for r in rows:
            try:
                if int(r.get(key, -1)) == int(val):
                    return r
            except Exception:
                pass
        return None

    def _index_of(self, rows: List[dict], key: str, val: int) -> Tuple[int, Optional[dict]]:
        for i, r in enumerate(rows):
            try:
                if int(r.get(key, -1)) == int(val):
                    return i, r
            except Exception:
                pass
        return -1, None

    def _maybe_save(self):
        self.st.write_clients(self.clients)
        self.st.write_airlines(self.airlines)
        self.st.write_flights(self.flights)

    def save_all(self)
        self._maybe_save()
        return{
            "clients": len(self.clients),
            "airlines": len(self.airlines),
            "flights": len(self.flights),
        }

    # ----------list citys ----------
    def list_cities(self) -> List[str]:
        return CITY_CATALOG

    def list_countries(self) -> List[str]:
        return sorted(COUNTRY_CATALOG)

    def list_cities_by_country(self, country: str) -> List[str]:
        return COUNTRY_TO_CITIES.get(country, [])

    def list_clients_combo(self) -> List[str]:
        # "client_id - Name (Phone)"
        return [f'{c["client_id"]} - {c.get("Name","")} ({c.get("Phone","")})' for c in self.clients]

    def list_airlines_combo(self) -> List[str]:
        return [f'{a["airline_id"]} - {a.get("CompanyName","")}' for a in self.airlines]

    # =========== Client check and CRUD ===========
    def _validate_client_required(self, data: Dict):
        miss = [k for k in REQUIRED_CLIENT_FIELDS if not str(data.get(k, "")).strip()]
        if miss:
            raise ValueError("Missing required fields: " + ", ".join(miss))

    def _clean_and_validate_client(self, data: Dict) -> Dict:
        """
        Use validators to clean and validate each field,
	    and also check that the city matches the selected country.
        """
        self._validate_client_required(data)

        clean = dict(data)

        clean["Name"] = validate_name(clean.get("Name", ""))
        clean["Phone"] = validate_phone(clean.get("Phone", ""))

        clean["Address1"] = validate_address(clean.get("Address1", ""))
        if clean.get("Address2", ""):
            clean["Address2"] = validate_address(clean.get("Address2", ""))
        if clean.get("Address3", ""):
            clean["Address3"] = validate_address(clean.get("Address3", ""))

        clean["State"] = validate_state(clean.get("State", ""))
        clean["Zip"] = validate_zip(clean.get("Zip", ""))

        country = validate_country(clean.get("Country", ""))
        if country not in COUNTRY_CATALOG:
            raise ValueError(f"Unknown country: {country}")

        city = validate_city(clean.get("City", ""))

        mapped = COUNTRY_TO_CITIES.get(country)
        if mapped:
            if city not in mapped:
                raise ValueError(f"City '{city}' is not in country '{country}' allowed city list")
        else:
            if CITY_CATALOG and city not in CITY_CATALOG:
                log.warning("City '%s' not found in global CITY_CATALOG; accepted as free text.", city)

        clean["Country"] = country
        clean["City"] = city

        clean["Type"] = "client"
        return clean

    def create_client(self, data: Dict) -> Dict:
        clean = self._clean_and_validate_client(data)
        new_id = self._next_id(self.clients, "client_id")
        c = Client(client_id=new_id, **{k: v for k, v in clean.items() if k != "client_id"})
        row = c.to_dict()
        self.clients.append(row)
        self._maybe_save()
        log.info("Create client: %s", row)
        return row

    def update_client(self, client_id: int, patch: Dict) -> Dict:
        idx, row = self._index_of(self.clients, "client_id", client_id)
        if row is None:
            raise KeyError(f"Client {client_id} not found")
        merged = {**row, **patch, "client_id": client_id}
        clean = self._clean_and_validate_client(merged)
        # id & type
        clean["client_id"] = client_id
        clean["Type"] = "client"
        self.clients[idx] = clean
        self._maybe_save()
        log.info("Update client %s -> %s", client_id, clean)
        return clean

    def delete_client(self, client_id: int):
        idx, row = self._index_of(self.clients, "client_id", client_id)
        if row is None:
            raise KeyError(f"Client {client_id} not found")
        # delete flight
        self.clients.pop(idx)
        self.flights = [f for f in self.flights if int(f.get("client_id", 0)) != int(client_id)]
        self._maybe_save()
        log.info("Delete client %s", client_id)

    def search_clients(self, q: str) -> List[Dict]:
        q = (q or "").strip().lower()
        if not q:
            return []
        out: List[Dict] = []
        for r in self.clients:
            if q.isdigit() and int(q) == int(r.get("client_id", 0)):
                out.append(r); continue
            if q in str(r.get("Phone", "")).lower() or q in str(r.get("Name", "")).lower():
                out.append(r)
        log.info("Search clients q=%s -> %d", q, len(out))
        return out

    # =========== Airline check and CRUD ===========
    def _clean_and_validate_airline(self, data: Dict) -> Dict:
        clean = dict(data)
        cname = clean.get("CompanyName", "")
        clean["CompanyName"] = validate_company_name(cname)
        clean["Type"] = "airline"
        return clean

    def create_airline(self, data: Dict) -> Dict:
        clean = self._clean_and_validate_airline(data)
        new_id = self._next_id(self.airlines, "airline_id")
        a = Airline(airline_id=new_id, **{k: v for k, v in clean.items() if k != "airline_id"})
        row = a.to_dict()
        self.airlines.append(row)
        self._maybe_save()
        log.info("Create airline: %s", row)
        return row

    def update_airline(self, airline_id: int, patch: Dict) -> Dict:
        idx, row = self._index_of(self.airlines, "airline_id", airline_id)
        if row is None:
            raise KeyError(f"Airline {airline_id} not found")
        merged = {**row, **patch, "airline_id": airline_id}
        clean = self._clean_and_validate_airline(merged)
        clean["airline_id"] = airline_id
        self.airlines[idx] = clean
        self._maybe_save()
        log.info("Update airline %s -> %s", airline_id, clean)
        return clean

    def delete_airline(self, airline_id: int):
        idx, row = self._index_of(self.airlines, "airline_id", airline_id)
        if row is None:
            raise KeyError(f"Airline {airline_id} not found")
        self.airlines.pop(idx)
        self.flights = [f for f in self.flights if int(f.get("airline_id", 0)) != int(airline_id)]
        self._maybe_save()
        log.info("Delete airline %s", airline_id)

    def search_airlines(self, q: str) -> List[Dict]:
        q = (q or "").strip().lower()
        if not q:
            return []
        out: List[Dict] = []
        for r in self.airlines:
            if q.isdigit() and int(q) == int(r.get("airline_id", 0)):
                out.append(r); continue
            if q in str(r.get("CompanyName", "")).lower():
                out.append(r)
        log.info("Search airlines q=%s -> %d", q, len(out))
        return out

    # =========== Flight check and CRUD ===========
    def _check_fk(self, client_id: int, airline_id: int):
        if not self._find(self.clients, "client_id", client_id):
            raise ValueError(f"client_id {client_id} not found")
        if not self._find(self.airlines, "airline_id", airline_id):
            raise ValueError(f"airline_id {airline_id} not found")

    def _clean_and_validate_flight(self, data: Dict) -> Dict:
        clean = dict(data)
        try:
            cid = int(clean.get("client_id", 0))
            aid = int(clean.get("airline_id", 0))
        except Exception:
            raise ValueError("client_id and airline_id must be integers")
        self._check_fk(cid, aid)

        # date check
        date_str = clean.get("Date", "")
        try:
            datetime.strptime(date_str, "%Y-%m-%d %H:%M")
        except Exception:
            raise ValueError("Date must be 'YYYY-MM-DD HH:MM'")
        #validators
        clean["Date"] = validate_datetime(date_str)

        #check citys valid
        start_city = validate_city(clean.get("StartCity", ""))
        end_city = validate_city(clean.get("EndCity", ""))

        # Optional: strictly enforce
        if CITY_CATALOG:
            if start_city not in CITY_CATALOG:
                log.warning("StartCity '%s' not in CITY_CATALOG; accepted.", start_city)
            if end_city not in CITY_CATALOG:
                log.warning("EndCity '%s' not in CITY_CATALOG; accepted.", end_city)

        clean["client_id"] = cid
        clean["airline_id"] = aid
        clean["StartCity"] = start_city
        clean["EndCity"] = end_city
        clean["Type"] = "flight"
        return clean

    def create_flight(self, data: Dict) -> Dict:
        clean = self._clean_and_validate_flight(data)
        new_id = self._next_id(self.flights, "ID")
        f = Flight(ID=new_id, **{k: v for k, v in clean.items() if k != "ID"})
        row = f.to_dict()
        self.flights.append(row)
        self._maybe_save()
        log.info("Create flight: %s", row)
        return row

    def update_flight(self, flight_id: int, patch: Dict) -> Dict:
        idx, row = self._index_of(self.flights, "ID", flight_id)
        if row is None:
            raise KeyError(f"Flight {flight_id} not found")
        merged = {**row, **patch, "ID": flight_id}
        clean = self._clean_and_validate_flight(merged)
        clean["ID"] = flight_id
        self.flights[idx] = clean
        self._maybe_save()
        log.info("Update flight %s -> %s", flight_id, clean)
        return clean

    def delete_flight(self, flight_id: int):
        idx, row = self._index_of(self.flights, "ID", flight_id)
        if row is None:
            raise KeyError(f"Flight {flight_id} not found")
        self.flights.pop(idx)
        self._maybe_save()
        log.info("Delete flight %s", flight_id)

    # ---------- check flights ----------
    def search_flights(self, q: str) -> List[Dict]:
        q = (q or "").strip().lower()
        if not q:
            return []
        # match client
        matched = []
        for c in self.clients:
            if q.isdigit() and int(q) == int(c.get("client_id", 0)):
                matched.append(c); continue
            if q in c.get("Name", "").lower() or q in c.get("Phone", "").lower():
                matched.append(c)
        ids = {int(c["client_id"]) for c in matched}

        out: List[Dict] = []
        for f in self.flights:
            if int(f.get("client_id", 0)) not in ids:
                continue
            enr = dict(f)
            a = self._find(self.airlines, "airline_id", int(f["airline_id"])) or {}
            c = self._find(self.clients, "client_id", int(f["client_id"])) or {}
            enr["ClientName"] = c.get("Name", "")
            enr["Phone"] = c.get("Phone", "")
            enr["Airline"] = a.get("CompanyName", "")
            out.append(enr)
        log.info("Search flights q=%s -> %d", q, len(out))
        return out
