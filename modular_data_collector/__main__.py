import logging
import sys
from typing import (
    Any,
    Dict,
    Optional,
)

import conf
import jsons
from jsons.exceptions import DeserializationError, SignatureMismatchError

from modular_data_collector.config import Config
from modular_data_collector.scheduler import create_scheduler

_logger = logging.getLogger(__name__)


def main(conf_dict: Optional[Dict[str, Any]] = None) -> None:

    conf_dict = conf_dict or conf.asdict()
    config = _setup_config(conf_dict)

    if config is None:
        sys.exit(1)

    logging.basicConfig(level=config.log_level,
                        format='%(asctime)s | %(name)-50s | %(levelname)-5s | %(message)s',
                        stream=sys.stdout)

    _logger.info("Running with config: %s", config)

    scheduler = create_scheduler(config)
    scheduler.start()


def _setup_config(conf_dict: Dict[str, Any]) -> Optional[Config]:
    # Set up the config or return None upon failure.
    result = None
    try:
        result = jsons.load(conf_dict, cls=Config, strict=True)
    except SignatureMismatchError as err:
        print(f'Invalid setting for argument: `{err.argument}`',
              file=sys.stderr)
    except DeserializationError as err:
        print(err.message)
    return result


if __name__ == "__main__":
    main()
