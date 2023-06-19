from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from modular_data_collector.sources.source import BaseDTO

"""
{
"name": "BRISK",
"id": "7806936",
"lat": 51.739,
"lon": 3.847502,
"timestamp": 1687160902,
"mmsi": "244373614",
"imo": "0",
"callsign": "PB7515",
"speed": 0.1,
"area": "UKC - UK Coast & Atlantic",
"type": "Sailing Vessel",
"country": "Netherlands",
"destination": "No data (CLASS B transponder)",
"port_current_id": "1401",
"port_current": "SCHARENDIJKE",
"port_next_id": null,
"port_next": null
},
"""


@dataclass
class VesselInfo:
    name: str
    id: str
    lat: float
    lon: float
    timestamp: datetime
    mmsi: str
    imo: str
    callsign: str
    speed: float
    area: Optional[str]
    type: Optional[str]
    country: str
    destination: Optional[str]


@dataclass
class VesselDTO(BaseDTO):
    vessels: List[VesselInfo]
