# #442 Реализовать ICMPv6 (RFC 4443)

**Статус:** 🟢 свободна, зависит от #441 · **Issue:** https://github.com/mimi-net/miminet/issues/442 · 2026-05-19
**Сложность:** средняя (после #441) · **Linux-бэкенд:** обязателен

## Суть
В Linux ICMPv6 уже есть в ядре, «реализовывать» протокол не нужно. По факту задача такая: пропускать ICMPv6 в захват
и **разбирать и анимировать** его на фронте (Echo Request/Reply, Destination Unreachable, Time Exceeded для traceroute6).

## ⚠️ Главный блокер всей ветки IPv6 (#441–#444)
IPv6 в эмуляции **сейчас сознательно выключен**, и это результат недавней работы по стабильности:
- [`back/src/network.py:24`](https://github.com/mimi-net/miminet/blob/24c36f3/back/src/network.py#L24): `use_v6=False`. В [`:53`](https://github.com/mimi-net/miminet/blob/24c36f3/back/src/network.py#L53) и
  [`:309`](https://github.com/mimi-net/miminet/blob/24c36f3/back/src/network.py#L309) (`__disable_ipv6`) `disable_ipv6=1` ставится на всех интерфейсах, отключить это можно через
  `MIMINET_DISABLE_IPV6=0`.
- [`back/src/network_topology.py:234-242`](https://github.com/mimi-net/miminet/blob/24c36f3/back/src/network_topology.py#L234): захват трафика идёт с фильтром `not igmp and not ip6`.
  В комментарии сказано, что поток MLDv2 и DAD забивает буферы захвата и вытесняет ARP/ICMP (issue #450, PR #452/#453).
- `pkt_parser.py` пропускает IPv6 и IGMP.

Значит, прежде чем делать IPv6, надо **договориться с мейнтейнерами**: включать IPv6 только для сетей, где он настроен, и
фильтровать MLD-шум, но не весь `ip6`. Иначе вернутся проблемы, которые чинили в #452/#453.

## Что сделать
1. После #441: `pkt_parser.py` разбирает `dpkt.icmp6`, подписи пакетов в анимации, фильтры отображения.
2. Добавить jobs `ping6` и `traceroute6` (front `miminet_host.py` + back `jobs.py` + валидаторы).
3. Тесты: ping6 между двумя хостами по link-local.
