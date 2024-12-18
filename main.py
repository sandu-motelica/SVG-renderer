from scripts.svg_parser import Parser

if __name__ == '__main__':
    # help(Parser)

    p = Parser("data\\example.svg")
    p.parse()
