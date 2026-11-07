# #411 500 на сервере (SSL SYSCALL error: EOF detected)

**Статус:** 🟢 свободна · **Issue:** https://github.com/mimi-net/miminet/issues/411 · 2026-03-25 · описания нет, только лог
**Сложность:** низкая · **Linux-бэкенд:** не нужен

## Суть
`/emulation_queue/size`: `psycopg2.OperationalError: SSL SYSCALL error: EOF detected`. Это классический симптом
**протухшего соединения в пуле**: сервер или pgbouncer закрыл соединение, а SQLAlchemy отдал его из пула.
По времени (13:28 против 13:17) это тот же инцидент, что и #412.

## Что сейчас в коде
- `pool_pre_ping` не включён ([`app.py:252-258`](https://github.com/mimi-net/miminet/blob/24c36f3/front/src/app.py#L252)).
- `/emulation_queue/size` фронт опрашивает периодически, поэтому он первым ловит битое соединение.

## Что сделать
См. #412: `pool_pre_ping=True` + `pool_recycle` прямо лечат этот случай. Ещё можно сделать `get_emulation_queue_size`
([`miminet_network.py:608`](https://github.com/mimi-net/miminet/blob/24c36f3/front/src/miminet_network.py#L608)) устойчивым: при `OperationalError` возвращать последнее
значение или 503, а не 500.

---

## Оценка сложности фикса (проверено 2026-10-23, общий PR с #412)

**Вердикт: 🟢 ЛЕГКО.** Закрывается тем же PR, что и #412 (`pool_pre_ping` + `pool_recycle`).

**Доказательство** (`experiments/exp_411.py`, PostgreSQL 16): соединение из пула закрыто на стороне сервера
(`pg_terminate_backend`, как при обрыве на pgbouncer или managed PG):
```
stale conn, as in main:         OperationalError: server closed the connection unexpectedly
stale conn, pool_pre_ping=True: OK
```
На проде то же самое выглядит как `SSL SYSCALL error: EOF detected`, потому что соединение идёт по SSL.

**Проверенная и отброшенная версия:** соединения, общие для форкнутых uwsgi-воркеров. Это маловероятно: БД инициализирует отдельный
процесс `python3 app.py` до запуска uwsgi (`front/run_app.sh`). Но `uwsgi.ini` лежит в `.gitignore`, проверить `lazy-apps` нельзя.
Стоит упомянуть это в PR как вопрос.

**Подробности изменений и тестов** см. в `412-db-timeout-500.md`.

---

## Статус: исправлено локально (2026-10-23)
Ветка `fix/412-db-connection-resilience-front` в `..\miminet`, черновик PR: [`drafts/pr-411-412.md`](drafts/pr-411-412.md). Обрыв соединения: до фикса 500, после 200.
