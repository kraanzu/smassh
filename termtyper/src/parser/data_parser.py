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
        elapsed = stats.checkpoints[-1].elapsed if stats.checkpoints else 0

        return dict(
            mode=mode,
            count=count,
            start_time=stats.start_time,
            elapsed_time=elapsed,
            wpm=stats.wpm,
            raw_wpm=stats.raw_wpm,
            accuracy=stats.accuracy,
        )

    def add_stats(self, stats: StatsTracker):
        report = self.generate_report(stats)
        self.get("data").append(report)
        self.save()


data_parser = DataParser()
