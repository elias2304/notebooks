import json
import base64
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

nb = json.load(open('tis/hw1/hw1.ipynb', encoding='utf-8'))

out_dir = Path('tis/hw1/extracted_assets')
out_dir.mkdir(exist_ok=True)

# Extract images
for i, name in [(24, 'daily_plot.png'), (26, 'monthly_plot.png'), (28, 'yearly_plot.png')]:
    outputs = nb['cells'][i]['outputs']
    for out in outputs:
        data = out.get('data', {})
        if 'image/png' in data:
            img_bytes = base64.b64decode(data['image/png'])
            (out_dir / name).write_bytes(img_bytes)
            print(f"Saved {name}, size: {len(img_bytes)} bytes")

# Check cell 5, 11, 15, 17, 21
for idx in [3, 5, 7, 9, 11, 13, 15, 17, 19, 21]:
    cell = nb['cells'][idx]
    print(f"\n--- CELL {idx} ---")
    for out in cell.get('outputs', []):
        if out.get('text'):
            print("STREAM:", ''.join(out['text']).strip())
        if out.get('data', {}).get('text/plain'):
            print("TEXT/PLAIN:\n", ''.join(out['data']['text/plain']).strip())
