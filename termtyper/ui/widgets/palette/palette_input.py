from textual.widgets import Input


class PaletteInput(Input):
    DEFAULT_CSS = """
    PaletteInput {
        border: none;
        height: 1;
    }

    PaletteInput:focus {
        border: none;
    }
    """
