"""#524: generate a network preview through the UI and inspect its background."""

import subprocess
import sys
import time

from PIL import Image

import mm_browser as mb

repo_static = sys.argv[1]  # .../front/src/static
copy_to = sys.argv[2]

d = mb.make_driver()
try:
    mb.login(d)
    guid = mb.new_network(d)
    mb.drop_device(d, "host", -150, 0)
    mb.drop_device(d, "l2_switch", 100, -50)
    ids = mb.node_ids(d)
    print("connect:", mb.connect(d, ids[0], ids[1]))
    d.execute_script("TakeGraphPictureAndUpdate();")
    time.sleep(3)
finally:
    d.quit()

uri = subprocess.run(
    ["docker", "exec", "miminet-dev-pg", "psql", "-U", "postgres", "-d", "miminet", "-tAc",
     f"select preview_uri from network where guid = '{guid}'"],
    capture_output=True, text=True, check=True,
).stdout.strip()
print("preview_uri:", uri)

img = Image.open(f"{repo_static}/images/preview/{uri}")
print("mode:", img.mode, "size:", img.size)
rgba = img.convert("RGBA")
corner = rgba.getpixel((0, 0))
alpha_values = [p[3] for p in rgba.getdata()]
transparent = sum(1 for a in alpha_values if a == 0)
print("corner pixel RGBA:", corner)
print(f"fully transparent pixels: {transparent}/{len(alpha_values)} ({100 * transparent / len(alpha_values):.0f}%)")
img.save(copy_to)
