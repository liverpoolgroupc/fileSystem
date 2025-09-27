# services.py
from typing import Dict, List, Optional, Tuple
import logging

from models import Client, Airline, Flight
from storage import JsonlStorage

log = logging.getLogger(__name__)

# 下拉“城市/国家”目录
CITY_CATALOG = [
    "New York", "San Francisco", "Los Angeles",
    "Tokyo", "Osaka",
    "Beijing", "Shanghai", "Shenzhen",
    "London", "Paris"
]
COUNTRY_CATALOG = ["US", "JP", "CN", "UK", "FR", "DE", "CA", "AU", "SG", "KR"]

REQUIRED_CLIENT_FIELDS = ("Name", "Address1", "City", "State", "Zip", "Country", "Phone")


class RMS:
    def __init__(self, storage: Optional[JsonlStorage] = None):
        self.st = storage or JsonlStorage()
        data = self.st.load_all()
        self.clients: List[dict] = data.get("clients", [])
        self.airlines: List[dict] = data.get("airlines", [])
        self.flights: List[dict] = data.get("flights", [])

    # ---------- 公共小工具 ----------
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

    # ---------- 下拉数据 ----------
    def list_cities(self) -> List[str]:
        return CITY_CATALOG

    def list_countries(self) -> List[str]:
        return COUNTER_CATALOG if (COUNTER_CATALOG := COUNTRY_CATALOG) else COUNTRY_CATALOG

    def list_clients_combo(self) -> List[str]:
        # "client_id - Name (Phone)"
        return [f'{c["client_id"]} - {c.get("Name","")} ({c.get("Phone","")})' for c in self.clients]

    def list_airlines_combo(self) -> List[str]:
        return [f'{a["airline_id"]} - {a.get("CompanyName","")}' for a in self.airlines]

    # ---------- 客户 ----------
    def _validate_client_required(self, data: Dict):
        miss = [k for k in REQUIRED_CLIENT_FIELDS if not str(data.get(k, "")).strip()]
        if miss:
            raise ValueError("Missing required fields: " + ", ".join(miss))

    def create_client(self, data: Dict) -> Dict:
        data["Type"] = "client"
        self._validate_client_required(data)
        new_id = self._next_id(self.clients, "client_id")
        c = Client(client_id=new_id, **{k: v for k, v in data.items() if k != "client_id"})
        self.clients.append(c.to_dict())
        self._maybe_save()
        log.info("Create client: %s", c.to_dict())
        return c.to_dict()

    def update_client(self, client_id: int, patch: Dict) -> Dict:
        idx, row = self._index_of(self.clients, "client_id", client_id)
        if row is None:
            raise KeyError(f"Client {client_id} not found")
        merged = {**row, **patch, "Type": "client", "client_id": client_id}
        self._validate_client_required(merged)
        self.clients[idx] = merged
        self._maybe_save()
        log.info("Update client %s -> %s", client_id, merged)
        return merged

    def delete_client(self, client_id: int):
        idx, row = self._index_of(self.clients, "client_id", client_id)
        if row is None:
            raise KeyError(f"Client {client_id} not found")
        # 同时删除其名下的航班
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
        return out

    # ---------- 航空公司 ----------
    def create_airline(self, data: Dict) -> Dict:
        data["Type"] = "airline"
        new_id = self._next_id(self.airlines, "airline_id")
        a = Airline(airline_id=new_id, **{k: v for k, v in data.items() if k != "airline_id"})
        self.airlines.append(a.to_dict())
        self._maybe_save()
        log.info("Create airline: %s", a.to_dict())
        return a.to_dict()

    def update_airline(self, airline_id: int, patch: Dict) -> Dict:
        idx, row = self._index_of(self.airlines, "airline_id", airline_id)
        if row is None:
            raise KeyError(f"Airline {airline_id} not found")
        merged = {**row, **patch, "Type": "airline", "airline_id": airline_id}
        self.airlines[idx] = merged
        self._maybe_save()
        log.info("Update airline %s -> %s", airline_id, merged)
        return merged

    def delete_airline(self, airline_id: int):
        idx, row = self._index_of(self.airlines, "airline_id", airline_id)
        if row is None:
            raise KeyError(f"Airline {airline_id} not found")
        self.airlines.pop(idx)
        self.flights = [f for f in self.flights if int(f.get("airline_id", 0)) != int(airline_id)]
        self._maybe_save()
        log.info("Delete airline %s", airline_id)

    # ---------- 航班 ----------
    def _check_fk(self, client_id: int, airline_id: int):
        if not self._find(self.clients, "client_id", client_id):
            raise ValueError(f"client_id {client_id} not found")
        if not self._find(self.airlines, "airline_id", airline_id):
            raise ValueError(f"airline_id {airline_id} not found")

    def create_flight(self, data: Dict) -> Dict:
        data["Type"] = "flight"
        self._check_fk(int(data["client_id"]), int(data["airline_id"]))
        new_id = self._next_id(self.flights, "ID")
        f = Flight(ID=new_id, **{k: v for k, v in data.items() if k != "ID"})
        self.flights.append(f.to_dict())
        self._maybe_save()
        log.info("Create flight: %s", f.to_dict())
        return f.to_dict()

    def update_flight(self, flight_id: int, patch: Dict) -> Dict:
        idx, row = self._index_of(self.flights, "ID", flight_id)
        if row is None:
            raise KeyError(f"Flight {flight_id} not found")
        merged = {**row, **patch, "Type": "flight", "ID": flight_id}
        self._check_fk(int(merged["client_id"]), int(merged["airline_id"]))
        self.flights[idx] = merged
        self._maybe_save()
        log.info("Update flight %s -> %s", flight_id, merged)
        return merged

    def delete_flight(self, flight_id: int):
        idx, row = self._index_of(self.flights, "ID", flight_id)
        if row is None:
            raise KeyError(f"Flight {flight_id} not found")
        self.flights.pop(idx)
        self._maybe_save()
        log.info("Delete flight %s", flight_id)

    # ---------- 航班查询 ----------
    def search_flights_by_client(self, client_id: int) -> List[Dict]:
        out: List[Dict] = []
        for f in self.flights:
            if int(f.get("client_id", 0)) != int(client_id):
                continue
            enr = dict(f)
            c = self._find(self.clients, "client_id", int(f["client_id"])) or {}
            a = self._find(self.airlines, "airline_id", int(f["airline_id"])) or {}
            enr["ClientName"] = c.get("Name", "")
            enr["Phone"] = c.get("Phone", "")
            enr["Airline"] = a.get("CompanyName", "")
            out.append(enr)
        return out

    def search_flights(self, q: str) -> List[Dict]:
        q = (q or "").strip().lower()
        if not q:
            return []
        # 先找出匹配客户
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
        return out

    def search_flights_by_fk(self, client_id: int, airline_id: int) -> List[Dict]:
        out: List[Dict] = []
        for f in self.flights:
            if int(f.get("client_id", 0)) == int(client_id) and int(f.get("airline_id", 0)) == int(airline_id):
                enr = dict(f)
                a = self._find(self.airlines, "airline_id", int(f["airline_id"])) or {}
                c = self._find(self.clients, "client_id", int(f["client_id"])) or {}
                enr["ClientName"] = c.get("Name", "")
                enr["Phone"] = c.get("Phone", "")
                enr["Airline"] = a.get("CompanyName", "")
                out.append(enr)
        return out
