from pathlib import Path
from typing import Any, ClassVar

import platformdirs

from smassh.src.parser.config_parser import settings
from smassh.src.stats_tracker import StatsTracker

from .parser import Parser


class DataParser(Parser):
    """
    Inherited from `Parser` class to manage user data
    """

    config_path = Path(platformdirs.user_data_dir("smassh"))
    lang_path = config_path / "languages"
    DEFAULT_CONFIG: ClassVar[dict[str, Any]] = {"data": []}

    def __init__(self) -> None:
        super().__init__()

        english_path = self.lang_path / "english.json"

        if not self.lang_path.is_dir():
            self.lang_path.mkdir(parents=True, exist_ok=True)

        if not english_path.exists():
            import shutil
            from importlib.resources import as_file, files

            bundled = files("smassh.data.languages").joinpath("english.json")
            with as_file(bundled) as src:
                shutil.copy(src, english_path)

    def generate_report(self, stats: StatsTracker) -> dict[str, Any]:
        mode = settings.get("mode")
        count = settings.get(f"{mode}_count")
        start = stats.start_time or 0
        end = stats.end_time or 0
        elapsed = end - start

        return {
            "mode": mode,
            "count": count,
            "start_time": stats.start_time,
            "elapsed_time": elapsed,
            "wpm": stats.wpm,
            "raw_wpm": stats.raw_wpm,
            "accuracy": stats.accuracy,
        }

    def add_stats(self, stats: StatsTracker, failed: bool) -> None:
        report = self.generate_report(stats) | {"failed": failed}
        self.get("data").append(report)
        self.save()

    def current_mode_tests(self) -> list[dict]:
        mode = settings.get("mode")
        count = settings.get(f"{mode}_count")

        def same_mode(test: dict):
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
