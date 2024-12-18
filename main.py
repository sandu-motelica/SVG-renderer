from scripts.svg_parser import Parser
from scripts.renderer import Renderer

if __name__ == '__main__':
    # help(Parser)

    p = Parser("data\\example.svg")
    elements = p.parse()
    r = Renderer(200, 200)
    r.draw_elements(elements)
    r.save_PNG("output.png")
