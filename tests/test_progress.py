from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase
from unittest.mock import patch

from smassh.src.parser.config_parser import settings
from smassh.src.parser.data_parser import DataParser
from smassh.src.stats_tracker import CheckPoint, Match, StatsTracker


class ProgressTest(TestCase):
    def setUp(self) -> None:
        self.directory = TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.path = patch.object(DataParser, "config_path", Path(self.directory.name))
        self.path.start()
        self.addCleanup(self.path.stop)
        self.language_path = patch.object(
            DataParser, "lang_path", Path(self.directory.name) / "languages"
        )
        self.language_path.start()
        self.addCleanup(self.language_path.stop)
        self.config = patch.dict(settings.config, {"mode": "words", "words_count": 30})
        self.config.start()
        self.addCleanup(self.config.stop)
        self.history = DataParser()

    def attempt(self, failed=False):
        stats = StatsTracker()
        stats.start_time = 100
        stats.end_time = 110
        for letter in "hello world ":
            checkpoint = CheckPoint(letter, 0, Match.MATCH)
            checkpoint.add_elapsed(1)
            stats.checkpoints.append(checkpoint)
        self.history.add_stats(stats, failed)
        return stats

    def test_completed_attempt_survives_restart(self) -> None:
        stats = self.attempt()
        report = DataParser().get("data")[0]
        self.assertEqual(report["wpm"], stats.wpm)
        self.assertEqual(report["accuracy"], stats.accuracy)
        self.assertEqual(report["language"], settings.get("language"))

    def test_failed_attempt_does_not_set_record(self) -> None:
        self.attempt(failed=True)
        self.assertEqual(self.history.hightest_wpm(), 0)

    def test_different_language_is_not_compared(self) -> None:
        self.attempt()
        with patch.dict(settings.config, {"language": "another"}):
            self.assertEqual(self.history.current_mode_tests(), [])

    def test_clear_history_persists_and_preserves_settings(self) -> None:
        self.attempt()
        self.history.config["theme"] = "nord"
        original = settings.config.copy()
        self.history.clear_history()
        self.assertEqual(DataParser().get("data"), [])
        self.assertEqual(self.history.hightest_wpm(), 0)
        self.assertEqual(settings.config, original)
        self.assertEqual(DataParser().get("theme"), "nord")

    def test_summary_uses_successful_comparable_attempts(self) -> None:
        stats = self.attempt()
        self.attempt(failed=True)
        summary = self.history.summary()
        self.assertEqual(summary["count"], 1)
        self.assertEqual(summary["average_wpm"], stats.wpm)
        self.assertEqual(summary["best_wpm"], stats.wpm)

    def test_empty_history_has_no_average(self) -> None:
        self.assertEqual(self.history.summary()["count"], 0)
        self.assertIsNone(self.history.summary()["average_wpm"])

    def test_failed_save_keeps_previous_history(self) -> None:
        self.attempt()
        previous = self.history.get("data").copy()
        with (
            patch.object(self.history, "save", side_effect=OSError("Disk full")),
            self.assertRaises(OSError),
        ):
            self.attempt()
        self.assertEqual(self.history.get("data"), previous)
        self.assertEqual(DataParser().get("data"), previous)

    def test_failed_clear_keeps_history(self) -> None:
        self.attempt()
        previous = self.history.get("data").copy()
        with (
            patch.object(self.history, "save", side_effect=OSError("Read only")),
            self.assertRaises(OSError),
        ):
            self.history.clear_history()
        self.assertEqual(self.history.get("data"), previous)
