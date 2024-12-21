from scripts.svg_parser import Parser
from scripts.renderer import Renderer
import sys


def convert(input, output, scale=4):
    """
    Converts an SVG file to a PNG file.

    Args:
        input (str): Path to the input SVG file.
        output (str): Path to the output PNG file.
        scale (int): Scaling factor for resolution.
    """
    p = Parser(input)
    width, height = p.extract_dimensions()
    elements = p.parse()
    r = Renderer(width, height, scale)
    r.draw_elements(elements)
    r.save_PNG(output)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Invalid arguments. Usage : python main.py <input_file> <output_file>")
        exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    convert(input_file, output_file)
