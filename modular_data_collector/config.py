from dataclasses import dataclass, field
from typing import (
    Any,
    Dict,
    List,
)


@dataclass
class Config:
    log_level: str = 'INFO'

    sources: List[Dict[str, Any]] = field(default_factory=list)

    def __post_init__(self) -> None:
        # Perform some validations on the given config.
        assert self.log_level in ('CRITICAL', 'FATAL', 'ERROR', 'WARNING', 'WARN', 'INFO', 'DEBUG', 'NOTSET'), \
            self._msg('log_level', self.log_level, 'it must be a valid loglevel from `logging`.')

    def _msg(self, name: str, value: object, msg: str) -> str:
        return f'Invalid setting for `{name}` (`{value}`): {msg}'
