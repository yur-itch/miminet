# #412 Ошибка 500 на сервере (таймаут подключения к PostgreSQL)

**Статус:** 🟢 свободна · **Issue:** https://github.com/mimi-net/miminet/issues/412 · 2026-03-25 · описания нет, только лог
**Сложность:** низкая (защитная часть) · **Linux-бэкенд:** не нужен

## Суть
`psycopg2.OperationalError: connection to server at "...mdb.yandexcloud.net" port 6432 failed: Connection timed out`.
Запрос `/web_network` висел 130 секунд, затем 500. Причина инфраструктурная (Managed PostgreSQL или pgbouncer был недоступен).

## Что сейчас в коде
- В [`app.py:252-258`](https://github.com/mimi-net/miminet/blob/24c36f3/front/src/app.py#L252) задаётся только `SQLALCHEMY_DATABASE_URI`. Нет `SQLALCHEMY_ENGINE_OPTIONS`
  (`pool_pre_ping`, `pool_recycle`, `connect_args={"connect_timeout": ...}`). Обработчика ошибок БД нет.

## Что сделать (общий PR с #411)
1. `SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True, "pool_recycle": 300, "connect_args": {"connect_timeout": 5}}`.
   Тогда запрос падает за 5 секунд, а не за 130, и мёртвые соединения из пула отбрасываются.
2. `@app.errorhandler(OperationalError)` возвращает 503 с понятной страницей или JSON (ср. #414).
3. Возможно, закрыть #411 и #412 одним PR и попросить мейнтейнера закрыть дубликат.

---

## Оценка сложности фикса (проверено 2026-10-23, общий PR с #411)

**Вердикт: 🟢 ЛЕГКО.** 1–2 часа вместе с тестом. Эффект проверен экспериментом.

**Доказательства:**
- В логе запрос висел **130 071 мс**. Это стандартный предел TCP-подключения в Linux (`tcp_syn_retries=6` ≈ 127 с): у psycopg2 без
  `connect_timeout` подключение к недоступному хосту ждёт ровно столько.
- `experiments/exp_411.py`: подключение к недоступному адресу с `connect_args={"connect_timeout": 3}` падает **через 3.0 с**.

**Что менять:** `front/src/app.py`, после `:255`:
```python
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_pre_ping": True,
    "pool_recycle": 300,
}
```
и `connect_timeout=5` в URI внутри `get_database_uri` (`app.py:204-249`), см. ниже, почему не через `connect_args`.
**Осторожно с тестами:** `SQLALCHEMY_DATABASE_URI` можно переопределить через env и направить на SQLite, а `sqlite3.connect()` не знает
аргумента `connect_timeout` и упадёт с `TypeError`. Поэтому `connect_timeout` лучше задавать в query-строке URI внутри
`get_database_uri` (`...&connect_timeout=5` для prod и `?connect_timeout=5` для dev): libpq и psycopg2 его понимают, а тестовые URI это
не затрагивает. В `SQLALCHEMY_ENGINE_OPTIONS` тогда остаются только `pool_pre_ping` и `pool_recycle`, они работают с любой БД.

**Дополнительно (по желанию, отдельным коммитом):** `@app.errorhandler(sqlalchemy.exc.OperationalError)` возвращает 503 с понятным
текстом (HTML для страниц, JSON для API). Это пересекается с #414 (заглушка при обновлении).

**Тесты и окружение:** Linux не нужен. Unit-тест: `get_database_uri("prod")` содержит `connect_timeout`, а в `app.config` есть
`pool_pre_ping` (по образцу `front/tests/test_config_db.py`, он уже мокает env для prod).

**Риски:** низкие. `pool_pre_ping` добавляет один лёгкий `SELECT 1` на выдачу соединения из пула. На нагрузке miminet это незаметно.
Prod ходит через pgbouncer (порт 6432), `pool_pre_ping` с ним совместим.

---

## Статус: исправлено локально (2026-10-23)
Ветка `fix/412-db-connection-resilience-front` в `..\miminet`, черновик PR: [`drafts/pr-411-412.md`](drafts/pr-411-412.md). connect_timeout=5 в URI.
