# Experiments used for the difficulty estimates (2026-10-23)

Run outside the repo, against a throwaway Postgres:

```bash
docker run -d --rm --name mm-pg-test -e POSTGRES_PASSWORD=test -p 55432:5432 postgres:16-alpine
uv venv venv --python 3.12
uv pip install --python venv/Scripts/python.exe "Flask==3.1.3" "Flask-Admin==2.0.1" "Flask-SQLAlchemy==3.1.1" "SQLAlchemy==2.0.43" "wtforms==3.2.1" "psycopg2-binary==2.9.10"
export DB_URL="postgresql+psycopg2://postgres:test@localhost:55432/postgres"
python exp_542.py main; python exp_542.py fixed   # #542
python exp_535.py                                  # #535
python exp_411.py                                  # #411/#412
node exp_404.mjs                                   # #404
# implicit globals in front JS (needs: npm i espree eslint-scope)
node implicit_globals.mjs <path-to-repo>/front/src/static/*.js
```

| Script | Result |
|---|---|
| `exp_542.py` | as in main: `created_by_id = None`; with fields excluded from the form: `created_by_id = 1` |
| `exp_535.py` | reopened task → `0/1` (NULLS FIRST); after `finish_old_sessions` → `0/1` even with `nulls_last()`; "best finished" → `1/1` |
| `exp_411.py` | stale pooled conn: `OperationalError` → with `pool_pre_ping=True`: OK; `connect_timeout=3` fails in 3.0 s instead of ~130 s |
| `exp_404.mjs` | foreign `const port` + sloppy `port = ...` → `TypeError: Assignment to constant variable.`; with `let` → OK |
| `implicit_globals.mjs` | 51 writes to undeclared names (20 names) in `front/src/static/*.js` |

## live-checks/ — checks against the running local front (used for the fixes, 2026-10-23)
Stand: `docker run -d --name miminet-dev-pg -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=my_postgres -e POSTGRES_DB=miminet -p 5430:5432 postgres:18`,
init once with `MODE=dev SQLALCHEMY_DATABASE_URI=postgresql+psycopg2://postgres:my_postgres@localhost:5430/miminet python app.py dev` (from `front/src`),
then `run_front.sh` / `restart_front.sh` (Flask on 127.0.0.1:5000; paths inside point to this session's venv — adjust).
Login: `selenium` / `password`; for admin pages set `role = 2` for that user in the DB.
Browser checks use headless Edge via Selenium (`mm_browser.py`). On Windows, kill old servers before restarting:
two processes can listen on :5000 at once (SO_REUSEADDR) and requests go to the stale one.
