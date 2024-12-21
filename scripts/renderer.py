from PIL import Image, ImageDraw
from scripts.path_parser import PathParser

class Renderer:
    """
       A class to render SVG-like elements onto a PNG image.

       This class supports rendering various geometric shapes such as rectangles,
       circles, lines, ellipses, and paths. The elements are provided as dictionaries
       and rendered dynamically based on their type.

       Attributes:
           width (int): Width of the rendered image.
           height (int): Height of the rendered image.
           image (Image): The Pillow Image object where elements are drawn.
           elements_supported (list): List of supported element types.
           draw (ImageDraw): The Pillow ImageDraw object used for drawing.
       """

    def __init__(self, width, height, scale=2, elements_supported=None):
        """
        Initializes the Renderer with a blank image and supported elements.

        Args:
            width (int): Width of the image.
            height (int): Height of the image.
            elements_supported (list[str], optional): A list of element types that
                the renderer supports. If None, the default supported elements
                are ['rect', 'circle', 'line', 'ellipse', 'path', 'polyline'].
        """

        self.width = width
        self.height = height
        self.image = Image.new('RGBA', (int(width * scale), int(height * scale)), (255, 255, 255, 0))
        self.elements_supported = elements_supported
        if self.elements_supported is None:
            self.elements_supported = elements_supported
        self.elements_supported = ['rect', 'circle', 'line', 'ellipse', 'path', 'polyline']
        self.draw = ImageDraw.Draw(self.image, 'RGBA')

    def draw_elements(self, elements):
        """
        Iterates over the list of elements and draws them based on their type.

        Args:
            elements (list[dict]): A list of element dictionaries containing type
                and attributes (e.g., rect, circle, line).

        Returns:
            Image: The updated Pillow Image object.
        """
        for element in elements:
            element_type = element['type']
            if element['type'] in self.elements_supported:
                draw_function = getattr(self, f"draw_{element_type}", None)
                if callable(draw_function):
                    draw_function(element)
                else:
                    print(f"Function '{element_type}' is not defined.")
        return self.image

    def draw_rect(self, element):
        """
        Draws a rectangle on the image.

        Args:
            element (dict): Attributes of the rectangle, including:
                - 'x' (float): Top-left x-coordinate.
                - 'y' (float): Top-left y-coordinate.
                - 'width' (float): Width of the rectangle.
                - 'height' (float): Height of the rectangle.
                - 'fill' (str): Fill color.
                - 'stroke' (str): Stroke color.
        """
        x = element['x']
        y = element['y']
        w = element['width']
        h = element['height']
        fill = element['fill']
        stroke = element['stroke']
        width = element['stroke-width']

        self.draw.rectangle([x, y, x + w, y + h], fill=fill, outline=stroke, width=width)

    def draw_circle(self, element):
        """
        Draws a circle on the image.

        Args:
            element (dict): Attributes of the circle, including:
                - 'cx' (float): X-coordinate of the center.
                - 'cy' (float): Y-coordinate of the center.
                - 'r' (float): Radius of the circle.
                - 'fill' (str): Fill color.
                - 'stroke' (str): Stroke color.
        """

        cx = element['cx']
        cy = element['cy']
        r = element['r']
        fill = element['fill']
        stroke = element['stroke']
        width = element['stroke-width']
        self.draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fill, outline=stroke, width=width)

    def draw_line(self, element):
        """
        Draws a line on the image.

        Args:
            element (dict): Attributes of the line, including:
                - 'x1' (float): Start x-coordinate.
                - 'y1' (float): Start y-coordinate.
                - 'x2' (float): End x-coordinate.
                - 'y2' (float): End y-coordinate.
                - 'stroke' (str): Line color.
                - 'width' (int): Line width.
        """

        x1 = element['x1']
        y1 = element['y1']
        x2 = element['x2']
        y2 = element['y2']
        stroke = element['stroke']
        width = element['stroke-width']
        self.draw.line([x1, y1, x2, y2], fill=stroke, width=width)

    def draw_ellipse(self, element):
        """
        Draws an ellipse on the image.

        Args:
            element (dict): Attributes of the ellipse, including:
                - 'cx' (float): X-coordinate of the center.
                - 'cy' (float): Y-coordinate of the center.
                - 'rx' (float): Radius on the x-axis.
                - 'ry' (float): Radius on the y-axis.
                - 'fill' (str): Fill color.
                - 'stroke' (str): Stroke color.
        """
        cx = element['cx']
        cy = element['cy']
        rx = element['rx']
        ry = element['ry']
        stroke = element['stroke']
        fill = element['fill']
        width = element['stroke-width']
        self.draw.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=fill, outline=stroke, width=width)

    def draw_polyline(self, element):
        """
        Draws a polyline on the image.

        Args:
            element (dict): Attributes:
                - 'points' (str): Comma-separated coordinates ("x1,y1 x2,y2").
                - 'stroke' (str): Line color.
                - 'fill' (str): Fill color or None.
                - 'stroke-width' (int): Line width.
        """

        points = element['points'].split(' ')
        points = list(map(lambda x: (float(x.split(',')[0]), float(x.split(',')[1])), points))

        stroke = element['stroke']
        fill = element['fill']
        width = element['stroke-width']

        if fill:
            self.draw.polygon(points, fill=fill)
        if stroke:
            self.draw.line(points, fill=stroke, width=width)

    def draw_path(self, element):
        """
        Draws a path using SVG commands.

        Args:
            element (dict): Attributes:
                - 'd' (str): Path data (SVG format).
                - 'stroke' (str): Outline color.
                - 'fill' (str): Fill color or None.
                - 'stroke-width' (int): Line width.
        """
        path_data = element['d']
        stroke = element['stroke']
        fill = element['fill']
        width = element['stroke-width']

        parser = PathParser(path_data)
        points = parser.parse()
        if fill:
            self.draw.polygon(points, fill=fill)
        if stroke:
            self.draw.line(points, fill=stroke, width=width)

    def save_PNG(self, filename):
        """
        Saves the current image as a PNG file.

        Args:
            filename (str): The name of the file to save the image to.
        """

        self.image.save(filename)
        print("Successfully convert SVG file to PNG.")
