import xml.etree.ElementTree as ET


class Parser:
    def __init__(self, path):
        self.path = path

    def parse(self):
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

        print(elements)
        return elements

    @staticmethod
    def parse_rectangle(attributes):
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
        return {
            "type": "circle",
            "cx": float(attributes.get("cx", 0)),
            "cy": float(attributes.get("cy", 0)),
            "r": float(attributes.get("r", 0)),
            "fill": attributes.get("fill", "none"),
            "stroke": attributes.get("stroke", "none")
        }
