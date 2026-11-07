# #416 Full-cone NAT на маршрутизаторе

**Статус:** 🟢 свободна · **Issue:** https://github.com/mimi-net/miminet/issues/416 · 2026-04-07
**Сложность:** средняя · **Linux-бэкенд:** обязателен

## Что сейчас в коде
- Уже есть NAT через MASQUERADE ([`jobs.py:379`](https://github.com/mimi-net/miminet/blob/24c36f3/back/src/jobs.py#L379), `NAT_JOB_ID = 101`) и проброс портов TCP/UDP через DNAT
  (`PORT_FORWARDING_*_JOB_ID`, [`jobs.py:394`](https://github.com/mimi-net/miminet/blob/24c36f3/back/src/jobs.py#L394)).
- Linux MASQUERADE ведёт себя как *port-restricted/symmetric* NAT. **Full-cone в штатном netfilter нет**: нужен сторонний модуль
  ядра (netfilter-full-cone-nat), который в контейнер Mininet не поставить без пересборки ядра.

## Как можно сделать
1. **Эмуляция full-cone через пару правил.** SNAT на фиксированный внешний порт плюс DNAT этого порта обратно на внутренний
   адрес и порт. Эффект тот же: любой внешний хост может слать на сопоставленный порт. Это работает в рамках одного или нескольких
   заданных маппингов, и для учебной демонстрации этого хватает.
2. Новый job на роутере «Full-cone NAT: внутренний ip:port ↔ внешний порт, протокол». Нужны front (`miminet_host.py`, форма),
   back (`jobs.py`, валидатор) и тест.
3. Можно сделать сценарий, который показывает разницу: при MASQUERADE пакет от «чужого» внешнего хоста не проходит, при full-cone проходит.

## Вопросы
- Уточнить у автора, нужна ли именно семантика full-cone или нужен учебный набор «типы NAT» (full-cone, restricted, port-restricted, symmetric).
