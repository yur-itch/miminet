# #322 Добавить логирование

**Статус:** 🔴 занята по факту: два открытых PR · **Issue:** https://github.com/mimi-net/miminet/issues/322

## Существующая работа
- [PR #385 «Logging Miminet»](https://github.com/mimi-net/miminet/pull/385) (silvitreatment, 2025-12-22, +1033/−89),
  последний коммит 2026-01-15, конфликтует с main, ревью нет.
- [PR #436 «Logging Miminet v2»](https://github.com/mimi-net/miminet/pull/436) (IgorFilimonov, 2026-05-10, +1031/−111, 22 файла),
  ссылается на #385 как продолжение. Последний коммит 2026-05-14, конфликтует с main, ревью нет.
- Ветки `logging` и `feature/logging_sync`.

## Вывод
Большую задачу не брать. Узкая и свободная её часть — **#506** (заменить `print` на `logger` и убрать печать токенов).
Перед ней стоит посмотреть diff #436, чтобы не дублировать работу.
