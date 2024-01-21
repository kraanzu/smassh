from textual.widgets import Input


class PaletteInput(Input):
    DEFAULT_CSS = """
    PaletteInput {
        border: none;
        content-align: left middle;
        padding: 0 1;
    }

    PaletteInput:focus {
        border: none;
        content-align: left middle;
        padding: 0 1;
    }
    """
