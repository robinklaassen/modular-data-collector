from dataclasses import dataclass
from typing import Optional, Type

from modular_data_collector.sources.source import SourceConfig, Source, BaseDTO
from modular_data_collector.targets.target import TargetConfig, Target


@dataclass
class MockSourceConfig(SourceConfig):
    ...


@dataclass
class MockTargetConfig(TargetConfig):
    ...


class MockSource(Source):

    @staticmethod
    def config_class() -> Optional[Type[SourceConfig]]:
        return MockSourceConfig

    def retrieve(self) -> BaseDTO:
        pass


class MockTarget(Target):

    @staticmethod
    def config_class() -> Optional[Type[TargetConfig]]:
        return MockTargetConfig

    def store(self, data: BaseDTO) -> None:
        pass