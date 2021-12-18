from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional, Type, Dict, Any


@dataclass
class BaseDTO(ABC):
    ...


@dataclass
class SourceConfig(ABC):
    name: str
    interval_sec: int
    targets: List[Dict[str, Any]]


class Source(ABC):

    def __init__(self, source_config: SourceConfig) -> None:
        self.interval_sec = source_config.interval_sec
        self._config = source_config

    @property
    def name(self) -> str:
        return self.__class__.__name__

    @staticmethod
    def config_class() -> Optional[Type[SourceConfig]]:
        """
        Return the (data)class into which specific agent configurations are
        to be loaded.
        :return: the agent config class.
        """
        # Override this static method in an inheriting class to define in
        # which class the specific configurations are to be loaded.

    @abstractmethod
    def retrieve(self) -> BaseDTO:
        raise NotImplementedError()
