import logging
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, Type, Dict, Any

import requests

from sources.NS.train_dto import TrainLocation, TrainDTO
from modular_data_collector.sources.source import Source, SourceConfig

_logger = logging.getLogger(__name__)


@dataclass
class NSVehiclesConfig(SourceConfig):
    api_key: str
    request_timeout: int = 10


class NSVehicles(Source):
    """
    API documentation: https://apiportal.ns.nl/docs/services/virtual-train-api/operations/getVehicles?
    """
    base_uri = 'https://gateway.apiportal.ns.nl/virtual-train-api/api/vehicle'

    def __init__(self, config: NSVehiclesConfig):
        super().__init__(config)
        self._api_key = config.api_key
        self._request_timeout = config.request_timeout

    @staticmethod
    def config_class() -> Optional[Type[SourceConfig]]:
        return NSVehiclesConfig

    def retrieve(self) -> TrainDTO:
        timestamp = datetime.utcnow()
        r = requests.get(self.base_uri,
                         headers={'Ocp-Apim-Subscription-Key': self._api_key},
                         timeout=self._request_timeout)
        r.raise_for_status()

        train_locations = self._convert(r.json()['payload']['treinen'])
        _logger.info("Retrieved %d vehicles from NS API.", len(train_locations))
        return TrainDTO(timestamp, train_locations)

    def _convert(self, source_data: List[Dict[str, Any]]) -> List[TrainLocation]:
        return [
            TrainLocation(
                id=t['treinNummer'],
                lat=t['lat'],
                lng=t['lng'],
                speed=t['snelheid'],
                direction=t['richting'],
            )
            for t in source_data
        ]
