# #65 Работа с iptables

**Статус:** ⚪ свободна, но, скорее всего, частично устарела · **Issue:** https://github.com/mimi-net/miminet/issues/65 · 2024-02-08 · описания нет
**Сложность:** неизвестна

## Что уже есть в коде (через iptables)
- NAT (MASQUERADE), `NAT_JOB_ID = 101`
- Проброс портов TCP и UDP (DNAT), job'ы 109 и 110
- Блокировка TCP/UDP-порта, `BLOCK_TCP_UDP_PORT_JOB_ID = 202`
- iptables используется и в хосте «Hacker»
  ([`jobs.py:491`](https://github.com/mimi-net/miminet/blob/24c36f3/back/src/jobs.py#L491)).

## Что можно предложить
Спросить в issue, что ещё нужно. Варианты:
- (а) общий «межсетевой экран» на роутере: правила FORWARD accept/drop по src, dst, proto и port, с таблицей правил в UI;
- (б) показ счётчиков правил (`iptables -L -v`) после эмуляции;
- (в) закрыть issue как выполненный.

Вариант (а) хорошо подходит для курса по сетям, но это средняя по объёму задача: форма, job, валидация, тесты.
