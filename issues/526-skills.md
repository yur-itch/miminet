# #526 Добавить скилы

**Статус:** 🟢 свободна · **Issue:** https://github.com/mimi-net/miminet/issues/526 · 2026-10-02
**Сложность:** низкая (это документация) · **Linux-бэкенд:** не нужен

## Суть
Текст issue: «Python-flask, JS, HTML bootstrap, PlayWright. Если кажется, что что-то ещё нужно, добавляем.»
Судя по контексту (недавно мейнтейнер добавил [`AGENTS.md`](https://github.com/mimi-net/miminet/blob/24c36f3/AGENTS.md), `docs/ARCHITECTURE` и `docs/REQUIREMENTS`),
речь о **skills для AI-агентов**: наборах инструкций (например, `.claude/skills/<name>/SKILL.md` или аналог), а не о метках
на GitHub. Но это моя интерпретация, её стоит уточнить.

## Что сейчас в репозитории
- Папок `.claude/`, `.agents/` и `skills/` нет. В `AGENTS.md` слово «skill» не встречается.

## Что сделать
1. Уточнить в issue формат: куда класть и под какого агента (Claude Code, Codex, Cursor).
2. Написать по одному скилу на тему: как писать Flask-роуты и тесты в этом проекте, конвенции JS (jQuery, Cytoscape),
   Bootstrap-шаблоны, как писать Playwright-тесты (`front/tests/playwright`).
3. Ссылаться на существующие `docs/ARCHITECTURE/CONVENTIONS.md` и `docs/FUNCTIONAL_TESTS.md`, а не дублировать их.
