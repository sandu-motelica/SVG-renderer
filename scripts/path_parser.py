import re


class PathParser:
    """
    Parses SVG path data and generates a list of points for rendering.

    Supports commands: M, L, H, V, C, S, Q, T, A, Z (and their lowercase equivalents).
    """

    def __init__(self, path_data):
        """
        Initializes the parser with SVG path data.

        Args:
            path_data (str): SVG path data string containing commands and coordinates.
        """
        self.commands = re.findall(r'[MmLlHhVvCcSsQqTtAaZz]|-?\d+\.?\d*', path_data)
        self.current_position = [0, 0]
        self.points = []
        self.last_command = None
        self.control_point = None

    def parse(self):
        """
        Parses the path data and generates a list of points.

        Returns:
            list[tuple]: List of (x, y) coordinates for rendering.
        """
        while self.commands:
            cmd = self.commands.pop(0)
            if cmd in "Mm":
                self._handle_move_to(cmd)
            elif cmd in "Ll":
                self._handle_line_to(cmd)
            elif cmd in "Hh":
                self._handle_horizontal_line_to(cmd)
            elif cmd in "Vv":
                self._handle_vertical_line_to(cmd)
            elif cmd in "Cc":
                self._handle_cubic_bezier(cmd)
            elif cmd in "Ss":
                self._handle_smooth_cubic_bezier(cmd)
            elif cmd in "Qq":
                self._handle_quadratic_bezier(cmd)
            elif cmd in "Tt":
                self._handle_smooth_quadratic_bezier(cmd)
            elif cmd in "Aa":
                self._handle_arc(cmd)
            elif cmd in "Zz":
                self._handle_close_path()
            self.last_command = cmd
        return self.points

    def _handle_move_to(self, cmd):
        """
        Processes M/m commands to move to a new point.

        Args:
            cmd (str): The SVG command ('M' or 'm').
        """
        x, y = float(self.commands.pop(0)), float(self.commands.pop(0))
        self.current_position = [self.current_position[0] + x, self.current_position[1] + y] if cmd == "m" else [x, y]
        self.points.append(tuple(self.current_position))

    def _handle_line_to(self, cmd):
        """
        Processes L/l commands to draw a straight line.

        Args:
            cmd (str): The SVG command ('L' or 'l').
        """
        x, y = float(self.commands.pop(0)), float(self.commands.pop(0))
        self.current_position = [self.current_position[0] + x, self.current_position[1] + y] if cmd == "l" else [x, y]
        self.points.append(tuple(self.current_position))

    def _handle_horizontal_line_to(self, cmd):
        """
        Processes H/h commands to draw a horizontal line.

        Args:
            cmd (str): The SVG command ('H' or 'h').
        """
        x = float(self.commands.pop(0))
        self.current_position[0] = self.current_position[0] + x if cmd == "h" else x
        self.points.append(tuple(self.current_position))

    def _handle_vertical_line_to(self, cmd):
        """
        Processes V/v commands to draw a vertical line.

        Args:
            cmd (str): The SVG command ('V' or 'v').
        """
        y = float(self.commands.pop(0))
        self.current_position[1] = self.current_position[1] + y if cmd == "v" else y
        self.points.append(tuple(self.current_position))

    def _handle_cubic_bezier(self, cmd):
        """
        Processes C/c commands to draw a cubic Bezier curve.

        Args:
            cmd (str): The SVG command ('C' or 'c').
        """
        x1, y1, x2, y2, x, y = (float(self.commands.pop(0)) for _ in range(6))
        if cmd == "c":
            x1, y1, x2, y2, x, y = [v + self.current_position[i % 2] for i, v in enumerate([x1, y1, x2, y2, x, y])]
        bezier_points = self.generate_cubic_bezier_points(self.current_position, [x1, y1, x2, y2, x, y])
        self.points.extend(bezier_points)
        self.current_position, self.control_point = [x, y], [x2, y2]

    def _handle_smooth_cubic_bezier(self, cmd):
        """
        Processes S/s commands for smooth cubic Bezier curves.

        Args:
            cmd (str): The SVG command ('S' or 's').
        """
        if self.last_command not in "CcSs":
            self.control_point = self.current_position
        else:
            self.control_point = [2 * self.current_position[i] - self.control_point[i] for i in range(2)]
        x2, y2, x, y = (float(self.commands.pop(0)) for _ in range(4))
        if cmd == "s":
            x2, y2, x, y = [v + self.current_position[i % 2] for i, v in enumerate([x2, y2, x, y])]
        bezier_points = self.generate_cubic_bezier_points(self.current_position, [*self.control_point, x2, y2, x, y])
        self.points.extend(bezier_points)
        self.current_position, self.control_point = [x, y], [x2, y2]

    def _handle_quadratic_bezier(self, cmd):
        """
        Processes Q/q commands to draw a quadratic Bezier curve.

        Args:
            cmd (str): The SVG command ('Q' or 'q').
        """
        x1, y1, x, y = (float(self.commands.pop(0)) for _ in range(4))
        if cmd == "q":
            x1, y1, x, y = [v + self.current_position[i % 2] for i, v in enumerate([x1, y1, x, y])]
        bezier_points = self.generate_quadratic_bezier_points(self.current_position, [x1, y1, x, y])
        self.points.extend(bezier_points)
        self.current_position, self.control_point = [x, y], [x1, y1]

    def _handle_smooth_quadratic_bezier(self, cmd):
        """
        Processes T/t commands for smooth quadratic Bezier curves.

        Args:
            cmd (str): The SVG command ('T' or 't').
        """
        if self.last_command not in "QqTt":
            self.control_point = self.current_position
        else:
            self.control_point = [2 * self.current_position[i] - self.control_point[i] for i in range(2)]
        x, y = float(self.commands.pop(0)), float(self.commands.pop(0))
        if cmd == "t":
            x, y = [v + self.current_position[i % 2] for i, v in enumerate([x, y])]
        bezier_points = self.generate_quadratic_bezier_points(self.current_position, [*self.control_point, x, y])
        self.points.extend(bezier_points)
        self.current_position = [x, y]

    def _handle_arc(self, cmd):
        """
        Processes A/a commands to draw an elliptical arc.

        Args:
            cmd (str): The SVG command ('A' or 'a').
        """
        rx, ry, x_rot, large_arc, sweep, x, y = (float(self.commands.pop(0)) if i < 5 else int(self.commands.pop(0)) for
                                                 i in range(7))
        if cmd == "a":
            x, y = x + self.current_position[0], y + self.current_position[1]
        arc_points = self.generate_arc_points(self.current_position, rx, ry, x_rot, large_arc, sweep, [x, y])
        self.points.extend(arc_points)
        self.current_position = [x, y]

    def _handle_close_path(self):
        """
        Processes Z/z commands to close the current path.
        """
        self.points.append(self.points[0])

    @staticmethod
    def generate_cubic_bezier_points(start_point, control_points):
        """
        Generates points for a cubic Bezier curve.

        Args:
            start_point (list[float]): Starting point [x, y].
            control_points (list[float]): Control points and end point [x1, y1, x2, y2, x3, y3].

        Returns:
            list[tuple]: Points along the cubic Bezier curve.
        """

        x1, y1, x2, y2, x3, y3 = control_points
        bezier_points = []
        for t in [i / 10 for i in range(11)]:
            bx = (1 - t) ** 3 * start_point[0] + 3 * (1 - t) ** 2 * t * x1 + 3 * (1 - t) * t ** 2 * x2 + t ** 3 * x3
            by = (1 - t) ** 3 * start_point[1] + 3 * (1 - t) ** 2 * t * y1 + 3 * (1 - t) * t ** 2 * y2 + t ** 3 * y3
            bezier_points.append((bx, by))
        return bezier_points

    @staticmethod
    def generate_quadratic_bezier_points(start_point, control_points):
        """
        Generates points for a quadratic Bezier curve.

        Args:
            start_point (list[float]): Starting point [x, y].
            control_points (list[float]): Control point and end point [x1, y1, x2, y2].

        Returns:
            list[tuple]: Points along the quadratic Bezier curve.
        """
        x1, y1, x2, y2 = control_points
        bezier_points = []
        for t in [i / 10 for i in range(11)]:
            bx = (1 - t) ** 2 * start_point[0] + 2 * (1 - t) * t * x1 + t ** 2 * x2
            by = (1 - t) ** 2 * start_point[1] + 2 * (1 - t) * t * y1 + t ** 2 * y2
            bezier_points.append((bx, by))
        return bezier_points

    @staticmethod
    def generate_arc_points(start_point, rx, ry, x_rot, large_arc, sweep, end_point):
        """
        Generates points for an elliptical arc.

        Args:
            start_point (list[float]): Starting point [x, y].
            rx (float): X-axis radius.
            ry (float): Y-axis radius.
            x_rot (float): Rotation of the ellipse in degrees.
            large_arc (int): Flag for large arc (1 = true, 0 = false).
            sweep (int): Flag for arc direction (1 = clockwise, 0 = counterclockwise).
            end_point (list[float]): Ending point [x, y].

        Returns:
            list[tuple]: Points along the elliptical arc.
        """
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

        radicand = max(0, int((rx_sq * ry_sq - rx_sq * y1p_sq - ry_sq * x1p_sq) /
                              (rx_sq * y1p_sq + ry_sq * x1p_sq)))
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
