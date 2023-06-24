from typing import List

from influxdb_client import Point

from sources.ais_api.vessel_dto import VesselDTO


def convert_vessels_to_influx(data: VesselDTO) -> List[Point]:
    return [
        Point("vessels")
        .time(vessel.timestamp)
        .tag("name", vessel.name)
        .tag("id", vessel.id)
        .tag("mmsi", vessel.mmsi)
        .tag("imo", vessel.imo)
        .tag("callsign", vessel.callsign)
        .tag("area", vessel.area)
        .tag("type", vessel.type)
        .tag("country", vessel.country)
        .tag("destination", vessel.destination)
        .field("lat", vessel.lat)
        .field("lng", vessel.lng)
        .field("speed", vessel.speed)
        for vessel in data.vessels
    ]
