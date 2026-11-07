# #434 Добавить групповой (multicast) сервер и клиентов

**Статус:** 🟢 свободна · **Issue:** https://github.com/mimi-net/miminet/issues/434 · 2026-05-06 · метки: Mininet (Advanced), Linux admin (Advanced)
**Сложность:** высокая · **Linux-бэкенд:** обязателен

## Суть
Показать вступление в группу и выход из неё (IGMP join/leave) и прохождение группового трафика через маршрутизаторы.

## Что сейчас в коде
- Поддержки нет: в `back/src` нет `igmp`, `mcast`, `smcroute` и `pimd`.
- Более того, IGMP **вырезается** при захвате: [`network_topology.py:242`](https://github.com/mimi-net/miminet/blob/24c36f3/back/src/network_topology.py#L242),
  `extra_arguments="not igmp and not ip6"`. И при разборе: [`pkt_parser.py:290`](https://github.com/mimi-net/miminet/blob/24c36f3/back/src/pkt_parser.py#L290), `# Skip IGMP`.
  Убрать фильтр глобально нельзя, потому что вернётся шум (см. #450, #452).

## Что сделать
1. Сначала обсудить в issue, как включать IGMP в захват только для сетей с multicast-jobs (флаг в network JSON).
2. Jobs: «multicast-сервер» (например, `iperf -u -c 239.x.x.x -T ttl` или socat/python-скрипт) и «вступить в группу»
   (`socat UDP4-RECV:...,ip-add-membership=...` или smcroute на хосте).
3. Маршрутизация multicast на роутере: smcroute (статическая) или pimd (PIM-SM). Это самая сложная часть,
   надо проверить, что пакеты есть в образе back.
4. `pkt_parser.py`: разбор IGMPv2/v3 (dpkt.igmp) и анимация join/leave.

## Риски
- Большая задача, затрагивает Docker-образ, фронт и бэк. Для «первого контрибьюшна» не подходит.
