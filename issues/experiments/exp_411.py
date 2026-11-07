"""#411/#412: stale pooled connection and connect hang, with/without engine options."""

import os
import time

from sqlalchemy import create_engine, text

URL = os.environ["DB_URL"]


def stale_connection(**opts):
    engine = create_engine(URL, pool_size=1, **opts)
    with engine.connect() as c:
        pid = c.execute(text("select pg_backend_pid()")).scalar()
    # Server side drops the idle pooled connection (what pgbouncer/managed PG
    # failover does) - simulated with pg_terminate_backend from another session.
    admin = create_engine(URL, poolclass=None)
    with admin.connect() as c:
        c.execute(text("select pg_terminate_backend(:p)"), {"p": pid})
    admin.dispose()
    try:
        with engine.connect() as c:
            c.execute(text("select 1"))
        return "OK"
    except Exception as e:
        return f"{type(e).__name__}: {str(e).splitlines()[0]}"
    finally:
        engine.dispose()


print("stale conn, as in main:        ", stale_connection())
print("stale conn, pool_pre_ping=True:", stale_connection(pool_pre_ping=True))

# Unreachable host: 10.255.255.1 drops SYNs, like the timed-out managed DB host.
dead = "postgresql+psycopg2://u:p@10.255.255.1:6432/db"
t = time.time()
try:
    create_engine(dead, connect_args={"connect_timeout": 3}).connect()
except Exception as e:
    print(f"connect_timeout=3: failed after {time.time() - t:.1f}s ({type(e).__name__})")
