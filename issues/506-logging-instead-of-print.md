# #506 Внедрить логирование и избавиться от print

**Статус:** 🟡 свободна, но пересекается с зависшими PR по логированию
**Issue:** https://github.com/mimi-net/miminet/issues/506 · 2026-09-22 · **Сложность:** низкая · **Linux-бэкенд:** не нужен для фронта

## Что сейчас в коде
- `print(` в Python: 23 вызова во `front/src` и 1 в `back/src`. Больше всего в `miminet_model.py` (12), `miminet_auth.py` (5)
  и `app.py` (3). В части модулей уже есть `logger = logging.getLogger(...)`.
- ⚠️ [`miminet_auth.py:628`](https://github.com/mimi-net/miminet/blob/24c36f3/front/src/miminet_auth.py#L628) печатает access- и refresh-токены пользователя.
  Это нужно убрать в первую очередь.

## Связанные PR (открыты, конфликтуют с main)
- #385 «Logging Miminet» (последний коммит 2026-01-15) и #436 «Logging Miminet v2» (2026-05-14), закрывают #322.
  Это более крупная работа: структурированное логирование и сбор логов. #506 — узкая задача «заменить print на logger».

## Что сделать
1. Посмотреть, что в #436 уже сделано с `print`, чтобы не конфликтовать. Сделать маленький PR: `print` → `logger.info/error`
   в `front/src` и `back/src`, токены не логировать.
2. Добавить ruff-правило `T20` (flake8-print) в `pyproject.toml`, чтобы `print` не возвращались. Это пересекается с #505
   (линтеры, назначен на i1ya).

---

## Оценка сложности фикса (проверено 2026-10-23)

**Вердикт: 🟢 ЛЕГКО.** 1–3 часа. Работа механическая, но нужно не промахнуться в двух местах.

**Точный список (`print(` в Python, main @ 24c36f3):**
| Файл | Шт. | Что там |
|---|---|---|
| `front/src/miminet_model.py` | 12 | `:138-266`, сообщения `init_db`/`ensure_db_exists` (работают в `python3 app.py` до uwsgi) |
| `front/src/miminet_auth.py` | 5 | `:614-615` ошибка БД при регистрации VK, **`:628` печать access- и refresh-токенов** ⚠️, `:747,:760` тестовый пользователь |
| `front/src/app.py` | 3 | `:163` allowed origins, `:223,:244` выбор БД |
| `front/src/miminet_config.py` | 1 | `:14` нет `SECRET_KEY_FILE` |
| `front/src/tasks.py` | 1 | `:44` |
| `back/src/network_topology.py` | 1 | `:68` неизвестный тип узла |
| `front/src/pcap_parser.py:121` | — | **не трогать:** это `print(..., file=file)`, запись в файл, а не лог |

**Как делать:**
1. В каждом модуле `logger = logging.getLogger(__name__)`. `print(...)` заменить на `logger.info`, а в `except` на `logger.error` или
   `logger.exception`.
2. Строку `:628` с токенами **удалить**, а не переводить в logger: токены не должны попадать в логи ни на каком уровне.
3. Конфигурация логирования уже есть: `logging.basicConfig(level=logging.INFO)` в `miminet_auth.py:169`, выполняется при импорте
   из `app.py`, поэтому `logger.info` будет виден и в `python3 app.py`, и под uwsgi. Новую конфигурацию в этом PR не вводить:
   это зона PR #436 (`logging_config.py`).
4. Чтобы `print` не возвращались: добавить в `pyproject.toml` `[tool.ruff.lint] select += ["T20"]` с исключением для
   `pcap_parser.py`. Это пересекается с #505 (назначен на i1ya), поэтому лучше спросить, а не делать молча.

**Пересечение с PR #436:** проверено, #436 **не** убирает эти `print` (наоборот, добавляет `print("log requested")`). Конфликты
возможны только в `front/src/tasks.py` и `back/src/network_topology.py`, обе правки однострочные.

**Тесты и окружение:** Linux не нужен. Достаточно `ruff check` и существующих тестов. Отдельный тест имеет смысл только на то, что
`vk_callback` не логирует токены (через `caplog`).

**Совет:** удаление печати токенов можно сделать **самым первым, отдельным PR** («security: stop printing JWT tokens to stdout»).
Это одна строка с очевидной ценностью.

---

## Статус: исправлено локально (2026-10-23)
Ветка `refactor/506-print-to-logging + fix/506-stop-printing-jwt-tokens-front` в `..\miminet`, черновик PR: [`drafts/pr-506-logging.md`](drafts/pr-506-logging.md). Две ветки: печать токенов отдельно; см. также drafts/pr-506-tokens.md.
