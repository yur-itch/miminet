"""#411: drop the server's pooled DB connections, then hit DB-backed pages."""

import subprocess

import requests

BASE = "http://127.0.0.1:5000"
s = requests.Session()
s.post(BASE + "/auth/login.html", data={"email": "selenium", "password": "password"})
for _ in range(3):  # warm the pool
    s.get(BASE + "/home")

killed = subprocess.run(
    ["docker", "exec", "miminet-dev-pg", "psql", "-U", "postgres", "-d", "miminet", "-tAc",
     "select count(pg_terminate_backend(pid)) from pg_stat_activity "
     "where datname = 'miminet' and pid <> pg_backend_pid()"],
    capture_output=True, text=True, check=True,
).stdout.strip()
print("terminated server-side connections:", killed)

for path in ("/home", "/home", "/home"):
    r = s.get(BASE + path, allow_redirects=False)
    print(f"GET {path} -> {r.status_code}")
