# #444 Реализовать SLAAC (RFC 4862, 4941, 8981)

**Статус:** 🟢 свободна, конец цепочки IPv6 · **Issue:** https://github.com/mimi-net/miminet/issues/444 · 2026-05-19
**Сложность:** средняя (после #443) · **Linux-бэкенд:** обязателен

## Суть
Хосты получают глобальный адрес по RA. Сюда же входят privacy-адреса (RFC 4941/8981). Со стороны Linux это
`accept_ra=1`, `autoconf=1`, `use_tempaddr=2` и radvd на роутере с префиксом.

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
1. После #443: в UI роутера задавать IPv6-префикс для RA.
2. На хосте режим «SLAAC» рядом с DHCP-клиентом (`DHCP_CLIENT_JOB_ID`).
3. Показывать полученные адреса после эмуляции (вывод `ip -6 addr`).
