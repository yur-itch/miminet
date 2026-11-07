"""Open the main pages as the logged-in test user and report console errors."""
import mm_browser as mb

d = mb.make_driver()
try:
    mb.login(d)
    for path in ["/", "/home", "/user/profile.html", "/examples", "/course", "/quiz/test/all", "/admin/", "/admin/test/", "/admin/section/", "/admin/answer/"]:
        d.get(mb.BASE + path)
        errs = [m[:140] for m in mb.severe_console(d) if "favicon" not in m]
        print(f"{path:22} title={d.title[:30]!r:34} console errors: {errs if errs else 'none'}")
    guid = mb.new_network(d)
    print(f"{'/web_network':22} editor loaded, console errors: {mb.severe_console(d) or 'none'}")
finally:
    d.quit()
