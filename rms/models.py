from dataclasses import dataclass, field, asdict
from typing import Dict


@dataclass
class Client:
    """client record ：client_id as identifier"""
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
    """airline records：airline_id as identifier"""
    airline_id: int
    Type: str = field(default="airline")
    CompanyName: str = ""

    def to_dict(self) -> Dict:
        d = asdict(self)
        d["Type"] = "airline"
        return d