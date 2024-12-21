import xml.etree.ElementTree as ET
from PIL import ImageColor

class Parser:
    """
    A class to parse SVG files and extract supported geometric elements.

    Supported elements:
    - Rectangle
    - Circle
    - Line
    - Ellipse
    - Path
    - Polyline
    """

    DEFAULT_COLOR = 'black'

    def __init__(self, path):
        """
        Initializes the Parser with the path to the SVG file.
        Args:
             path (str): The path to the SVG file to be parsed.
        """
        self.path = path
        self.parsed_elements = ['rect', 'circle', 'line', 'ellipse', 'path', 'polyline']

    def extract_dimensions(self):
        tree = ET.parse(self.path)
        root = tree.getroot()

        width = root.attrib.get('width')
        height = root.attrib.get('height')

        if not width or not height:
            viewbox = root.attrib.get('viewBox')
            if viewbox:
                _, _, width, height = map(float, viewbox.split())
            else:
                print("Invalid dimensions")
                exit(1)

        return int(width), int(height)

    def parse(self):
        """
        Parses the SVG file and extracts geometric elements.

        Returns:
            list[dict]: A list of dictionaries, each representing a geometric element.

        Raises:
            ValueError: If the SVG file cannot be read or parsed.
        """

        try:
            tree = ET.parse(self.path)
            root = tree.getroot()
        except Exception as e:
            raise ValueError(f"Error on reading SVG file: {e}")

        elements = []
        for element in root:
            tag = element.tag.split('}')[1]
            attributes = element.attrib
            if tag in self.parsed_elements:
                parse_function = getattr(Parser, f"parse_{tag}", None)
                if callable(parse_function):
                    elements.append(parse_function(attributes))
                else:
                    print(f"Function 'parse_{tag}' is not defined.")

        return elements

    @staticmethod
    def parse_rect(attributes):
        """
        Parses a rectangle element and extracts its attributes.

        Args:
            attributes (dict): The attributes of the rectangle element.

        Returns:
            dict: A dictionary with rectangle attributes.
        """

        return {
            "type": "rect",
            "x": float(attributes.get("x", 0)),
            "y": float(attributes.get("y", 0)),
            "width": float(attributes.get("width", 0)),
            "height": float(attributes.get("height", 0)),
            "stroke": Parser.parse_color(attributes.get("stroke", Parser.DEFAULT_COLOR)),
            "stroke-width": int(attributes.get("stroke-width", 0)),
            "fill": Parser.parse_color(attributes.get("fill", Parser.DEFAULT_COLOR))
        }

    @staticmethod
    def parse_circle(attributes):
        """
        Parses a circle element and extracts its attributes.

        Args:
            attributes (dict): The attributes of the circle element.

        Returns:
            dict: A dictionary with circle attributes.
        """
        return {
            "type": "circle",
            "cx": float(attributes.get("cx", 0)),
            "cy": float(attributes.get("cy", 0)),
            "r": float(attributes.get("r", 0)),
            "fill": Parser.parse_color(attributes.get("fill", Parser.DEFAULT_COLOR)),
            "stroke-width": int(attributes.get("stroke-width", 0)),
            "stroke": Parser.parse_color(attributes.get("stroke", Parser.DEFAULT_COLOR))
        }

    @staticmethod
    def parse_line(attributes):
        """
        Parses a line element and extracts its attributes.

        Args:
            attributes (dict): The attributes of the line element.

        Returns:
            dict: A dictionary with line attributes.
        """
        return {
            "type": "line",
            "x1": float(attributes.get("x1", 0)),
            "y1": float(attributes.get("y1", 0)),
            "x2": float(attributes.get("x2", 0)),
            "y2": float(attributes.get("y2", 0)),
            "stroke-width": int(attributes.get("stroke-width", 0)),
            "stroke": Parser.parse_color(attributes.get("stroke", Parser.DEFAULT_COLOR))
        }

    @staticmethod
    def parse_ellipse(attributes):
        """
        Parses an ellipse element and extracts its attributes.

        Args:
            attributes (dict): The attributes of the ellipse element.

        Returns:
            dict: A dictionary with ellipse attributes.
        """
        return {
            "type": "ellipse",
            "cx": float(attributes.get("cx", 0)),
            "cy": float(attributes.get("cy", 0)),
            "rx": float(attributes.get("rx", 0)),
            "ry": float(attributes.get("ry", 0)),
            "stroke": Parser.parse_color(attributes.get("stroke", Parser.DEFAULT_COLOR)),
            "stroke-width": int(attributes.get("stroke-width", 0)),
            "fill": Parser.parse_color(attributes.get("fill", Parser.DEFAULT_COLOR))
        }

    @staticmethod
    def parse_path(attributes):
        """
        Parses a path element and extracts its attributes.

        Args:
            attributes (dict): The attributes of the path element.

        Returns:
            dict: A dictionary with path attributes.
        """
        if not isinstance(attributes, dict):
            raise ValueError("Expected attributes to be a dictionary")

        return {
            "type": "path",
            "d": attributes.get("d", ""),
            "stroke": Parser.parse_color(attributes.get("stroke", Parser.DEFAULT_COLOR)),
            "stroke-width": int(attributes.get("stroke-width", 0)),
            "fill": Parser.parse_color(attributes.get("fill", Parser.DEFAULT_COLOR)),
        }

    @staticmethod
    def parse_polyline(attributes):
        """
        Parses the attributes of an SVG polyline element into a dictionary.

        Args:
            attributes (dict): The attributes of the polyline element.

        Returns:
            dict: A dictionary with polyline attributes.
        """
        return {
            "type": "polyline",
            "points": attributes.get("points", ""),
            "stroke": Parser.parse_color(attributes.get("stroke", Parser.DEFAULT_COLOR)),
            "stroke-width": int(attributes.get("stroke-width", 0)),
            "fill": Parser.parse_color(attributes.get("fill", Parser.DEFAULT_COLOR))
        }

    @staticmethod
    def parse_color(color):
        """
        Parses a color value and returns it in a format usable by the renderer.

        Args:
            color (str): The color value, which can be:
                - 'none' or 'transparent': Returns `None`.
                - 'rgba()': A string in the 'rgba(r,g,b,a)' format.
                - '#RRGGBB', 'rgb()', or named colors: Validated by Pillow's ImageColor.
                - Invalid colors: Replaced with a default color.

        Returns:
            tuple or str or None:
                - `None` if the color is 'none' or 'transparent'.
                - `(r, g, b, a)` if the color is in 'rgba()' format.
                - The original string for valid named or hex colors.
                - Default color if invalid.
        """
        if not color or color in ["none", "transparent"]:
            return None

        if color.startswith('rgba'):
            try:
                values = color[color.index('(') + 1:color.index(')')].split(',')
                r, g, b = map(int, values[:3])
                a = int(float(values[3]) * 255) if len(values) == 4 else 255
                return r, g, b, a
            except (ValueError, IndexError):
                return Parser.DEFAULT_COLOR

        try:
            ImageColor.getrgb(color)
            return color
        except ValueError:
            return Parser.DEFAULT_COLOR
