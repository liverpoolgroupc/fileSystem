# services.py
from typing import Dict, List, Optional
from models import Client, Airline, Flight
from storage import JsonlStorage


class RMS:
    """核心业务：内存里维护三个列表，并负责 CRUD / 搜索 / 校验."""

    def __init__(self, storage: Optional[JsonlStorage] = None):
        self.storage = storage or JsonlStorage()
        data = self.storage.load_all()
        self.clients: List[dict] = data["clients"]
        self.airlines: List[dict] = data["airlines"]
        self.flights: List[dict] = data["flights"]

    # --------- 通用工具 ----------
    @staticmethod
    def _next_id(items: List[dict]) -> int:
        max_id = 0
        for r in items:
            try:
                max_id = max(max_id, int(r["ID"]))
            except KeyError:
                pass
        return max_id + 1

    @staticmethod
    def _find(items: List[dict], key: str, value) -> Optional[dict]:
        return next((r for r in items if r.get(key) == value), None)

    # --------- Client ----------
    def create_client(self, d: Dict) -> dict:
        c = Client.from_dict({"ID": d.get("ID") or self._next_id(self.clients), **d})
        if self._find(self.clients, "ID", c.ID):
            raise ValueError("Client ID already exists")
        row = c.to_dict()
        self.clients.append(row)
        return row

    def update_client(self, client_id: int, d: Dict) -> dict:
        r = self._find(self.clients, "ID", client_id)
        if not r:
            raise KeyError("Client not found")
        r.update(Client.from_dict({**r, **d}).to_dict())
        return r

    def delete_client(self, client_id: int) -> None:
        self.clients[:] = [r for r in self.clients if r["ID"] != client_id]
        # 同步清理相关 Flight
        self.flights[:] = [f for f in self.flights if f["Client_ID"] != client_id]

    def get_client(self, client_id: int) -> Optional[dict]:
        return self._find(self.clients, "ID", client_id)

    # --------- Airline ----------
    def create_airline(self, d: Dict) -> dict:
        a = Airline.from_dict({"ID": d.get("ID") or self._next_id(self.airlines), **d})
        if self._find(self.airlines, "ID", a.ID):
            raise ValueError("Airline ID already exists")
        row = a.to_dict()
        self.airlines.append(row)
        return row

    def update_airline(self, airline_id: int, d: Dict) -> dict:
        r = self._find(self.airlines, "ID", airline_id)
        if not r:
            raise KeyError("Airline not found")
        r.update(Airline.from_dict({**r, **d}).to_dict())
        return r

    def delete_airline(self, airline_id: int) -> None:
        self.airlines[:] = [r for r in self.airlines if r["ID"] != airline_id]
        self.flights[:] = [f for f in self.flights if f["Airline_ID"] != airline_id]

    def get_airline(self, airline_id: int) -> Optional[dict]:
        return self._find(self.airlines, "ID", airline_id)

    # --------- Flight ----------
    def create_flight(self, d: Dict) -> dict:
        f = Flight.from_dict(d)
        # 外键校验
        if not self.get_client(f.Client_ID):
            raise ValueError("Client_ID does not exist")
        if not self.get_airline(f.Airline_ID):
            raise ValueError("Airline_ID does not exist")
        row = f.to_dict()
        self.flights.append(row)
        return row

    def delete_flight(self, idx: int) -> None:
        # 简化：以索引删除；现实可用复合键
        if idx < 0 or idx >= len(self.flights):
            raise IndexError("Flight index out of range")
        del self.flights[idx]

    # --------- 查询 ----------
    def search_clients(self, keyword: str) -> List[dict]:
        k = keyword.lower().strip()
        return [c for c in self.clients if k in c.get("Name", "").lower()]

    def search_airlines(self, keyword: str) -> List[dict]:
        k = keyword.lower().strip()
        return [a for a in self.airlines if k in a.get("CompanyName", "").lower()]

    def save(self) -> None:
        self.storage.save_all(
            {"clients": self.clients, "airlines": self.airlines, "flights": self.flights}
        )
