# SVG Renderer

## Overview
`SVG Renderer` is a Python application that converts SVG files into PNG images. It supports key SVG elements such as rectangles, circles, ellipses, lines, paths, and polylines. The rendering process uses `Pillow` for creating and manipulating PNG images.

---

## Features
- Supports SVG elements: `<rect>`, `<circle>`, `<ellipse>`, `<line>`, `<path>`, `<polyline>`.
- Handles attributes like `stroke`, `fill`, and `stroke-width`.
- Converts SVG files into PNG format.

---

## Requirements
- Python 3.7+
- Install dependencies with:
  ```bash
  pip install pillow
  ```

---

## Usage
Run the application from the command line:
```bash
python main.py <input_file.svg> <output_file.png>
```

### Example:
```bash
python main.py example.svg output.png
```

---

## Project Structure
```
.
├── main.py             # Entry point of the application
├── scripts/
│   ├── svg_parser.py   # Parses SVG files
│   ├── renderer.py     # Renders parsed elements
│   ├── path_parser.py  # Decodes <path> commands
└── README.md           # Project documentation
```

---

## Example
### Input (`example.svg`):
```xml
<svg width="100" height="100">
  <rect x="10" y="10" width="80" height="80" fill="blue" stroke="black" />
  <circle cx="50" cy="50" r="30" fill="red" />
</svg>
```

### Output (`output.png`):
A PNG image with a blue rectangle and a red circle.
