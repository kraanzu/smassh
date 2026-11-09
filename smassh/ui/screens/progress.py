from datetime import datetime
from time import time

from textual.app import ComposeResult, events
from textual.widgets import Button, DataTable, Select, Static

from smassh.src import data_parser
from smassh.src.progress import weekly_averages
from smassh.ui.widgets import BaseWindow
from smassh.ui.widgets.line_chart import LineChart
from smassh.ui.widgets.weekly_chart import WeeklyChart


class ProgressScreen(BaseWindow):
    """Local typing history and progress for comparable tests."""

    DEFAULT_CSS = """
    ProgressScreen { padding: 1 3; }
    ProgressScreen Static { height: auto; }
    ProgressScreen Select { margin-bottom: 1; }
    ProgressScreen #progress-summary { margin: 1 0; }
    ProgressScreen LineChart { height: 12; }
    ProgressScreen DataTable { height: 1fr; min-height: 5; }
    ProgressScreen #clear-history { margin-top: 1; margin-bottom: 1; }
    """

    def compose(self) -> ComposeResult:
        yield Select(
            [("Current test settings", "current"), ("All attempts", "all")],
            value="current",
            allow_blank=False,
            id="history-filter",
        )
        yield Select(
            [
                ("All time", 0),
                ("Last 7 days", 7),
                ("Last 30 days", 30),
                ("Last 90 days", 90),
            ],
            value=0,
            allow_blank=False,
            id="history-period",
        )
        yield Select(
            [("Horizontal bars", "bars"), ("Line chart", "line")],
            value="bars",
            allow_blank=False,
            id="history-chart",
        )
        yield Static(id="progress-summary", markup=False)
        yield Static("Weekly averages · Monday–Sunday · completed tests only")
        yield WeeklyChart(id="speed-history")
        yield LineChart("Weekly speed (WPM)", id="speed-line")
        yield LineChart("Weekly accuracy (%)", id="accuracy-line")
        yield DataTable(id="history")
        yield Button("Clear history", id="clear-history", variant="error")
        yield Static(str(data_parser.full_path), markup=False)
        yield Static("Ctrl+G: progress · Esc: home · C: clear history")

    def on_mount(self) -> None:
        self.query_one(DataTable).add_columns(
            "Date", "Test", "WPM", "Raw", "Accuracy", "Status"
        )

    def on_show(self) -> None:
        self.refresh_history()

    def on_select_changed(self, event: Select.Changed) -> None:
        self.refresh_history()

    def refresh_history(self) -> None:
        current = self.query_one("#history-filter", Select).value == "current"
        attempts = (
            data_parser.current_mode_tests() if current else data_parser.get("data")
        )
        days = self.query_one("#history-period", Select).value
        if isinstance(days, int) and days:
            attempts = [t for t in attempts if t["start_time"] >= time() - days * 86400]
        successful = [test for test in attempts if not test.get("failed")]
        table = self.query_one(DataTable)
        table.clear()
        for test in reversed(attempts):
            date = datetime.fromtimestamp(test["start_time"]).strftime("%Y-%m-%d %H:%M")
            table.add_row(
                date,
                f"{test['mode']} {test['count']}",
                str(test["wpm"]),
                str(test["raw_wpm"]),
                f"{test['accuracy']}%",
                "Failed" if test.get("failed") else "Completed",
            )
        weeks = weekly_averages(attempts)
        bars = self.query_one(WeeklyChart)
        bars.set_weeks(weeks)
        show_line = self.query_one("#history-chart", Select).value == "line"
        bars.display = not show_line
        labels = ("", "", "")
        if weeks:
            first = weeks[0]["date"]
            last = weeks[-1]["date"]
            middle = first + (last - first) // 2
            labels = tuple(date.strftime("%d %b") for date in (first, middle, last))
        for selector, metric in (
            ("#speed-line", "wpm"),
            ("#accuracy-line", "accuracy"),
        ):
            chart = self.query_one(selector, LineChart)
            chart.display = show_line
            chart.set_series(
                [(week["date"].toordinal(), week[metric]) for week in weeks], labels
            )
        if successful:
            average = sum(t["wpm"] for t in successful) / len(successful)
            best = max(t["wpm"] for t in successful)
            seconds = sum(t["elapsed_time"] for t in successful)
            text = f"{len(successful)} completed · Average {average:.1f} WPM · Best {best} WPM · Practice {seconds / 60:.1f} min"
        else:
            text = "No completed tests in this selection. Finish a test to see your progress."
        self.query_one("#progress-summary", Static).update(text)

    def clear_history(self) -> None:
        def confirmed(ok: bool) -> None:
            if ok:
                try:
                    data_parser.clear_history()
                except OSError as error:
                    self.notify(f"Could not clear history: {error}", severity="error")
                self.refresh_history()

        self.app.push_screen("confirm", confirmed)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "clear-history":
            self.clear_history()

    async def handle_key(self, event: events.Key) -> bool:
        if event.key == "c":
            self.clear_history()
            return True
        return await super().handle_key(event)
