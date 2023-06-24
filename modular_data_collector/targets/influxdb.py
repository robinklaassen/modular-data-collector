import logging
from dataclasses import dataclass
from typing import Optional, Type

from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS

from converters.trains import convert_trains_to_influx
from converters.vessels import convert_vessels_to_influx
from modular_data_collector.sources.ais_api.vessel_dto import VesselDTO
from modular_data_collector.sources.ns_api.train_dto import TrainDTO
from modular_data_collector.sources.source import BaseDTO
from modular_data_collector.targets.target import Target, TargetConfig

_logger = logging.getLogger(__name__)


@dataclass
class InfluxDBConfig(TargetConfig):
    url: str
    token: str
    organization: str
    bucket: str
    verify_ssl: bool = True


class InfluxDB(Target):

    def __init__(self, target_config: InfluxDBConfig):
        super().__init__(target_config)

        self._url = target_config.url
        self._token = target_config.token
        self._organization = target_config.organization
        self._bucket = target_config.bucket
        self._verify_ssl = target_config.verify_ssl

        self._client = self._create_client()

    @staticmethod
    def config_class() -> Optional[Type[TargetConfig]]:
        return InfluxDBConfig

    def store(self, data: BaseDTO) -> None:
        # TODO auto discover converter functions based on types instead of hard coding
        if isinstance(data, TrainDTO):
            points = convert_trains_to_influx(data)
        elif isinstance(data, VesselDTO):
            points = convert_vessels_to_influx(data)
        else:
            raise AttributeError(f"No converter found for data of class {type(data)}.")

        self._client \
            .write_api(write_options=SYNCHRONOUS) \
            .write(self._bucket, self._organization, points)  # TODO consider async fire-and-forget

        _logger.info("Wrote %d points to InfluxDB.", len(points))

    def _create_client(self) -> InfluxDBClient:

        client = InfluxDBClient(url=self._url, token=self._token, org=self._organization, verify_ssl=self._verify_ssl)

        if not client.ping():
            raise ConnectionRefusedError(f"Could not connect to InfluxDB at url {self._url}, ping failed.")

        buckets_api = client.buckets_api()

        if buckets_api.find_bucket_by_name(self._bucket) is None:
            # TODO consider creating bucket with retention here if not exists
            raise LookupError(f"Could not find InfluxDB bucket `{self._bucket}`.")

        _logger.info("InfluxDB client created successfully")

        return client
