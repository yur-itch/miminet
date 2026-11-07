# #290 Добавить метрику к добавлению маршрута

**Статус:** 🟢 свободна · **Issue:** https://github.com/mimi-net/miminet/issues/290 · 2025-08-31
**Сложность:** низкая или средняя · **Linux-бэкенд:** нужен для e2e-проверки, но код в основном простой

## Что сейчас в коде
- Front: [`miminet_host.py:283`](https://github.com/mimi-net/miminet/blob/24c36f3/front/src/miminet_host.py#L283),
  `add_route_job = host.create_job(ADD_ROUTE_JOB_ID, "ip route add [0]/[1] via [2]")` с тремя параметрами (ip, mask, gw).
- Back: [`jobs.py:414-423`](https://github.com/mimi-net/miminet/blob/24c36f3/back/src/jobs.py#L414),
  `ip route add {ip}/{mask} via {router}`, валидатор `ip_route_add_checker`
  ([`:133`](https://github.com/mimi-net/miminet/blob/24c36f3/back/src/jobs.py#L133)). Метрики нет.
- Недавно в этой форме делали фильтр IP/mask (PR #375, закрыл #326 и #327), так что код свежий и с тестами
  (`front/tests/test_fields_filter.py`).

## Что сделать
1. Front: необязательное поле «Метрика» у хоста, роутера и сервера (проверить, где ещё есть add route).
   Подпись job: `ip route add [0]/[1] via [2] metric [3]`.
2. Back: необязательный `arg_4` (целое), валидация, `... metric N`. Старые сети без `arg_4` должны работать как раньше.
3. Тест: два маршрута в одну сеть с разными метриками, проверить, что трафик идёт по меньшей. Плюс unit-тест валидатора.

## Почему хорошая задача
Небольшая, затрагивает весь стек (форма, job, backend) и при этом прямо про маршрутизацию, то есть про тему курса.
