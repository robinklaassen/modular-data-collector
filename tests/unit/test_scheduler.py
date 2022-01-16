from unittest import TestCase

from modular_data_collector import scheduler
from modular_data_collector.config import Config
from modular_data_collector.sources.source import Source
from modular_data_collector.targets.target import Target

from tests.unit.shared_mocks import MockSource, MockTarget


class SchedulerTestSuite(TestCase):

    def test_construct_job_dict(self):
        scheduler.sources_pkg.ALL = {MockSource}
        scheduler.targets_pkg.ALL = {MockTarget}

        config = Config(
            sources=[{
                "name": "MockSource",
                "interval_sec": 10,
                "targets": [{
                    "name": "MockTarget"
                }]
            }]
        )

        job_dict = scheduler._construct_job_dict(config)

        self.assertEqual(1, len(job_dict))
        self.assertIsInstance(next(iter(job_dict)), Source)
        self.assertIsInstance(list(job_dict.values())[0][0], Target)
