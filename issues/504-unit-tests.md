# #504 Добавить unit-тесты и правила их написания

**Статус:** 🟢 свободна · **Issue:** https://github.com/mimi-net/miminet/issues/504 · 2026-09-22 (описание пустое)
**Сложность:** средняя (зависит от объёма) · **Linux-бэкенд:** для тестов фронта не нужен

## Что сейчас в репозитории
- `front/tests`: около 30 файлов, большинство — e2e (Selenium, Playwright), плюс несколько «браузер-фри» тестов
  (`test_quiz_progress.py`, `test_job_validators.py`, `test_fields_filter.py`, `test_jwt_cookies.py`).
- `back/tests`: `test_pkt_parser.py`, `test_jobs.py`, `test_vlan.py` и др.
- В [`docs/DEVELOPMENT.md`](https://github.com/mimi-net/miminet/blob/24c36f3/docs/DEVELOPMENT.md) есть раздел «Frontend unit test (no containers, offline)», есть
  `BACKEND_TESTS.md` и `FUNCTIONAL_TESTS.md`. Отдельного документа «правила написания unit-тестов» нет.

## Что сделать
1. Уточнить, что именно хочет мейнтейнер: только документ или документ плюс тесты для конкретных модулей.
2. Хорошие кандидаты для покрытия: `quiz/util/dto.py` (там же баг #535), `configurators.py`, валидаторы job'ов
   в `back/src/jobs.py` (`*_checker`), `miminet_admin` (баг #542).
3. Предложить `docs/UNIT_TESTS.md`: структура, именование, моки БД (pytest-mock уже используется), как запускать без Docker.
