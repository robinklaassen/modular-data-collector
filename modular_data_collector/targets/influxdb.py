import logging
from dataclasses import dataclass
from typing import Optional, Type

from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

from sources.NS.train_dto import TrainDTO
from sources.source import BaseDTO
from modular_data_collector.targets.target import Target, TargetConfig

_logger = logging.getLogger(__name__)


@dataclass
class InfluxDBConfig(TargetConfig):
    url: str
    token: str
    organization: str
    bucket: str


class InfluxDB(Target):

    def __init__(self, target_config: InfluxDBConfig):
        super().__init__(target_config)

        self._url = target_config.url
        self._token = target_config.token
        self._organization = target_config.organization
        self._bucket = target_config.bucket

        self._client = self._create_client()

    @staticmethod
    def config_class() -> Optional[Type[TargetConfig]]:
        return InfluxDBConfig

    def store(self, data: BaseDTO) -> None:
        if isinstance(data, TrainDTO):
            self._store_train_dto(data)

    def _store_train_dto(self, data: TrainDTO) -> None:
        # TODO should consider separating this specific functionality from the generic connection class
        points = [
            Point("train_locations")
                .time(data.timestamp)
                .tag("train_id", loc.id)
                .field("lat", loc.lat)
                .field("lng", loc.lng)
                .field("speed", loc.speed)
                .field("direction", loc.direction)
            for loc in data.locations
        ]

        self._client \
            .write_api(write_options=SYNCHRONOUS) \
            .write(self._bucket, self._organization, points)  # TODO consider async fire-and-forget

        _logger.info("Wrote %d train locations to InfluxDB.", len(points))

    def _create_client(self) -> InfluxDBClient:

        client = InfluxDBClient(url=self._url, token=self._token, org=self._organization)

        if not client.ping():
            raise ConnectionRefusedError(f"Could not connect to InfluxDB at url {self._url}, ping failed.")

        buckets_api = client.buckets_api()

        if buckets_api.find_bucket_by_name(self._bucket) is None:
            # TODO consider creating bucket with retention here if not exists
            raise LookupError(f"Could not find InfluxDB bucket `{self._bucket}`.")

        _logger.info("InfluxDB client created successfully")

        return client
