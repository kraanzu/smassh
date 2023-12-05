import os
from pathlib import Path

parent_folder = Path(__file__).parent / "css"
CSS = ""

for file in os.listdir(parent_folder):
    if not file.endswith(".css"):
        continue

    with open(os.path.join(parent_folder, file), "r") as css_file:
        CSS += css_file.read()
