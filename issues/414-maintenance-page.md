# #414 Заглушка при обновлении сервера

**Статус:** 🟢 свободна · **Issue:** https://github.com/mimi-net/miminet/issues/414 · 2026-03-27
**Сложность:** низкая или средняя (это в основном DevOps) · **Linux-бэкенд:** не нужен, но нужно разобраться в деплое

## Что сейчас в репозитории
- [`front/default.conf.template`](https://github.com/mimi-net/miminet/blob/24c36f3/front/default.conf.template): nginx проксирует всё через `uwsgi_pass miminet:80`.
  `error_page` и maintenance-страницы нет.
- Деплой: `ansible/` и `front/docker-compose-prod.yml`. Прод-nginx, судя по тому, что `/images/preview` работает на проде,
  настроен частично вне репозитория (см. заметку в 524).

## Что сделать
1. Статическая `maintenance.html` в стиле сайта.
2. Вариант A: в nginx `error_page 502 503 504 /maintenance.html` (`location = /maintenance.html { internal; root ...; }`).
   Тогда во время перезапуска контейнера `miminet` пользователь видит заглушку.
3. Вариант B: флаг-файл `if (-f /etc/nginx/maintenance.on) { return 503; }` и включение и выключение флага в ansible-плейбуке деплоя.
4. Для AJAX (`/post_nodes_edges` и т. п.) отдавать JSON 503, а фронт показывает toast «Сервер обновляется».

## Вопросы
- Где реально стоит внешний nginx на проде? Без ответа мейнтейнера изменения могут не попасть на прод.
