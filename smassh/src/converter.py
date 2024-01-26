import re
import os
import sys


def convert_css(input_file, output_file) -> None:
    with open(input_file, "r") as f:
        css_content = f.read()

    pattern = re.compile(r"--([\w-]+):\s*([^;]+);")
    matches = pattern.findall(css_content)

    new_tcss_content = ""
    for custom_property, color_value in matches:
        new_tcss_content += f"${custom_property}: {color_value};\n"

    with open(output_file, "w") as f:
        f.write(new_tcss_content)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py input.css")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = os.path.splitext(input_file)[0] + ".tcss"

    convert_css(input_file, output_file)
