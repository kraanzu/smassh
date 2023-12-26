from textual.widgets import Input


class PaletteInput(Input):
    DEFAULT_CSS = """
    PaletteInput {
        border: none;
        height: 1;
        padding: 0;
    }

    PaletteInput:focus {
        border: none;
        padding: 0;
    }
    """
