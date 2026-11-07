# #542 Админка: при создании теста не сохраняется автор, и список тестов падает

**Статус:** 🟢 свободна · **Issue:** https://github.com/mimi-net/miminet/issues/542 · 2026-10-21 (свежая, метка `quiz`)
**Сложность:** низкая · **Linux-бэкенд:** не нужен. Нужен пользователь с ролью админа в локальной БД.

## Суть (по traceback)
После `POST /admin/test/new/` у записи `Test` поле `created_by_id = NULL`. Потом
[`created_by_formatter`](https://github.com/mimi-net/miminet/blob/24c36f3/front/src/miminet_admin.py#L375) кидает `Exception("Error occurred while retrieving user nickname")`,
и **вся страница** `/admin/test/` отдаёт 500.

## Гипотеза (по коду)
- Базовый [`on_model_change`](https://github.com/mimi-net/miminet/blob/24c36f3/front/src/miminet_admin.py#L355) ставит `model.created_by_id = current_user.id`.
- Но у [`TestView`](https://github.com/mimi-net/miminet/blob/24c36f3/front/src/miminet_admin.py#L382) **нет** своего `form_excluded_columns`, он наследует только
  `["is_deleted", "updated_on", "created_on"]` ([`:341`](https://github.com/mimi-net/miminet/blob/24c36f3/front/src/miminet_admin.py#L341)). Поэтому в форме остаётся поле
  отношения `created_by_user` (пустое). При сохранении flask-admin записывает `created_by_user = None`, и при flush SQLAlchemy
  синхронизирует FK из отношения, то есть затирает `created_by_id`.
- У [`SectionView`](https://github.com/mimi-net/miminet/blob/24c36f3/front/src/miminet_admin.py#L445) `created_by_id` и `created_by_user` из формы исключены. Видимо, поэтому
  разделы создаются нормально, а тесты нет.

## Что сделать
1. В `TestView` добавить `form_excluded_columns = MiminetAdminModelView.form_excluded_columns + ["created_by_id", "created_by_user"]`
   (так уже сделано в другом view, [`:529`](https://github.com/mimi-net/miminet/blob/24c36f3/front/src/miminet_admin.py#L529)).
2. `created_by_formatter` (и `get_test_name`) не должны ронять всю страницу: возвращать `"—"` и писать warning в лог.
   Это нужно, чтобы уже испорченные записи на проде не ломали список.
3. Возможно, нужен SQL-скрипт или миграция, чтобы проставить автора существующим тестам с NULL. Это вопрос к мейнтейнеру.
4. Тест: создать Test через админку под админом и проверить, что `created_by_id == admin.id`.

---

## Оценка сложности фикса (проверено 2026-10-23)

**Вердикт: 🟢 ЛЕГКО.** 1–2 часа вместе с тестом. Гипотеза **подтверждена экспериментом**.

**Эксперимент** (`experiments/exp_542.py`: Flask-Admin 2.0.1, SQLAlchemy 2.0.43, PostgreSQL 16, модель и `on_model_change`
такие же, как в проекте; POST формы создания с пустым полем «Created By User»):
```
[main]  author field rendered in form: True   created_by_id after create: None
[fixed] author field rendered in form: False  created_by_id after create: 1
```
Значит, причина в том, что пустое поле отношения `created_by_user` попадает в `populate_obj`, и при flush SQLAlchemy затирает FK,
выставленный в `on_model_change`.

**Что менять (`front/src/miminet_admin.py`):**
1. `TestView` (`:382`): `form_excluded_columns = MiminetAdminModelView.form_excluded_columns + ["created_by_id", "created_by_user"]`.
   Это 4 строки, тот же паттерн уже используется на `:529`.
2. `created_by_formatter` (`:375`): вместо `raise Exception` возвращать `"—"` и писать `logger.warning`. Без этого уже
   испорченные записи на проде продолжат ронять `/admin/test/` с ошибкой 500 даже после фикса. То же для `get_test_name` (`:406`).
3. Опционально, по согласованию: SQL для починки существующих записей, например
   `UPDATE test SET created_by_id = <id> WHERE created_by_id IS NULL`. Кому их назначить, решает мейнтейнер.

**Другие view (проверено 2026-10-23):**
| View | `created_by_user` исключён из формы? | Итог |
|---|---|---|
| `TestView` (`:382`) | ❌ нет | баг из issue |
| `AnswerView` (`:624`) | ❌ нет (своего `form_excluded_columns` нет, только `form_extra_fields`) | **тот же баг**: «Варианты», созданные через админку, теряют автора, а список падает на `created_by_formatter`. Механизм тот же, но отдельно не воспроизводился |
| `SectionView` (`:445`) | ✅ да | ок |
| `QuestionView` (`:529`) | ✅ да | ок |
| `SessionQuestionView` (`:699`) | — `can_create = False` | ок |

То есть в PR стоит чинить и `TestView`, и `AnswerView`: одинаковая правка, и в описании PR это нужно указать.

**Тесты и окружение:** Linux не нужен. Тест на Flask test client: под админом сделать POST `/admin/test/new/`, затем
`Test.created_by_id == admin.id`. Плюс тест форматтера: запись с NULL не роняет страницу списка. В `app.py` есть переопределение
`SQLALCHEMY_DATABASE_URI` через env, «специально для тестов», так что тесту хватит временного Postgres в Docker.

**Риски:** низкие. Изменения касаются только админки.

---

## Статус: исправлено локально (2026-10-23)
Ветка `fix/542-keep-admin-author-front` в `..\miminet`, черновик PR: [`drafts/pr-542.md`](drafts/pr-542.md). Исправлены TestView и AnswerView; до фикса 500 на обоих списках, после 200; тест падает без фикса.
