from inspect import isabstract
from typing import (
    List,
    Set,
    Type,
)

from barentsz import discover

from modular_data_collector.sources.source import Source as _Source

ALL: Set[Type[_Source]] = set(discover(what=List[_Source], exclude=isabstract))
