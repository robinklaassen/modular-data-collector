from dataclasses import dataclass
from datetime import datetime
from typing import List

from sources.source import BaseDTO


@dataclass
class TrainLocation:
    id: int
    lat: float
    lng: float
    speed: float
    direction: float


@dataclass
class TrainDTO(BaseDTO):  # type: ignore
    timestamp: datetime
    locations: List[TrainLocation]
