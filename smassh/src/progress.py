from collections import defaultdict
from datetime import datetime, timedelta


def weekly_averages(attempts: list[dict]) -> list[dict]:
    """Average successful attempts by local calendar week (Monday–Sunday)."""
    weeks = defaultdict(list)
    for attempt in attempts:
        if not attempt.get("failed"):
            date = datetime.fromtimestamp(attempt["start_time"]).date()
            monday = date - timedelta(days=date.weekday())
            weeks[monday].append(attempt)
    return [
        {
            "date": date,
            "count": len(tests),
            "wpm": sum(test["wpm"] for test in tests) / len(tests),
            "accuracy": sum(test["accuracy"] for test in tests) / len(tests),
        }
        for date, tests in sorted(weeks.items())
    ]
