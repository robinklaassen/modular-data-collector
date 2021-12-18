from inspect import isabstract
from typing import (
    List,
    Set,
    Type,
)

from barentsz import discover

from modular_data_collector.targets.target import Target as _Target

ALL: Set[Type[_Target]] = set(discover(what=List[_Target], exclude=isabstract))
