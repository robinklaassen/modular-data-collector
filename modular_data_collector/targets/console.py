import logging

from sources.source import BaseDTO
from modular_data_collector.targets.target import Target

_logger = logging.getLogger(__name__)


class Console(Target):

    def store(self, data: BaseDTO) -> None:
        _logger.info("Printing retrieved values to console:")
        print(data)
