# #441 Добавить link-local адреса (fe80::/10) на устройства

**Статус:** 🟢 свободна, но требует согласования · **Issue:** https://github.com/mimi-net/miminet/issues/441 · 2026-05-19 · автор Disinterpreter
**Сложность:** высокая · **Linux-бэкенд:** обязателен (Mininet и ipmininet; WSL не подходит)

## Суть
Хосты, серверы и роутеры при переходе в UP получают link-local адрес (EUI-64), пингуют друг друга, поддерживают нотацию
`fe80::1%iface`. Это первый шаг цепочки #441 → #442 ICMPv6 → #443 NDP → #444 SLAAC.

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
1. Написать в issue вопрос про стратегию: флаг IPv6 на уровне сети, фильтр захвата `not (icmp6 and ip6[40] == 143)` (MLDv2),
   потребление ресурсов.
2. Бэкенд: при включённом флаге не выключать IPv6. Ядро Linux само назначит link-local через EUI-64, то есть «реализовывать»
   адресацию почти не нужно, нужно её разрешить и показать.
3. Фронт: показывать link-local в конфигурации интерфейсов. Добавить ping6 (новый job или опция в существующем ping).
4. `pkt_parser.py`: парсинг IPv6 и ICMPv6 для анимации.
5. Тесты в `back/tests` по образцу существующих JSON-сетей.
