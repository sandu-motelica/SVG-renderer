from PIL import Image, ImageDraw


class Renderer:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.image = Image.new('RGBA', (width, height), (255, 255, 255, 0))
        self.elements_supported = ['rect', 'circle', 'line', 'ellipse']
        self.draw = ImageDraw.Draw(self.image)

    def draw_elements(self, elements):
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
        x = element['x']
        y = element['y']
        w = element['width']
        h = element['height']
        fill = element['fill']
        stroke = element['stroke']
        self.draw.rectangle([x, y, x + w, y + h], fill=fill, outline=stroke)

    def draw_circle(self, element):
        cx = element['cx']
        cy = element['cy']
        r = element['r']
        fill = element['fill']
        stroke = element['stroke']
        self.draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fill, outline=stroke)

    def draw_line(self, element):
        x1 = element['x1']
        y1 = element['y1']
        x2 = element['x2']
        y2 = element['y2']
        stroke = element['stroke']
        width = element['width']
        self.draw.line([x1, y1, x2, y2], fill=stroke, width=width)

    def draw_ellipse(self, element):
        cx = element['cx']
        cy = element['cy']
        rx = element['rx']
        ry = element['ry']
        stroke = element['stroke']
        fill = element['fill']
        self.draw.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=fill, outline=stroke)

    def save_PNG(self, filename):
        self.image.save(filename)
