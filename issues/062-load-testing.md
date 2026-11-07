# #62 Нагрузочное тестирование: сколько ресурсов нужно на одного студента

**Статус:** 🟡 свободна, но есть **заброшенная ветка** · **Issue:** https://github.com/mimi-net/miminet/issues/62 · 2024-02-08 · описания нет
**Сложность:** средняя · **Linux-бэкенд:** обязателен

## Существующая работа
- Ветка [`miminet-benchmark`](https://github.com/mimi-net/miminet/tree/miminet-benchmark), последний коммит 2025-11-26,
  **8 коммитов впереди и 112 позади main**. Файлы: `back/benchmark/{Dockerfile,README.md,run_benchmark_in_docker.sh,run_quick_benchmark.sh}`,
  `back/src/benchmark_emulation.py`, `back/src/benchmarking.py` и правки `emulator.py`. PR не открывался.
- С тех пор бэкенд сильно менялся: Python 3.12, ipmininet 1.3, readiness gate, изменения в teardown (#452, #453, #518).

## Что сделать
1. Написать автору ветки или мейнтейнеру: можно ли подхватить работу.
2. Перенести бенчмарк на текущий main, измерить CPU, RAM и время на одну эмуляцию для типовых сетей
   (из `back/tests/network_examples_json`), посчитать нагрузку на N одновременных студентов (через очередь RabbitMQ и воркеры).
3. Результат оформить как `docs/BENCHMARK.md` и скрипт.
