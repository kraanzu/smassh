from textual.widgets import Input


class PaletteInput(Input):
    """
    Input Widget for Palette Menu to filter results
    """

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
