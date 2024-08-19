from pathlib import Path
import json
import time

import pcbnew

# Load the key layout data
with open(Path(__file__).parent / 'output/iris_layout.json') as f:
    key_layout = json.load(f)

assert isinstance(key_layout, list)
print(f"Loaded {len(key_layout)} keys.")

key_ref_identifier_list = [
    f"K{page}{num:02d}"
    for page in [3,4,5,6]
    for num in range(1, 16+1)
]

key_layout.sort(
    key=lambda k: (
        k['center_abs_x_units'] * 1000 + k['center_abs_y_units']
        if k['center_abs_y_units'] < 4.9
        # Else: The bottom row goes at the end.
        else 1e6 + (k['center_abs_x_units'] * 1000)
    )
)

board = pcbnew.GetBoard()
assert board

# Magic factor, based on the effective Dots-per-mm (from loading the SVG in Inkscape),
# as well as based on the empirical scale factor of loading the SVG into KiCad.
UNIT_TO_MM_SCALE = (79.37500/300) * 65

for i, key in enumerate(key_layout):
    ref_id = key_ref_identifier_list[i]
    print(f"Placing {ref_id} at: {key}")
    
    footprint = board.FindFootprintByReference(ref_id)
    assert footprint, f"Could not find footprint with reference {ref_id}"
    footprint.SetPosition(
        pcbnew.VECTOR2I_MM(
            21 + (key['center_abs_x_units'] - key['width_units']/2) * UNIT_TO_MM_SCALE,
            22.2 + (key['center_abs_y_units'] - key['height_units']/2) * UNIT_TO_MM_SCALE,
        )
    )
    pcbnew.Refresh()

    # if i > 20:
    #     print("Early debugging exit.")
    #     break

print("Done.")
