from pathlib import Path
from typing import Any, Dict, List
from .parser import Parser
from smassh.src.stats_tracker import StatsTracker
from smassh.src.parser.config_parser import config_parser
import appdirs


class DataParser(Parser):
    config_path = Path(appdirs.user_data_dir("smassh"))
    DEFAULT_CONFIG = dict(data=[])

    def generate_report(self, stats: StatsTracker) -> Dict[str, Any]:
        mode = config_parser.get("mode")
        count = config_parser.get(f"{mode}_count")
        start = stats.start_time or 0
        end = stats.end_time or 0
        elapsed = end - start

        return dict(
            mode=mode,
            count=count,
            start_time=stats.start_time,
            elapsed_time=elapsed,
            wpm=stats.wpm,
            raw_wpm=stats.raw_wpm,
            accuracy=stats.accuracy,
        )

    def add_stats(self, stats: StatsTracker, failed: bool) -> None:
        report = self.generate_report(stats) | dict(failed=failed)
        self.get("data").append(report)
        self.save()

    def current_mode_tests(self) -> List[Dict]:
        mode = config_parser.get("mode")
        count = config_parser.get(f"{mode}_count")

        def same_mode(test: Dict):
            return test["mode"] == mode and count == test["count"]

        return list(filter(same_mode, self.get("data")))

    def hightest_wpm(self) -> int:
        tests = self.current_mode_tests()
        if not tests:
            return 0

        return max(tests, key=lambda x: x["wpm"])["wpm"]

    def hightest_accuracy(self) -> int:
        tests = self.current_mode_tests()
        if not tests:
            return 0

        return max(tests, key=lambda x: x["accuracy"])["accuracy"]

    def is_highest_wpm(self, wpm: int) -> bool:
        return wpm > self.hightest_wpm()

    def is_highest_accuracy(self, accuracy: int) -> bool:
        return accuracy > self.hightest_accuracy()


data_parser = DataParser()
