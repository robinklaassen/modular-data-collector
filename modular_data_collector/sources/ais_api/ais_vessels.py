import logging
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import (
    Optional,
    Type
)

import requests

from modular_data_collector.sources.ais_api.vessel_dto import VesselDTO, VesselInfo
from modular_data_collector.sources.source import Source, SourceConfig

_logger = logging.getLogger(__name__)


@dataclass
class AISVesselsConfig(SourceConfig):
    # defaults are for Rotterdam port
    base_uri: str = "http://localhost:5000/getVesselsNearMe"
    center_lat: float = 51.8877475
    center_lon: float = 4.3004186
    distance: int = 15  # nautical miles
    request_timeout: int = 10


class AISVessels(Source):
    """
    Self-hosted API from github: https://github.com/transparency-everywhere/ais-api
    It seems from experience that the API returns max 500 records.
    So we should keep the distance small to ensure getting all the ships in the area.
    """

    def __init__(self, config: AISVesselsConfig):
        super().__init__(config)
        self._target_uri = "/".join(
            [config.base_uri, str(config.center_lat), str(config.center_lon), str(config.distance)])
        self._request_timeout = config.request_timeout

        _logger.info("Target URI for AIS API is: %s", self._target_uri)

    @staticmethod
    def config_class() -> Optional[Type[SourceConfig]]:
        return AISVesselsConfig

    def retrieve(self) -> VesselDTO:
        response = requests.get(self._target_uri, timeout=self._request_timeout)
        response.raise_for_status()

        vessels = [self._parse_vessel(d) for d in response.json()]

        _logger.info("Retrieved %d vessels from AIS API.", len(vessels))
        return VesselDTO(vessels=vessels)

    def _parse_vessel(self, data: dict) -> VesselInfo:
        data['lng'] = data.pop('lon')
        data['timestamp'] = datetime.utcfromtimestamp(data['timestamp']).replace(tzinfo=timezone.utc)
        data['speed'] = float(data['speed'])

        return VesselInfo(**data)
