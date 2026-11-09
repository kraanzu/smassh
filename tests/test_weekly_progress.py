from datetime import datetime
from unittest import TestCase

from smassh.src.progress import weekly_averages


class WeeklyProgressTest(TestCase):
    def test_averages_completed_tests_in_the_same_calendar_week(self) -> None:
        monday = datetime(2026, 11, 2, 10).timestamp()
        sunday = datetime(2026, 11, 8, 10).timestamp()
        next_monday = datetime(2026, 11, 9, 10).timestamp()
        attempts = [
            {"start_time": next_monday, "wpm": 60, "accuracy": 98},
            {"start_time": monday, "wpm": 30, "accuracy": 90},
            {"start_time": sunday, "wpm": 50, "accuracy": 94},
            {"start_time": monday, "wpm": 0, "accuracy": 0, "failed": True},
        ]
        weeks = weekly_averages(attempts)
        self.assertEqual(len(weeks), 2)
        self.assertEqual(weeks[0]["date"], datetime(2026, 11, 2).date())
        self.assertEqual(weeks[0]["count"], 2)
        self.assertEqual(weeks[0]["wpm"], 40)
        self.assertEqual(weeks[0]["accuracy"], 92)
        self.assertEqual(weeks[1]["wpm"], 60)

    def test_empty_history_has_no_weeks(self) -> None:
        self.assertEqual(weekly_averages([]), [])

    def test_week_across_year_boundary_stays_together(self) -> None:
        attempts = [
            {
                "start_time": datetime(2025, 12, 31).timestamp(),
                "wpm": 30,
                "accuracy": 90,
            },
            {
                "start_time": datetime(2026, 1, 1).timestamp(),
                "wpm": 50,
                "accuracy": 100,
            },
        ]
        weeks = weekly_averages(attempts)
        self.assertEqual(len(weeks), 1)
        self.assertEqual(weeks[0]["date"], datetime(2025, 12, 29).date())
        self.assertEqual(weeks[0]["wpm"], 40)
