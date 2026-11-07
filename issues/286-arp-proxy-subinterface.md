# #286 ARP Proxy на сабинтерфейсах

**Статус:** 🟢 свободна. Ветка `NikitaPisarev/subinterface-test` от 2024 года — это только тест сабинтерфейса, к задаче не относится.
**Issue:** https://github.com/mimi-net/miminet/issues/286 · 2025-08-31 · **Сложность:** средняя · **Linux-бэкенд:** обязателен

## Что сейчас в коде
- Back: [`jobs.py:560-567`](https://github.com/mimi-net/miminet/blob/24c36f3/back/src/jobs.py#L560),
  `sysctl -w net.ipv4.conf.{iface}.proxy_arp=1` после `valid_iface`.
- Front: интерфейс выбирается через `FillDeviceSelectIntf`
  ([`config_devices.js:1541`](https://github.com/mimi-net/miminet/blob/24c36f3/front/src/static/config_devices.js#L1541)),
  который перебирает только `device_node.interface`, то есть физические линки. Сабинтерфейсы VLAN создаются отдельным job'ом
  (`SUBINTERFACE_VLAN_JOB_ID = 104`, [`jobs.py:508`](https://github.com/mimi-net/miminet/blob/24c36f3/back/src/jobs.py#L508))
  и в списке не появляются.

## Подводные камни
- Имя сабинтерфейса вида `eth0.10` содержит точку, а `sysctl -w net.ipv4.conf.eth0.10.proxy_arp=1` воспримет точку как
  разделитель. Надо писать `net.ipv4.conf.eth0/10.proxy_arp` или в `/proc/sys/net/ipv4/conf/eth0.10/proxy_arp`.
- Порядок job'ов: proxy_arp должен выполняться **после** создания сабинтерфейса.
- `valid_iface` может не пропускать имена с точкой, это надо проверить.

## Что сделать
1. Во фронте добавить в список ARP proxy сабинтерфейсы из job'ов 104 этого роутера.
2. В бэке поддержать имена с точкой и упорядочить job'ы.
3. Тест по образцу открытого PR #216 «Add test for ARP Proxy» (висит с 2025-03, его тоже можно довести).
