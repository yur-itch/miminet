# Диффы локальных фиксов

Каждый файл — один коммит из своей ветки (`git format-patch` от `main` (03–09 перебазированы на `0b63077` 2026-10-26)): сверху сообщение коммита, затем
список изменённых файлов, затем сам дифф (по 5 строк контекста). Порядок совпадает с предложенным порядком публикации.

| Файл | Ветка | Объём | Что читать в первую очередь |
|---|---|---|---|
| [01-524](01-524-preview-white-background.patch) ✅ слит (#544) | `fix/524-preview-white-background-front` | +2 −1 | одна строка в `netfront_f.js` |
| [02-404](02-404-declare-port-variable.patch) ✅ слит (#545) | `fix/404-declare-port-variable-front` | +2 −2 | `port` → `let port` ×2 |
| [03-506](03-506-stop-printing-jwt-tokens.patch) | `fix/506-stop-printing-jwt-tokens-front` | −2 | удалён `print` токенов |
| [04-542](04-542-keep-admin-author.patch) | `fix/542-keep-admin-author-front` | +85 −2 | `miminet_admin.py` (~20 строк), остальное тест |
| [05-543](05-543-hide-heavy-section-fields.patch) | `fix/543-hide-heavy-section-fields-front` | +29 | 2 строки в `miminet_admin.py`, остальное тест |
| [06-411-412](06-411-412-db-connection-resilience.patch) | `fix/412-db-connection-resilience-front` | +20 −2 | `app.py`, затем дополнения в `test_config_db.py` |
| [07-531](07-531-russian-document-lang.patch) | `fix/531-set-russian-document-lang-front` | +3 −3 | `lang="ru"` в трёх шаблонах |
| [08-539](08-539-yandex-avatar-and-example-network.patch) | `fix/539-yandex-avatar-and-example-network-front` | +200 −24 | `miminet_auth.py` (вынесены хелперы из VK), затем тест |
| [09-506](09-506-print-to-logging.patch) | `refactor/506-print-to-logging` | +35 −24 | 23 замены `print` → `logger` |

В 04, 05 и 08 есть ещё правка в `.github/workflows/front_coverage.yml`: туда добавлено имя нового теста, иначе CI его не
запустит. В 06 новых файлов тестов нет: проверки дописаны в уже существующий `test_config_db.py`.

Файлы сгенерированы из веток; если ветки поменяются, пересоздать так (из папки `miminet`):
```
git format-patch --stdout --stat -U5 main..<ветка> > ../issues/diffs/<имя>.patch
```
Применять их не нужно: ветки уже есть в репозитории, файлы только для чтения.
