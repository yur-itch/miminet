"""#543: time the admin section edit form for a section with many quiz sessions."""

import re
import statistics
import time

import requests

BASE = "http://127.0.0.1:5000"
s = requests.Session()
s.post(BASE + "/auth/login.html", data={"email": "selenium", "password": "password"})

times, size, html = [], 0, ""
for _ in range(5):
    t = time.perf_counter()
    r = s.get(BASE + "/admin/section/edit/?id=1")
    times.append(time.perf_counter() - t)
    size, html = len(r.content), r.text
print("status:", r.status_code)
print(f"edit form: median {statistics.median(times) * 1000:.0f} ms, size {size / 1024:.0f} KiB")
for field in ("questions", "quiz_sessions"):
    print(f"field '{field}' present:", bool(re.search(rf'name="{field}"', html)))
print("<option> count:", html.count("<option"))
