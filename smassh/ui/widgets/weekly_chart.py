from datetime import timedelta

from rich.text import Text
from textual.widgets import Static


class WeeklyChart(Static):
    """Compare weekly typing speed on a shared scale starting at zero."""

    DEFAULT_CSS = """
    WeeklyChart {
        height: auto;
        margin: 1 0;
    }
    """

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.weeks: list[dict] = []

    def set_weeks(self, weeks: list[dict]) -> None:
        self.weeks = weeks
        self.refresh(layout=True)

    def render(self) -> Text:
        if not self.weeks:
            return Text("No completed tests in this selection.")

        maximum = max(week["wpm"] for week in self.weeks)
        compact = self.size.width < 80
        bar_width = max(1, self.size.width - (2 if compact else 64))
        lines = []
        for week in self.weeks:
            start = week["date"]
            end = start + timedelta(days=6)
            label = f"{start:%d %b}–{end:%d %b %Y}"
            length = round(week["wpm"] / maximum * bar_width) if maximum else 0
            bar = "█" * length
            details = (
                f"{week['wpm']:.1f} WPM · "
                f"{week['accuracy']:.1f}% · {week['count']} tests"
            )
            if compact:
                lines.extend((label, f"  {bar}", details, ""))
            else:
                lines.append(f"{label:<24} {bar:<{bar_width}} {details}")
        lines.append(f"Scale: 0–{maximum:.1f} WPM · Accuracy (%) · Completed tests")
        return Text("\n".join(lines))
