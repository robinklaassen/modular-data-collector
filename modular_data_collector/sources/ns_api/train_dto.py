from dataclasses import dataclass
from datetime import datetime
from typing import List

from modular_data_collector.sources.source import BaseDTO


@dataclass
class TrainLocation:
    train_id: int
    lat: float
    lng: float
    speed: float
    direction: float
    train_type: str


@dataclass
class TrainDTO(BaseDTO):
    timestamp: datetime
    locations: List[TrainLocation]
