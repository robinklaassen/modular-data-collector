from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional, Type

from modular_data_collector.sources.source import BaseDTO


@dataclass
class TargetConfig(ABC):
    name: str


class Target(ABC):

    def __init__(self, target_config: TargetConfig) -> None:
        self._config = target_config

    @property
    def name(self) -> str:
        return self.__class__.__name__

    @staticmethod
    def config_class() -> Optional[Type[TargetConfig]]:
        """
        Return the (data)class into which specific agent configurations are
        to be loaded.
        :return: the agent config class.
        """
        # Override this static method in an inheriting class to define in
        # which class the specific configurations are to be loaded.

    @abstractmethod
    def store(self, data: BaseDTO) -> None:
        raise NotImplementedError()
