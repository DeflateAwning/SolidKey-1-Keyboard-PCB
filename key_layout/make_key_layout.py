import json
import re
from pathlib import Path

import svgwrite

# Key Layout is downloaded from URL, and stored in this repo:
# https://gist.githubusercontent.com/filoxo/98b578d90ebc699eaa30546a98a3ad6a/raw/1f3a0dddb1bc86494af2529e08c850739f513c87/Iris-macmap.kbd.json
# View the layout at: http://www.keyboard-layout-editor.com/#/gists/98b578d90ebc699eaa30546a98a3ad6a
FOLDER = Path(__file__).parent

# After all that, I found the spec: https://github.com/ijprest/keyboard-layout-editor/wiki/Serialized-Data-Format

def load_file() -> list:
    # Load the key layout input_data.
    with open(FOLDER / 'input' / 'iris_keymap_layout_input.json') as f:
        input_data = json.load(f)

    assert isinstance(input_data, list)

    # Check them remove the first element (dict containing only a "name" field).
    assert isinstance(input_data[0], dict)
    assert len(input_data[0]) == 1
    input_data = input_data[1:]

    return input_data

def parse_file(input_data: list) -> list[dict]:
    # Make a new list-of-dicts with the input_data we care about.
    # This format is wacky.
    key_layout: list[dict] = []
    all_fields = set()

    running_y = 0
    last_color = None

    for row_num, row in enumerate(input_data):
        assert isinstance(row, list)
        running_x = 0
        running_y += 1 + row[0].get('y', 0)

        key_num_in_row: int = 0
        while key_num_in_row < len(row):
            if isinstance(row[key_num_in_row], str):
                key_data: dict = dict()
                key_name: str = row[key_num_in_row]
                key_num_in_row += 1
            elif isinstance(row[key_num_in_row], dict):
                assert key_num_in_row + 1 < len(row), f"Expected a name after a data dict, but not enough elements in row."
                key_data = row[key_num_in_row].copy()
                key_name = row[key_num_in_row + 1]
                key_num_in_row += 2

            assert isinstance(key_data, dict)
            assert isinstance(key_name, str)
            if key_num_in_row == 0:
                assert 'y' not in key_data, f"Expected 'y' to only be in the first key of each row"

            # Track all the fields, for fun.
            all_fields.update(key_data.keys())

            # Update the running values.
            running_x += 1 + key_data.get('x', 0)
            last_color = key_data.get('c', last_color)

            # Add the key data to the key_layout.
            key_layout.append({
                'raw_name': key_name,
                'main_name': re.split(r'\s+', key_name)[-1], # Main name comes last.
                'all_names': re.split(r'\s+', key_name),
                'center_abs_x_units': running_x,
                'center_abs_y_units': running_y,
                'row_num': row_num,
                'key_num_in_row': key_num_in_row,
                # Probably don't really care about the following ones.
                'rotate_deg': key_data.get('r', 0),
                'rotate_point_x': key_data.get('rx', 0), # Should be absolute.
                'rotate_point_y': key_data.get('ry', 0),
                'width_units': key_data.get('w', 1),
                'height_units': key_data.get('h', 1),
                'color': last_color,
                'legend_size': key_data.get('f', None),
                'raw_x': key_data.get('x', None),
                'raw_y': key_data.get('y', None),
            })

    # Print all the fields we found.
    print(f"Found the following fields: {all_fields}")
    print(f"Found {len(key_layout)} keys.")

    return key_layout

def write_svg_layout(key_layout: list[dict], output_file: str | Path):
    """Display key layout in a graphic.
    """
    # Notes:
    # - In SVG files, the origin is at the top-left corner.

    # Create a new SVG drawing
    svg_drawing = svgwrite.Drawing(output_file, profile='tiny')

    # Set some basic parameters for units and scaling
    UNIT_SIZE = 50  # Size of one unit in pixels
    RECT_OPACITY = 1
    DRAW_KEY_LABELS = False
    DRAW_KEY_METADATA_LABELS = False
    DRAW_KEY_CENTER_CIRCLE = True

    # Find x/y min values to offset, if required.
    min_x = min(key['center_abs_x_units'] for key in key_layout)
    min_y = min(key['center_abs_y_units'] for key in key_layout)

    for key in key_layout:
        # Calculate position and size
        x = (key['center_abs_x_units'] - min_x) * UNIT_SIZE
        y = (key['center_abs_y_units'] - min_y) * UNIT_SIZE
        width = key['width_units'] * UNIT_SIZE
        height = key['height_units'] * UNIT_SIZE
        # rotation = key['rotate_deg']
        color = key['color'] if key['color'] else 'red'
        # legend_size = key['legend_size'] if key['legend_size'] else 12
        legend_size = 12

        # Create a group for each key to handle rotation
        # g = svg_drawing.g(transform=f"rotate({rotation},{x + width / 2},{y + height / 2})")
        g = svg_drawing.g()

        # Draw the key rectangle
        g.add(
            svg_drawing.rect(
                insert=(x, y),
                size=(width, height),
                fill=color,
                opacity=RECT_OPACITY,
                stroke='black'
            )
        )

        # Add the key label
        if DRAW_KEY_LABELS:
            g.add(
                svg_drawing.text(
                    f"{key['main_name']}",
                    insert=(x + width / 2, y + height / 2),
                    text_anchor="middle",
                    # alignment_baseline="middle",
                    font_size=legend_size,
                    fill='black'
                )
            )

        # Debugging: Add some metadata to the key.
        if DRAW_KEY_METADATA_LABELS:
            g.add(
                svg_drawing.text(
                    f"({key['center_abs_x_units']:.2f}, {key['center_abs_y_units']:.2f})",
                    insert=(x + width / 2, y + height / 2 + 15),
                    text_anchor="middle",
                    # alignment_baseline="middle",
                    font_size=8,
                    fill='black'
                )
            )
        
        if DRAW_KEY_CENTER_CIRCLE:
            g.add(
                svg_drawing.circle(
                    center=(x + width / 2, y + height / 2),
                    r=0.02 * UNIT_SIZE,
                    fill='black'
                )
            )

        # Add the group to the drawing
        svg_drawing.add(g)

    # Save the SVG file
    svg_drawing.save()


def main():
    input_data = load_file()
    key_layout = parse_file(input_data)
    
    # Write the key layout to a file.
    (FOLDER / 'output').mkdir(exist_ok=True)
    with open(FOLDER / 'output' / 'iris_layout.json', 'w') as f:
        json.dump(key_layout, f, indent=2)

    write_svg_layout(key_layout, FOLDER / 'output' / 'iris_layout.svg')

if __name__ == '__main__':
    main()
