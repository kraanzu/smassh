from math import ceil, floor

from rich.text import Text
from textual.widgets import Static


class LineChart(Static):
    """A small line chart with labelled value and time axes."""

    DEFAULT_CSS = """
    LineChart {
        height: 12;
        margin: 1 0;
    }
    """

    def __init__(self, title: str, **kwargs) -> None:
        super().__init__(**kwargs)
        self.title = title
        self.points: list[tuple[float, float]] = []
        self.labels: tuple[str, str, str] = ("", "", "")

    def set_series(
        self,
        points: list[tuple[float, float]],
        labels: tuple[str, str, str],
    ) -> None:
        self.points = sorted(points)
        self.labels = labels
        self.refresh()

    def render(self) -> Text:
        if not self.points:
            return Text(f"{self.title}\nNo completed tests in this selection.")

        width = max(8, self.size.width - 9)
        height = 6
        values = [value for _, value in self.points]
        low = max(0, floor((min(values) - 2) / 5) * 5)
        high = max(low + 5, ceil((max(values) + 2) / 5) * 5)
        start, end = self.points[0][0], self.points[-1][0]
        span = end - start or 1
        grid = [[" " for _ in range(width)] for _ in range(height + 1)]
        coordinates = [
            (
                round((timestamp - start) / span * (width - 1)),
                round((high - value) / (high - low) * height),
            )
            for timestamp, value in self.points
        ]
        for (x1, y1), (x2, y2) in zip(coordinates, coordinates[1:]):
            if x1 == x2:
                for y in range(min(y1, y2), max(y1, y2) + 1):
                    grid[y][x1] = "│"
                continue
            previous_y = y1
            for x in range(x1 + 1, x2 + 1):
                y = round(y1 + (y2 - y1) * (x - x1) / (x2 - x1))
                for between in range(min(previous_y, y) + 1, max(previous_y, y)):
                    grid[between][x] = "│"
                grid[y][x] = "─" if y == previous_y else "╱" if y < previous_y else "╲"
                previous_y = y
        for x, y in coordinates:
            grid[y][x] = "●"

        lines = [self.title]
        for row, cells in enumerate(grid):
            value = high - (high - low) * row / height
            label = f"{value:5.0f}" if row in (0, height // 2, height) else "     "
            lines.append(f"{label} │{''.join(cells)}")
        lines.append("      └" + "─" * width)
        axis = [" "] * width
        labels = self.labels if width >= 30 else (self.labels[0], "", self.labels[2])
        if len(self.points) == 1:
            labels = (labels[0], "", "")
        for label, position in zip(labels, (0, width // 2, width)):
            offset = min(max(0, position - len(label) // 2), max(0, width - len(label)))
            axis[offset : offset + len(label)] = label
        lines.append("       " + "".join(axis))
        if len(self.points) == 1:
            lines.append("One data point — complete more tests to see a trend.")
        return Text("\n".join(lines))
