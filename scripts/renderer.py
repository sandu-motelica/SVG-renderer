from PIL import Image, ImageDraw
import re


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

    def __init__(self, width, height, elements_supported=None):
        """
        Initializes the Renderer with a blank image and supported elements.

        Args:
            width (int): Width of the image.
            height (int): Height of the image.
            elements_supported (list[str], optional): A list of element types that
                the renderer supports. If None, the default supported elements
                are ['rect', 'circle', 'line', 'ellipse', 'path'].
        """

        self.width = width
        self.height = height
        self.image = Image.new('RGBA', (width, height), (255, 255, 255, 0))
        self.elements_supported = elements_supported
        if self.elements_supported is None:
            self.elements_supported = elements_supported
        self.elements_supported = ['rect', 'circle', 'line', 'ellipse', 'path', 'polyline']
        self.draw = ImageDraw.Draw(self.image)

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
        width = element['width']
        self.draw.rectangle([x, y, x + w, y + h], fill=fill, outline=stroke)

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
        width = element['width']
        self.draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fill, outline=stroke)

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
        width = element['width']
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
        width = element['width']
        self.draw.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=fill, outline=stroke)

    def draw_polyline(self, element):
        points = element['points'].split(' ')
        points = list(map(lambda x: (float(x.split(',')[0]), float(x.split(',')[1])), points))
        print(points)

        stroke = element['stroke']
        fill = element['fill']
        width = element['width']

        if fill:
            self.draw.polygon(points, fill=fill)
        if stroke:
            self.draw.line(points, fill=stroke, width=width)

    def draw_path(self, element):
        path_data = element['d']
        stroke = element['stroke']
        fill = element['fill']
        width = element['width']
        commands = re.findall(r'[MmLlHhVvCcSsQqTtAaZz]|-?\d+\.?\d*', path_data)

        current_position = [0, 0]
        points = []
        last_command = None
        control_point = None

        while commands:
            cmd = commands.pop(0)
            if cmd in "Mm":
                x = float(commands.pop(0))
                y = float(commands.pop(0))
                if cmd == "m":
                    current_position = [current_position[0] + x, current_position[1] + y]
                else:
                    current_position = [x, y]
                points.append(tuple(current_position))
                last_command = cmd
            elif cmd in "Ll":
                x = float(commands.pop(0))
                y = float(commands.pop(0))
                if cmd == "l":
                    current_position = [current_position[0] + x, current_position[1] + y]
                else:
                    current_position = [x, y]
                points.append(tuple(current_position))
                last_command = cmd
            elif cmd in "Hh":
                x = float(commands.pop(0))
                if cmd == "h":
                    current_position[0] += x
                else:
                    current_position[0] = x
                points.append(tuple(current_position))
                last_command = cmd
            elif cmd in "Vv":
                y = float(commands.pop(0))
                if cmd == "v":
                    current_position[1] += y
                else:
                    current_position[1] = y
                points.append(tuple(current_position))
                last_command = cmd
            elif cmd in "Cc":
                x1 = float(commands.pop(0))
                y1 = float(commands.pop(0))
                x2 = float(commands.pop(0))
                y2 = float(commands.pop(0))
                x = float(commands.pop(0))
                y = float(commands.pop(0))
                if cmd == "c":
                    x1 += current_position[0]
                    y1 += current_position[1]
                    x2 += current_position[0]
                    y2 += current_position[1]
                    x += current_position[0]
                    y += current_position[1]
                bezier_points = self.generate_cubic_bezier_points(current_position, [x1, y1, x2, y2, x, y])
                points.extend(bezier_points)
                current_position = [x, y]
                control_point = [x2, y2]
                last_command = cmd
            elif cmd in "Ss":
                if last_command not in "CcSs":
                    control_point = current_position
                else:
                    control_point = [2 * current_position[0] - control_point[0],
                                     2 * current_position[1] - control_point[1]]
                x2 = float(commands.pop(0))
                y2 = float(commands.pop(0))
                x = float(commands.pop(0))
                y = float(commands.pop(0))
                if cmd == "s":
                    x2 += current_position[0]
                    y2 += current_position[1]
                    x += current_position[0]
                    y += current_position[1]
                bezier_points = self.generate_cubic_bezier_points(current_position,
                                                                  [control_point[0], control_point[1], x2, y2, x, y])
                points.extend(bezier_points)
                current_position = [x, y]
                control_point = [x2, y2]
                last_command = cmd
            elif cmd in "Qq":
                x1 = float(commands.pop(0))
                y1 = float(commands.pop(0))
                x = float(commands.pop(0))
                y = float(commands.pop(0))
                if cmd == "q":
                    x1 += current_position[0]
                    y1 += current_position[1]
                    x += current_position[0]
                    y += current_position[1]
                bezier_points = self.generate_quadratic_bezier_points(current_position, [x1, y1, x, y])
                points.extend(bezier_points)
                current_position = [x, y]
                control_point = [x1, y1]
                last_command = cmd
            elif cmd in "Tt":
                if last_command not in "QqTt":
                    control_point = current_position
                else:
                    control_point = [2 * current_position[0] - control_point[0],
                                     2 * current_position[1] - control_point[1]]
                x = float(commands.pop(0))
                y = float(commands.pop(0))
                if cmd == "t":
                    x += current_position[0]
                    y += current_position[1]
                bezier_points = self.generate_quadratic_bezier_points(current_position,
                                                                      [control_point[0], control_point[1], x, y])
                points.extend(bezier_points)
                current_position = [x, y]
                last_command = cmd
            elif cmd in "Aa":
                rx = float(commands.pop(0))
                ry = float(commands.pop(0))
                x_rot = float(commands.pop(0))
                large_arc = int(commands.pop(0))
                sweep = int(commands.pop(0))
                x = float(commands.pop(0))
                y = float(commands.pop(0))
                if cmd == "a":
                    x += current_position[0]
                    y += current_position[1]
                arc_points = self.generate_arc_points(current_position, rx, ry, x_rot, large_arc, sweep, [x, y])
                points.extend(arc_points)
                current_position = [x, y]
                last_command = cmd
            elif cmd in "Zz":
                points.append(points[0])
                last_command = cmd

        if fill:
            self.draw.polygon(points, fill=fill)
        if stroke:
            self.draw.line(points, fill=stroke, width=width)

    @staticmethod
    def generate_cubic_bezier_points(start_point, control_points):
        x1, y1, x2, y2, x3, y3 = control_points
        bezier_points = []
        for t in [i / 10 for i in range(11)]:
            bx = (1 - t) ** 3 * start_point[0] + 3 * (1 - t) ** 2 * t * x1 + 3 * (1 - t) * t ** 2 * x2 + t ** 3 * x3
            by = (1 - t) ** 3 * start_point[1] + 3 * (1 - t) ** 2 * t * y1 + 3 * (1 - t) * t ** 2 * y2 + t ** 3 * y3
            bezier_points.append((bx, by))
        return bezier_points

    @staticmethod
    def generate_quadratic_bezier_points(start_point, control_points):
        x1, y1, x2, y2 = control_points
        bezier_points = []
        for t in [i / 10 for i in range(11)]:
            bx = (1 - t) ** 2 * start_point[0] + 2 * (1 - t) * t * x1 + t ** 2 * x2
            by = (1 - t) ** 2 * start_point[1] + 2 * (1 - t) * t * y1 + t ** 2 * y2
            bezier_points.append((bx, by))
        return bezier_points

    @staticmethod
    def generate_arc_points(start_point, rx, ry, x_rot, large_arc, sweep, end_point):
        from math import cos, sin, radians, sqrt, atan2, pi

        x_rot = radians(x_rot)

        x1, y1 = start_point
        x2, y2 = end_point

        dx = (x1 - x2) / 2.0
        dy = (y1 - y2) / 2.0

        x1p = cos(x_rot) * dx + sin(x_rot) * dy
        y1p = -sin(x_rot) * dx + cos(x_rot) * dy

        rx_sq = rx ** 2
        ry_sq = ry ** 2
        x1p_sq = x1p ** 2
        y1p_sq = y1p ** 2

        radicand = max(0, (rx_sq * ry_sq - rx_sq * y1p_sq - ry_sq * x1p_sq) /
                       (rx_sq * y1p_sq + ry_sq * x1p_sq))
        c = sqrt(radicand) if large_arc != sweep else -sqrt(radicand)

        cxp = c * (rx * y1p) / ry
        cyp = c * -(ry * x1p) / rx

        cx = cos(x_rot) * cxp - sin(x_rot) * cyp + (x1 + x2) / 2
        cy = sin(x_rot) * cxp + cos(x_rot) * cyp + (y1 + y2) / 2

        theta1 = atan2((y1p - cyp) / ry, (x1p - cxp) / rx)
        delta_theta = atan2((-y1p - cyp) / ry, (-x1p - cxp) / rx) - theta1

        if not sweep:
            delta_theta -= 2 * pi
        elif sweep:
            delta_theta = (delta_theta + 2 * pi) % (2 * pi)

        num_points = 10
        arc_points = []
        for i in range(num_points + 1):
            t = i / num_points
            theta = theta1 + t * delta_theta
            x = cx + rx * cos(theta) * cos(x_rot) - ry * sin(theta) * sin(x_rot)
            y = cy + rx * cos(theta) * sin(x_rot) + ry * sin(theta) * cos(x_rot)
            arc_points.append((x, y))

        return arc_points

    def save_PNG(self, filename):
        """
        Saves the current image as a PNG file.

        Args:
            filename (str): The name of the file to save the image to.
        """

        self.image.save(filename)
