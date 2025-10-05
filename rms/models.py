# models.py
from dataclasses import dataclass, field, asdict
from typing import Dict


@dataclass
class Client:
    """客户记录：client_id 为主键"""
    client_id: int
    Type: str = field(default="client")
    Name: str = ""
    Address1: str = ""
    Address2: str = ""
    Address3: str = ""
    City: str = ""
    State: str = ""
    Zip: str = ""
    Country: str = ""
    Phone: str = ""

    def to_dict(self) -> Dict:
        d = asdict(self)
        d["Type"] = "client"
        return d


@dataclass
class Airline:
    """航空公司记录：airline_id 为主键"""
    airline_id: int
    Type: str = field(default="airline")
    CompanyName: str = ""

    def to_dict(self) -> Dict:
        d = asdict(self)
        d["Type"] = "airline"
        return d


@dataclass
class Flight:
    """航班记录：ID 为航班自身主键，client_id/airline_id 为外键"""
    ID: int
    Type: str = field(default="flight")
    client_id: int = 0
    airline_id: int = 0
    Date: str = ""        # "YYYY-MM-DD HH:MM"
    StartCity: str = ""
    EndCity: str = ""

    def to_dict(self) -> Dict:
        d = asdict(self)
        d["Type"] = "flight"
        return d
