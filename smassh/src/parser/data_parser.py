import json
import os
from copy import deepcopy
from pathlib import Path
from tempfile import NamedTemporaryFile
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
        self.config = deepcopy(self.config)

        english_path = self.lang_path / "english.json"

        if not self.lang_path.is_dir():
            self.lang_path.mkdir(parents=True, exist_ok=True)

        if not english_path.exists():
            import shutil
            from importlib.resources import as_file, files

            bundled = files("smassh.data.languages").joinpath("english.json")
            with as_file(bundled) as src:
                shutil.copy(src, english_path)

    def save(self) -> None:
        """Replace the history only after the complete JSON has been written."""
        self.config_path.mkdir(parents=True, exist_ok=True)
        temporary = None
        try:
            with NamedTemporaryFile(
                mode="w", encoding="utf-8", dir=self.config_path, delete=False
            ) as fp:
                temporary = Path(fp.name)
                json.dump(
                    self.config, fp, ensure_ascii=False, indent=2, allow_nan=False
                )
                fp.flush()
                os.fsync(fp.fileno())
            os.replace(temporary, self.full_path)
        finally:
            if temporary is not None:
                temporary.unlink(missing_ok=True)

    def clear_history(self) -> None:
        """Remove saved attempts without changing typing preferences."""
        previous = self.config
        self.config = {**previous, "data": []}
        try:
            self.save()
        except OSError:
            self.config = previous
            raise

    def summary(self) -> dict[str, Any]:
        """Summarize successful attempts with the current test settings."""
        tests = self.current_mode_tests()
        return {
            "count": len(tests),
            "average_wpm": sum(t["wpm"] for t in tests) / len(tests) if tests else None,
            "best_wpm": max((t["wpm"] for t in tests), default=0),
            "average_accuracy": (
                sum(t["accuracy"] for t in tests) / len(tests) if tests else None
            ),
            "practice_time": sum(t["elapsed_time"] for t in tests),
        }

    def test_settings(self) -> dict[str, Any]:
        """Settings that affect whether two results can be compared."""
        return {
            key: settings.get(key)
            for key in (
                "language",
                "difficulty",
                "numbers",
                "punctuations",
                "capitalization_mode",
                "blind_mode",
                "confidence_mode",
                "force_correct",
                "min_speed",
                "min_accuracy",
                "min_burst",
            )
        }

    def generate_report(self, stats: StatsTracker) -> dict[str, Any]:
        mode = settings.get("mode")
        count = settings.get(f"{mode}_count")
        start = stats.start_time or 0
        end = stats.end_time or 0
        elapsed = end - start

        return {
            **self.test_settings(),
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
        previous = self.config
        self.config = deepcopy(previous)
        self.get("data").append(report)
        try:
            self.save()
        except OSError:
            self.config = previous
            raise

    def current_mode_tests(self) -> list[dict]:
        mode = settings.get("mode")
        count = settings.get(f"{mode}_count")

        def same_mode(test: dict):
            return (
                not test.get("failed", False)
                and test["mode"] == mode
                and count == test["count"]
                and all(
                    test.get(key) == value
                    for key, value in self.test_settings().items()
                )
            )

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
