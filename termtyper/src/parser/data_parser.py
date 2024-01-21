from pathlib import Path
from .parser import Parser
from termtyper.src.stats_tracker import StatsTracker
from termtyper.src.parser.config_parser import config_parser
import appdirs


class DataParser(Parser):
    config_path = Path(appdirs.user_data_dir("smassh"))
    DEFAULT_CONFIG = dict(data=[])

    def generate_report(self, stats: StatsTracker):
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

    def add_stats(self, stats: StatsTracker, failed: bool):
        report = self.generate_report(stats) | dict(failed=failed)
        self.get("data").append(report)
        self.save()


data_parser = DataParser()
