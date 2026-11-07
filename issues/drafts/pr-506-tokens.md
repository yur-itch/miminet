<!-- branch: fix/506-stop-printing-jwt-tokens-front · title: fix(front): stop printing JWT tokens on VK login (#506) -->
Refs #506

## Проблема
`vk_callback` печатал в stdout только что выданные access- и refresh-токены пользователя. При каждом входе через VK действующие токены сессии попадали в логи контейнера.

## Решение
Убран `print`: токены и так ставятся в cookies через `issue_jwt_cookies`.

Отдельный маленький PR, чтобы его можно было влить сразу. Остальная замена `print` на логирование лежит в соседнем PR (`refactor/506-print-to-logging`), и обе ветки сливаются без конфликтов в любом порядке.
