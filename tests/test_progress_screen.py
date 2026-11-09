from copy import deepcopy
from unittest import IsolatedAsyncioTestCase
from unittest.mock import patch

from smassh.src import data_parser
from smassh.ui.screens.progress import ProgressScreen
from smassh.ui.tui import Smassh


class ClearHistoryTest(IsolatedAsyncioTestCase):
    async def test_cancel_preserves_history_and_confirm_clears_it(self) -> None:
        report = {
            "mode": "words",
            "count": 30,
            "start_time": 100,
            "elapsed_time": 10,
            "wpm": 12,
            "raw_wpm": 12,
            "accuracy": 100,
            "failed": False,
        }
        config = {"data": [report]}
        with (
            patch.object(data_parser, "config", deepcopy(config)),
            patch.object(data_parser, "save"),
        ):
            async with Smassh().run_test() as pilot:
                await pilot.press("ctrl+g")
                await pilot.pause()
                progress = pilot.app.screen.query_one(ProgressScreen)
                progress.clear_history()
                await pilot.pause()
                await pilot.press("c")
                await pilot.pause()
                self.assertEqual(data_parser.get("data"), [report])
                progress.clear_history()
                await pilot.pause()
                await pilot.press("o")
                await pilot.pause()
                self.assertEqual(data_parser.get("data"), [])


class ProgressChartSelectionTest(IsolatedAsyncioTestCase):
    async def test_switching_chart_preserves_history_and_filters(self) -> None:
        from textual.app import App, ComposeResult
        from textual.widgets import DataTable, Select

        class ProgressApp(App):
            def compose(self) -> ComposeResult:
                yield ProgressScreen()

        report = {
            "mode": "words",
            "count": 30,
            "start_time": 100,
            "elapsed_time": 10,
            "wpm": 40,
            "raw_wpm": 42,
            "accuracy": 95,
            "failed": False,
        }
        with patch.object(data_parser, "config", {"data": [report]}):
            async with ProgressApp().run_test() as pilot:
                await pilot.pause()
                progress = pilot.app.screen.query_one(ProgressScreen)
                progress.query_one("#history-filter", Select).value = "all"
                await pilot.pause()
                self.assertTrue(progress.query_one("#speed-history").display)
                for mode in ("line", "bars"):
                    progress.query_one("#history-chart", Select).value = mode
                    await pilot.pause()
                    self.assertEqual(
                        progress.query_one("#speed-line").display, mode == "line"
                    )
                    self.assertEqual(
                        progress.query_one("#speed-history").display, mode == "bars"
                    )
                    self.assertEqual(
                        progress.query_one("#history-filter", Select).value, "all"
                    )
                    self.assertEqual(progress.query_one(DataTable).row_count, 1)
                    self.assertEqual(data_parser.get("data"), [report])
