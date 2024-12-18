import xml.etree.ElementTree as ET


class Parser:
    """
    A class to parse SVG files and extract supported geometric elements.

    Supported elements:
    - Rectangle
    - Circle
    - Line
    - Ellipse
    - Path
    """

    def __init__(self, path):
        """
        Initializes the Parser with the path to the SVG file.
        Args:
             path (str): The path to the SVG file to be parsed.
        """
        self.path = path

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

            if tag == "rect":
                elements.append(self.parse_rectangle(attributes))
            elif tag == "circle":
                elements.append(self.parse_circle(attributes))
            elif tag == "line":
                elements.append(self.parse_line(attributes))
            elif tag == "ellipse":
                elements.append(self.parse_ellipse(attributes))
            elif tag == "path":
                elements.append(self.parse_path(attributes))


        print(elements)
        return elements

    @staticmethod
    def parse_rectangle(attributes):
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
            "stroke": attributes.get("stroke", "none"),
            "fill": attributes.get("fill", "none")
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
            "fill": attributes.get("fill", "none"),
            "stroke": attributes.get("stroke", "none")
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
            "fill": attributes.get("fill", "none"),
            "stroke": attributes.get("stroke", "none")
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
            "stroke": attributes.get("stroke", "none"),
            "fill": attributes.get("fill", "none")
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
        return {
            "type": "path",
            "d": attributes.get("d", ""),
            "stroke": attributes.get("stroke", "none"),
            "fill": attributes.get("fill", "none")
        }
