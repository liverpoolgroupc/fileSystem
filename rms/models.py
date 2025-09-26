# models.py
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Dict, Any


def _strip(s: str) -> str:
    return (s or "").strip()


@dataclass
class Client:
    ID: int
    Type: str
    Name: str
    Address1: str = ""
    Address2: str = ""
    Address3: str = ""
    City: str = ""
    State: str = ""
    Zip: str = ""
    Country: str = ""
    Phone: str = ""

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "Client":
        return Client(
            ID=int(d["ID"]),
            Type=_strip(d.get("Type", "client")),
            Name=_strip(d.get("Name", "")),
            Address1=_strip(d.get("Address1", "")),
            Address2=_strip(d.get("Address2", "")),
            Address3=_strip(d.get("Address3", "")),
            City=_strip(d.get("City", "")),
            State=_strip(d.get("State", "")),
            Zip=_strip(d.get("Zip", "")),
            Country=_strip(d.get("Country", "")),
            Phone=_strip(d.get("Phone", "")),
        )

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["Type"] = "client"
        return d


@dataclass
class Airline:
    ID: int
    Type: str
    CompanyName: str

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "Airline":
        return Airline(
            ID=int(d["ID"]),
            Type=_strip(d.get("Type", "airline")),
            CompanyName=_strip(d.get("CompanyName", "")),
        )

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["Type"] = "airline"
        return d


@dataclass
class Flight:
    Client_ID: int
    Airline_ID: int
    Date: str  # ISO8601
    StartCity: str
    EndCity: str

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "Flight":
        # 验证/规范化日期
        date_str = _strip(d.get("Date", ""))
        if date_str:
            # 允许 yyyy-mm-dd 或完整 ISO8601
            try:
                dt = datetime.fromisoformat(date_str)
            except ValueError:
                dt = datetime.strptime(date_str, "%Y-%m-%d")
            date_str = dt.isoformat()
        return Flight(
            Client_ID=int(d["Client_ID"]),
            Airline_ID=int(d["Airline_ID"]),
            Date=date_str,
            StartCity=_strip(d.get("StartCity", "")),
            EndCity=_strip(d.get("EndCity", "")),
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "Client_ID": int(self.Client_ID),
            "Airline_ID": int(self.Airline_ID),
            "Date": self.Date,
            "StartCity": self.StartCity,
            "EndCity": self.EndCity,
            "Type": "flight",
        }
