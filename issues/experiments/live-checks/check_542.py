"""#542/#543 on the live local app: create Test/Answer via admin forms, check author + list pages."""

import re
import subprocess
import time

import requests

BASE = "http://127.0.0.1:5000"


def sql(q):
    return subprocess.run(
        ["docker", "exec", "miminet-dev-pg", "psql", "-U", "postgres", "-d", "miminet", "-tAc", q],
        capture_output=True, text=True, check=True,
    ).stdout.strip()


s = requests.Session()
r = s.post(BASE + "/auth/login.html", data={"email": "selenium", "password": "password"})
print("login ->", r.status_code, r.url)

# --- Test (#542) ---
form = s.get(BASE + "/admin/test/new/").text
print("test form has author field:", "created_by_user" in form)
name = f"t542-{int(time.time())}"
r = s.post(BASE + "/admin/test/new/", data={"name": name, "description": "x"}, allow_redirects=False)
print("create test ->", r.status_code)
print("test created_by_id in DB:", repr(sql(f"select created_by_id from test where name = '{name}'")))
print("GET /admin/test/ ->", s.get(BASE + "/admin/test/").status_code)

# --- Answer (same mechanism) ---
qid = sql("insert into question (text, question_type, is_deleted, created_by_id) values ('q542', 0, false, 1) returning id").splitlines()[0]
form = s.get(BASE + "/admin/answer/new/").text
print("answer form has author field:", "created_by_user" in form)
variant = f"v542-{int(time.time())}"
r = s.post(BASE + "/admin/answer/new/", data={"question_id": qid, "variant": variant}, allow_redirects=False)
print("create answer ->", r.status_code)
print("answer created_by_id in DB:", repr(sql(f"select created_by_id from answer where variant = '{variant}'")))
print("GET /admin/answer/ ->", s.get(BASE + "/admin/answer/").status_code)

# --- Section form (#543) ---
form = s.get(BASE + "/admin/section/new/").text
for field in ("questions", "quiz_sessions"):
    print(f"section form has '{field}' field:", bool(re.search(rf'name="{field}"', form)))
