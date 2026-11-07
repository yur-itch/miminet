# #539 Регистрация через Яндекс: не подтягивается аватар и не создаётся тестовая сеть

**Статус:** 🟢 свободна · **Issue:** https://github.com/mimi-net/miminet/issues/539 · 2026-10-19 (описание пустое, только заголовок)
**Сложность:** низкая или средняя · **Linux-бэкенд:** не нужен. Для ручной проверки нужно OAuth-приложение Яндекса (`client_yandex.json`).

## Что сейчас в коде — баг подтверждён чтением кода
- В [`yandex_callback`](https://github.com/mimi-net/miminet/blob/24c36f3/front/src/miminet_auth.py#L662) новый пользователь создаётся только с `nick`, `yandex_id` и `email`.
  Нет ни `avatar_uri`, ни блока `if user_is_new: Network(...)`.
- В [`vk_callback`](https://github.com/mimi-net/miminet/blob/24c36f3/front/src/miminet_auth.py#L519) оба шага есть: скачивание аватара через `save_avatar_blob` и
  создание примера сети [`:630`](https://github.com/mimi-net/miminet/blob/24c36f3/front/src/miminet_auth.py#L630) (`make_example_net_switch_and_hub()`).

## Что сделать
1. Вынести в общую функцию «после создания нового пользователя»: аватар и пример сети. Вызывать её из VK и Яндекса
   (а также из регистрации по email, если там этого нет — надо проверить).
2. Аватар Яндекса: в ответе `login.yandex.ru/info` есть поля `default_avatar_id` и `is_avatar_empty`. URL имеет вид
   `https://avatars.yandex.net/get-yapic/<id>/islands-200`. Если аватара нет, ставить `empty.jpg`, как в VK.
3. Тест с замоканным `OAuth2Session`.

## Попутно
- В VK-потоке [`miminet_auth.py:628`](https://github.com/mimi-net/miminet/blob/24c36f3/front/src/miminet_auth.py#L628) access- и refresh-токены пишутся в stdout через `print`.
  Это утечка токенов в логи, её стоит убрать в рамках #506.

---

## Оценка сложности фикса (проверено 2026-10-23)

**Вердикт: 🟢/🟡 ЛЕГКО–СРЕДНЕ.** 2–4 часа. Код простой и копирует VK-поток. Сложность в том, что полностью проверить вручную можно
только с OAuth-приложением Яндекса.

**Что менять (`front/src/miminet_auth.py`):**
1. Вынести из `vk_callback` (`:519-641`) две функции: `download_avatar(url) -> avatar_uri` (с `requests` + `save_avatar_blob`,
   fallback `empty.jpg`) и `create_example_network(user)` (блок `if user_is_new:` на `:630-640`).
2. В `yandex_callback` (`:662`) для нового пользователя:
   - аватар: `if not id_info.get("is_avatar_empty") and id_info.get("default_avatar_id"):` →
     `https://avatars.yandex.net/get-yapic/{default_avatar_id}/islands-200`;
   - после `commit` вызвать `create_example_network(user)`.
   Формат URL и размеры взяты из официальной документации:
   [Яндекс ID: информация о пользователе](https://yandex.ru/dev/id/doc/ru/user-information).
3. **Важно:** `default_avatar_id` приходит, только если у приложения в кабинете Яндекс OAuth включено право «Портрет пользователя».
   Если у прод-приложения его нет, аватар не появится даже после фикса. Это нужно уточнить у мейнтейнера (вопрос в PR).

**Найденная попутно проблема (отдельный issue, не смешивать):**
`email=id_info.get("default_email", "")`, а `User.email` объявлен `unique=True` (`miminet_model.py:43`). Второй пользователь Яндекса без
email получит `""` и упадёт на `IntegrityError`. Пользователь, у которого уже есть VK-аккаунт с тем же email, тоже не сможет войти через
Яндекс. VK-поток в этом случае связывает аккаунты по email (`:567-572`), а Яндекс нет. Исправление: `or None` вместо `""` и такое же
связывание по email.

**Тесты и окружение:** Linux не нужен. Unit-тест с замоканными `OAuth2Session.fetch_token`/`get` и `requests.get` для аватара:
новый пользователь получает `avatar_uri != "empty.jpg"` и одну `Network` с `title="Свитч и хаб (пример сети)"`. Готовых тестов на
OAuth-потоки в репозитории нет, моки придётся писать с нуля, это основная часть времени.

**Риски:** низкие. Рефакторинг VK-потока стоит делать аккуратно, чтобы его не сломать (тест и для VK).

---

## Статус: исправлено локально (2026-10-23)
Ветка `fix/539-yandex-avatar-and-example-network-front` в `..\miminet`, черновик PR: [`drafts/pr-539.md`](drafts/pr-539.md). Сквозная проверка на локальной БД пройдена; про право «Портрет пользователя» нужно спросить мейнтейнера.
