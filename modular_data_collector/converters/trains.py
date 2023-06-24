from typing import List

from influxdb_client import Point

from sources.ns_api.train_dto import TrainDTO


def convert_trains_to_influx(data: TrainDTO) -> List[Point]:
    return [
        Point("train_locations")
        .time(data.timestamp)
        .tag("train_id", loc.train_id)
        .tag("train_type", loc.train_type)
        .field("lat", loc.lat)
        .field("lng", loc.lng)
        .field("speed", loc.speed)
        .field("direction", loc.direction)
        for loc in data.locations
    ]
