#!/bin/sh
# Run the miminet front (Flask dev server) from the working copy against the dev Postgres container.
PY="C:/Users/PCyur/AppData/Local/Temp/claude/C--Users-PCyur-OneDrive-----------miminet/21426821-2124-44cb-890b-8c18cde00d1d/scratchpad/src/.venv/Scripts/python.exe"
cd "C:/Users/PCyur/OneDrive/Документы/miminet/miminet/front/src" || exit 1
MODE=dev SQLALCHEMY_DATABASE_URI="postgresql+psycopg2://postgres:my_postgres@localhost:5430/miminet" PYTHONIOENCODING=utf-8 \
  exec "$PY" -c "from app import app; app.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False)"
