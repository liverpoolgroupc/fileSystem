# services.py
import logging
from typing import Dict, List, Optional
from models import Client, Airline, Flight
from storage import JsonlStorage

log = logging.getLogger(__name__)


class RMS:
    def __init__(self, storage: Optional[JsonlStorage] = None, autosave: bool = True):
        self.storage = storage or JsonlStorage()
        self.autosave = autosave
        data = self.storage.load_all()
        self.clients: List[dict] = data["clients"]
        self.airlines: List[dict] = data["airlines"]
        self.flights: List[dict] = data["flights"]
        log.info("RMS initialized: clients=%d, airlines=%d, flights=%d",
                 len(self.clients), len(self.airlines), len(self.flights))

    # ---------- 工具 ----------
    @staticmethod
    def _next_id(items: List[dict], key: str = "ID") -> int:
        max_id = 0
        for r in items:
            try:
                max_id = max(max_id, int(r.get(key, 0)))
            except Exception:
                pass
        return max_id + 1

    @staticmethod
    def _find(items: List[dict], key: str, value) -> Optional[dict]:
        return next((r for r in items if r.get(key) == value), None)

    def _maybe_save(self):
        if self.autosave:
            self.save()

    # ---------- Client ----------
    def create_client(self, d: Dict) -> dict:
        new_id = d.get("ID") or self._next_id(self.clients)
        c = Client.from_dict({"ID": new_id, **d})
        if self._find(self.clients, "ID", c.ID):
            log.error("Create client failed: duplicate ID=%s", c.ID)
            raise ValueError("Client ID already exists")
        row = c.to_dict()
        self.clients.append(row)
        log.info("Client created: %s", row)
        self._maybe_save()
        return row

    def update_client(self, client_id: int, d: Dict) -> dict:
        r = self._find(self.clients, "ID", client_id)
        if not r:
            log.error("Update client failed: not found ID=%s", client_id)
            raise KeyError("Client not found")
        before = dict(r)
        r.update(Client.from_dict({**r, **d, "ID": client_id}).to_dict())
        log.info("Client updated: id=%s before=%s after=%s", client_id, before, r)
        self._maybe_save()
        return r

    def delete_client(self, client_id: int) -> None:
        cnt_before = len(self.clients)
        self.clients[:] = [r for r in self.clients if r["ID"] != client_id]
        flights_before = len(self.flights)
        self.flights[:] = [f for f in self.flights if f["Client_ID"] != client_id]
        log.info("Client deleted: id=%s (clients %d->%d, flights %d->%d)",
                 client_id, cnt_before, len(self.clients), flights_before, len(self.flights))
        self._maybe_save()

    def get_client(self, client_id: int) -> Optional[dict]:
        return self._find(self.clients, "ID", client_id)

    def search_clients(self, keyword: str) -> List[dict]:
        k = (keyword or "").lower().strip()
        res = [c for c in self.clients if k in c.get("Name", "").lower()]
        log.info("Search clients: key=%r -> %d rows", keyword, len(res))
        return res

    # ---------- Airline ----------
    def create_airline(self, d: Dict) -> dict:
        new_id = d.get("ID") or self._next_id(self.airlines)
        a = Airline.from_dict({"ID": new_id, **d})
        if self._find(self.airlines, "ID", a.ID):
            log.error("Create airline failed: duplicate ID=%s", a.ID)
            raise ValueError("Airline ID already exists")
        row = a.to_dict()
        self.airlines.append(row)
        log.info("Airline created: %s", row)
        self._maybe_save()
        return row

    def update_airline(self, airline_id: int, d: Dict) -> dict:
        r = self._find(self.airlines, "ID", airline_id)
        if not r:
            log.error("Update airline failed: not found ID=%s", airline_id)
            raise KeyError("Airline not found")
        before = dict(r)
        r.update(Airline.from_dict({**r, **d, "ID": airline_id}).to_dict())
        log.info("Airline updated: id=%s before=%s after=%s", airline_id, before, r)
        self._maybe_save()
        return r

    def delete_airline(self, airline_id: int) -> None:
        cnt_before = len(self.airlines)
        self.airlines[:] = [r for r in self.airlines if r["ID"] != airline_id]
        flights_before = len(self.flights)
        self.flights[:] = [f for f in self.flights if f["Airline_ID"] != airline_id]
        log.info("Airline deleted: id=%s (airlines %d->%d, flights %d->%d)",
                 airline_id, cnt_before, len(self.airlines), flights_before, len(self.flights))
        self._maybe_save()

    def get_airline(self, airline_id: int) -> Optional[dict]:
        return self._find(self.airlines, "ID", airline_id)

    def search_airlines(self, keyword: str) -> List[dict]:
        k = (keyword or "").lower().strip()
        res = [a for a in self.airlines if k in a.get("CompanyName", "").lower()]
        log.info("Search airlines: key=%r -> %d rows", keyword, len(res))
        return res

    # ---------- Flight ----------
    def create_flight(self, d: Dict) -> dict:
        # 外键校验
        client_id = int(d["Client_ID"])
        airline_id = int(d["Airline_ID"])
        c = self.get_client(client_id)
        if not c:
            log.error("Create flight failed: Client_ID=%s not exists", client_id)
            raise ValueError("Client_ID does not exist")
        a = self.get_airline(airline_id)
        if not a:
            log.error("Create flight failed: Airline_ID=%s not exists", airline_id)
            raise ValueError("Airline_ID does not exist")

        new_id = d.get("ID") or self._next_id(self.flights, "ID")
        f = Flight.from_dict({"ID": new_id, **d})
        row = f.to_dict()
        self.flights.append(row)
        log.info("Flight created: %s (linked Client: %s, Airline: %s)",
                 row, c.get("Name"), a.get("CompanyName"))
        self._maybe_save()
        return row

    def update_flight(self, flight_id: int, d: Dict) -> dict:
        r = self._find(self.flights, "ID", flight_id)
        if not r:
            log.error("Update flight failed: not found ID=%s", flight_id)
            raise KeyError("Flight not found")
        # 如果改了外键则重新校验
        cid = int(d.get("Client_ID", r["Client_ID"]))
        aid = int(d.get("Airline_ID", r["Airline_ID"]))
        if not self.get_client(cid):
            log.error("Update flight failed: Client_ID=%s not exists", cid)
            raise ValueError("Client_ID does not exist")
        if not self.get_airline(aid):
            log.error("Update flight failed: Airline_ID=%s not exists", aid)
            raise ValueError("Airline_ID does not exist")

        before = dict(r)
        r.update(Flight.from_dict({**r, **d, "ID": flight_id,
                                   "Client_ID": cid, "Airline_ID": aid}).to_dict())
        log.info("Flight updated: id=%s before=%s after=%s", flight_id, before, r)
        self._maybe_save()
        return r

    def delete_flight(self, flight_id: int) -> None:
        before = len(self.flights)
        removed = self._find(self.flights, "ID", flight_id)
        if not removed:
            log.error("Delete flight failed: id=%s not found", flight_id)
            raise KeyError("Flight not found")
        self.flights[:] = [f for f in self.flights if f["ID"] != flight_id]
        log.info("Flight deleted: id=%s (flights %d->%d) row=%s",
                 flight_id, before, len(self.flights), removed)
        self._maybe_save()

    def get_flight(self, flight_id: int) -> Optional[dict]:
        return self._find(self.flights, "ID", flight_id)

    # ---------- 保存 ----------
    def save(self) -> None:
        self.storage.save_all({
            "clients": self.clients,
            "airlines": self.airlines,
            "flights": self.flights
        })
        log.info("Saved to disk: clients=%d airlines=%d flights=%d",
                 len(self.clients), len(self.airlines), len(self.flights))
