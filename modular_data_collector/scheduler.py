import logging
from typing import (
    Callable,
    Dict,
    List,
)

import jsons
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

import modular_data_collector.sources as sources_pkg
import modular_data_collector.targets as targets_pkg
from modular_data_collector.config import Config
from modular_data_collector.sources.source import Source
from modular_data_collector.targets.target import Target

_logger = logging.getLogger(__name__)


def create_scheduler(config: Config) -> BlockingScheduler:
    job_dict = _construct_job_dict(config)

    sched = BlockingScheduler()

    for source, targets in job_dict.items():
        _logger.info("Adding job from `%s` to `%s`", source.name, [target.name for target in targets])
        job = _create_job(source, targets)
        sched.add_job(job, trigger=CronTrigger(second=f"*/{source.interval_sec}"))

    return sched


def _construct_job_dict(config: Config) -> Dict[Source, List[Target]]:
    output: Dict[Source, List[Target]] = {}

    for source_dict in config.sources:
        source_cls = [s for s in sources_pkg.ALL if s.__name__ == source_dict['name']][0]
        source_config = jsons.load(source_dict, source_cls.config_class(), strict=True)
        source = source_cls(source_config)

        output[source] = []

        for target_dict in source_config.targets:
            target_cls = [t for t in targets_pkg.ALL if t.__name__ == target_dict['name']][0]
            target_config = jsons.load(target_dict, target_cls.config_class(), strict=True)
            target = target_cls(target_config)

            output[source].append(target)

    return output


def _create_job(source: Source, targets: List[Target]) -> Callable[[], None]:
    def job() -> None:
        data = source.retrieve()
        for target in targets:
            target.store(data)

    return job
