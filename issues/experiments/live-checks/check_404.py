"""#404: connect host<->switch and host<->hub, with and without a foreign `const port`."""

import sys

import mm_browser as mb

shot_dir = sys.argv[1]

for label, preload in [("clean", None), ("foreign-const-port", "const port = 'from-extension';")]:
    d = mb.make_driver(preload)
    try:
        print(f"--- {label} ---")
        print("login:", mb.login(d))
        guid = mb.new_network(d)
        mb.drop_device(d, "host", -150, 0)
        mb.drop_device(d, "l2_switch", 0, -100)
        mb.drop_device(d, "l1_hub", 150, 0)
        ids = mb.node_ids(d)
        print("nodes:", ids)
        host = next(i for i in ids if i.startswith("host"))
        sw = next(i for i in ids if i.startswith("l2sw"))
        hub = next(i for i in ids if i.startswith("l1hub"))
        print("connect host-switch:", mb.connect(d, host, sw))
        print("connect host-hub:   ", mb.connect(d, host, hub))
        print("edges:", mb.edges_info(d))
        print("severe console:", [m[:160] for m in mb.severe_console(d)])
        d.save_screenshot(f"{shot_dir}/check404_{label}.png")
    finally:
        d.quit()
