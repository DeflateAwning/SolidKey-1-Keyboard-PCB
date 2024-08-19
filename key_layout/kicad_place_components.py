from pathlib import Path
import json
import time

import pcbnew

# Load the key layout data
with open(Path(__file__) / 'output/iris_layout.json') as f:
    key_layout = json.load(f)

assert isinstance(key_layout, list)
print(f"Loaded {len(key_layout)} keys.")

key_ref_identifier_list = [
    f"K{page}{num:02d}"
    for page in [1,2,3,4]
    for num in range(1, 16+1)
]

key_layout.sort(key=lambda k: k['center_abs_x_units'] * 1000 + k['center_abs_y_units'])

board = pcbnew.GetBoard()

for i, key in enumerate(key_layout):
    ref_id = key_ref_identifier_list[i]
    print(f"Placing {ref_id} at: {key}")
    
    footprint = board.FindFootprintByReference(ref_id)
    footprint.SetPosition(pcbnew.VECTOR2I_MM(key['center_abs_x_units'], key['center_abs_y_units']))
    pcbnew.Refresh()

    time.sleep(5)

print("Done.")
