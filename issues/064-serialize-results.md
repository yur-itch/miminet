# #64 Сериализация результатов эмуляции (JSON или другой машиночитаемый формат)

**Статус:** ⚪ свободна, но, скорее всего, **уже сделано** · **Issue:** https://github.com/mimi-net/miminet/issues/64 · 2024-02-08 · описания нет

## Что сейчас в коде
- Бэкенд возвращает результат эмуляции как JSON:
  [`back/src/tasks.py:73`](https://github.com/mimi-net/miminet/blob/24c36f3/back/src/tasks.py#L73) и `:152`,
  `return json.dumps(animation), pcaps`.
- Фронт хранит его в `Simulate.packets` (Text, JSON)
  ([`miminet_model.py:83`](https://github.com/mimi-net/miminet/blob/24c36f3/front/src/miminet_model.py#L83)),
  pcap-файлы лежат в `static/pcaps/<guid>` и доступны для скачивания и просмотра в MimiShark.

## Что сделать
Предложить мейнтейнеру закрыть issue или уточнить его: например, нужен публичный API «скачать результат эмуляции в JSON»
(сейчас это внутренний формат анимации).
