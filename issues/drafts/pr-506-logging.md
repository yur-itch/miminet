<!-- branch: refactor/506-print-to-logging · title: refactor: replace print with logging (#506) -->
Closes #506

## Что сделано
Все диагностические `print()` во `front/src` и `back/src` (23 вызова) заменены на модульные логгеры `logging.getLogger(__name__)` с уровнем по смыслу сообщения:
- `miminet_model.py`: прогресс `init_db`/`ensure_db_exists` (info/warning/error);
- `app.py`: allowed origins, выбор БД (info);
- `miminet_config.py`: нет `SECRET_KEY_FILE` (warning);
- `miminet_auth.py`: ошибка БД при регистрации через VK и ошибки тестового пользователя (error). Здесь же убрана печать JWT-токенов (то же изменение, что в `fix/506-stop-printing-jwt-tokens-front`);
- `tasks.py`: создание каталога pcap (по стилю файла, через `logging.info`);
- `back/src/network_topology.py`: неизвестный тип узла (warning).

`pcap_parser.py` оставлен как есть: там `print(..., file=file)` пишет файл, это не лог.

## Видимость сообщений
Логирование уже настроено через `logging.basicConfig(level=INFO)` в `miminet_auth`, который `app.py` импортирует раньше всего остального. Проверено, что сообщения `python3 app.py dev` видны как раньше, теперь с уровнем и модулем:
```
INFO:miminet_model:[DEV] Schema exists.
INFO:app:[DB] Using local PostgreSQL: ...
```

## Пересечения
- С PR #436 (Logging v2) не пересекается: он эти `print` не трогает.
- Правило ruff `T20` (запрет `print`) в этот PR не входит: оно относится скорее к #505.
