# BoardGame Platform

## Опис проєкту
**BoardGame Hub** — це вебплатформа для любителів настільних ігор, яка об'єднує каталог ігор, відгуки та можливість оренди ігор додому або бронювання ігрових сесій у локальних хабах та клубах настільних ігор.

Застосунок дозволяє користувачам шукати ігри за різними параметрами (кількість гравців, тривалість, складність), читати відгуки, переглядати сторінки жанрів і хабів. Авторизовані користувачі можуть залишати відгуки, додавати ігри до кошика оренди та створювати замовлення на бронювання.

## Як запустити проєкт

### 1. Клонування репозиторію

```bash
git clone <repo-url>
cd <папка-проєкту>
```

### 2. Віртуальне середовище

```bash
python3 -m venv .venv
source .venv/bin/activate        # macOS / Linux
# .venv\Scripts\activate         # Windows
```

### 3. Залежності

```bash
pip install -r requirements.txt
```

Для перевірки форматування коду:

```bash
pip install -r requirements-dev.txt
```

### 4. Міграції та тестові дані

```bash
python3 manage.py migrate
```

Міграція `0003_add_data` автоматично додає:

- 2 хаби
- 3 жанри
- 5 ігор

Міграція `users.0002_create_profiles` створює `Profile` для наявних користувачів.
Для нових користувачів профіль створюється автоматично під час реєстрації.

### 5. Запуск сервера

```bash
python3 manage.py runserver
```

- API: http://127.0.0.1:8000/api/v1/
- Адмінка: http://127.0.0.1:8000/admin/

Для доступу до адмінки можна створити суперкористувача:

```bash
python3 manage.py createsuperuser
```

Суперюзер автоматично отримує роль `admin`. Перевірити або змінити роль:
`/admin/` → **Users → Profiles**.

### 6. Перевірка

```bash
python3 check_submission.py
```

### 7. Postman

Імпортуйте колекцію `postman/boardgame_api.postman_collection.json` (Postman Collection v2.1). Базова адреса сервера винесена у змінну `{{base_url}}` — `http://127.0.0.1:8000/api/v1`.

Колекція містить 6 папок:

| Папка | Призначення |
|---|---|
| `00. Auth` | реєстрація, логін, refresh, профіль, перевірка `401` |
| `01. Games — читання` | публічні `GET`, фільтри, сортування, помилки `400`/`404` |
| `02. Games — життєвий цикл` | створення, оновлення, видалення гри; `403` для `user` |
| `03. Genres` | CRUD жанрів і пов'язані ігри |
| `04. Hubs` | CRUD хабів і пов'язані ігри |
| `05. CORS` | CORS-заголовки для `GET` і preflight |

Перед першим запуском заповніть `admin_username` і `admin_password` — дані суперюзера вашої локальної бази (у нього `role="admin"`).

## Тестування

Проєкт покритий автоматизованими тестами на **pytest** + **pytest-django**. Тестуються ендпоінти ресурсу **Games** (`GET`, `POST`, `PUT`, `DELETE`), права доступу (адміністратор / звичайний користувач / анонім) та валідація вхідних даних.

### Структура тестів

```text
catalog/tests/
├── conftest.py               # спільні фікстури
├── test_games_list.py        # GET list/detail, фільтри, сортування
├── test_games_create.py      # POST і негативні сценарії
├── test_games_update.py      # PUT, PATCH (405) і негативні сценарії
└── test_games_delete.py      # DELETE і негативні сценарії
```

### Встановлення залежностей

```bash
pip install -r requirements-dev.txt
```

`requirements-dev.txt` містить `-r requirements.txt`, тому встановляться і runtime-, і тестові залежності (`pytest`, `pytest-django`, `pytest-cov`).

### Запуск тестів

Усі тести:

```bash
pytest
```

Лише тести каталогу:

```bash
pytest catalog/tests -v
```

Окремий файл:

```bash
pytest catalog/tests/test_games_create.py -v
```

Окремий тест:

```bash
pytest catalog/tests/test_games_create.py::test_admin_can_create_game -v
```

Тестові файли названі за маскою `test*.py`, тестові функції — `test_*`.

### Вимірювання покриття

Текстовий звіт у терміналі:

```bash
pytest --cov=catalog --cov=users --cov-report=term-missing
```

Поточний результат: **32 тести, 86% покриття**.

```text
Name                                       Stmts   Miss  Cover   Missing
------------------------------------------------------------------------
catalog/admin.py                              16      0   100%
catalog/apps.py                                3      0   100%
catalog/exceptions.py                          4      0   100%
catalog/migrations/0001_initial.py             6      0   100%
catalog/migrations/0002_game_rating.py         4      0   100%
catalog/migrations/0003_add_data.py           30      6    80%   142-148
catalog/models.py                             30      3    90%   11, 19, 40
catalog/permissions.py                        10      0   100%
catalog/serializers.py                        43      0   100%
catalog/urls.py                                3      0   100%
catalog/views.py                             135     44    67%   23-24, 27-30, 37-38, 41-45, 48-55, 62-64, 84-85, 88-91, 98-99, 102-106, 109-116, 123-125
users/admin.py                                14      2    86%   15, 19
users/apps.py                                  5      0   100%
users/migrations/0001_initial.py               7      0   100%
users/migrations/0002_create_profiles.py      14      4    71%   10-11, 15-16
users/models.py                               10      1    90%   18
users/serializers.py                          41     20    51%   15-16, 73-75, 78-80, 83-93, 96-100, 103-104
users/signals.py                               8      0   100%
users/urls.py                                  4      0   100%
users/views.py                                16      5    69%   13-16, 23
------------------------------------------------------------------------
TOTAL                                        593     85    86%
```

`catalog/views.py` має 67%, оскільки тестами покритий ресурс Games; ендпоінти Hub і Genre залишаються без тестів.

## Документація API

API документовано за допомогою OpenAPI 3. Схема генерується автоматично з DRF-в'ю
та серіалайзерів бібліотекою `drf-spectacular`.

### Доступ до документації

Після запуску сервера (`python3 manage.py runserver`):

| Що | Посилання |
|---|---|
| Swagger UI | [http://127.0.0.1:8000/api/docs/](http://127.0.0.1:8000/api/docs/) |
| OpenAPI-схема (YAML) | [http://127.0.0.1:8000/api/schema/](http://127.0.0.1:8000/api/schema/) |

### Генерація схеми у файл

```bash
python3 manage.py spectacular --file openapi-schema.yml --validate
```

Команда створює файл `openapi-schema.yml` у корені проєкту, а `--validate`
перевіряє схему на відповідність специфікації OpenAPI 3.

### Задокументований ресурс

Повністю задокументовано ресурс **Games**:

| Метод | Endpoint | Опис | Автентифікація |
|---|---|---|---|
| GET | `/api/v1/games` | список ігор із пошуком, фільтрами та сортуванням | не потрібна |
| POST | `/api/v1/games` | створення гри | JWT, лише admin |
| GET | `/api/v1/games/{id}` | деталі гри | не потрібна |
| PUT | `/api/v1/games/{id}` | повне оновлення гри | JWT, лише admin |
| DELETE | `/api/v1/games/{id}` | видалення гри | JWT, лише admin |

Query-параметри `GET /api/v1/games`: `search`, `hub_id`, `genre_id`,
`min_players`, `complexity` (`Easy`, `Medium`, `Hard`), `sort`
(`price_asc`, `price_desc`, `rating_desc`, `rating_asc`, `popularity`).

Для захищених методів використовується JWT (схема `jwtAuth`, `Authorization: Bearer <access>`).
Коди відповідей: `200`, `201`, `204`, а також `400`, `401`, `403`, `404`.

## Логування
 Логи допомагають відстежити зміни даних, побачити помилки клієнта й знайти причину падіння.

### Налаштування

Конфігурація — `LOGGING` у `config/settings.py`. Одночасно працюють два обробники:

| Handler | Куди пише | Навіщо |
|---|---|---|
| `console` | термінал (`runserver`) | побачити подію одразу |
| `file` | `logs/app.log` | історія після закриття терміналу |

Файл ротується (`RotatingFileHandler`): до **5 МБ**, зберігається **3** резервні копії
(`app.log.1`–`app.log.3`). Каталог `logs/` створюється автоматично під час старту
(`LOG_DIR.mkdir`), а сам файл у `.gitignore`, тому в репозиторій не потрапляє.

Формат рядка:

```text
2026-11-16 20:10:07 INFO    users.views user registered id=24 username='alina'
```

`{дата} {рівень:<7} {логер} {повідомлення}` — вирівняний рівень дозволяє читати лог очима
й фільтрувати його через `grep`.

### Рівні

| Рівень | Коли використовується | Приклад |
|---|---|---|
| `DEBUG` | перегляд каталогу (часта подія, у проді вимикається) | `games listed search='catan' hub_id=None genre_id=2 min_players=3 complexity=None sort=price_asc count=4` |
| `INFO` | зміна стану: CRUD каталогу, реєстрація | `game created id=6 title='Catan' user_id=1` |
| `WARNING` | помилки клієнта (`4xx`) | `GET /api/v1/games/999999 status=404 user_id=None` |
| `ERROR` | необроблений виняток (`5xx`), з трейсбеком | `unhandled exception POST /api/v1/games user_id=1` |

### Що саме логується

| Місце | Рівень | Події |
|---|---|---|
| `catalog/views.py` | `DEBUG` | `games listed` — пошук, фільтри, сортування, кількість результатів |
| `catalog/views.py` | `INFO` | `game` / `hub` / `genre` `created`, `updated`, `deleted` з `id` і `user_id` |
| `users/views.py` | `INFO` | `user registered` |
| `config/exceptions.py` | `WARNING` | будь-яка `4xx`: метод, шлях, статус, `user_id`; для `400` — назви полів |
| `config/exceptions.py` | `ERROR` | `500` з трейсбеком |

## REST API Endpoints

Усі дані передаються у форматі JSON.

> **Статус реалізації:** реалізовано Games, Genres, Hubs, Auth & Profile і CORS.
> Reviews, Cart & Orders — заплановано.

### Автентифікація та ролі

API використовує JWT. Після логіну клієнт отримує пару токенів:

| Токен | Час життя | Призначення |
|---|---|---|
| `access` | 5 хвилин | додається до кожного захищеного запиту |
| `refresh` | 1 доба | отримання нового `access` без повторного логіну |

Заголовок для захищених запитів:

```http
Authorization: Bearer <access>
```

Ролі користувачів:

| Роль | Де зберігається | Права |
|---|---|---|
| `user` | `Profile.role` | читати каталог, переглядати власний профіль |
| `admin` | `Profile.role` | усе, що `user`, + створювати/редагувати/видаляти хаби, жанри, ігри |

`is_staff` (доступ до Django admin) **не** дає прав на запис у каталог — перевіряється саме `Profile.role`.

> Суперюзер автоматично отримує `role="admin"` (сигнал `post_save`).
> Змінити роль можна в адмінці: **Users → Profiles**.

Правила доступу:

| Endpoint | Метод | Доступ |
|---|---|---|
| `/games`, `/genres`, `/hubs`, їхні `{id}` та `/{id}/games` | `GET` | публічно |
| `/games`, `/genres`, `/hubs` | `POST`, `PUT`, `DELETE` | лише `admin` |
| `/register`, `/token`, `/token/refresh` | `POST` | публічно |
| `/users/me` | `GET` | будь-який автентифікований |

Усі помилки мають однаковий формат:

```json
{
  "error": {
    "message": "Невалідні дані.",
    "details": {
      "email": ["Введіть коректну email-адресу."]
    }
  }
}
```

`details` — порожній об'єкт (`{}`), якщо помилка не стосується конкретних полів.

| Код | Коли виникає |
|---|---|
| `400` | невалідні дані; у `details` — повідомлення по кожному полю |
| `401` | немає токена; токен битий або прострочений; невірний логін |
| `403` | токен валідний, але роль не `admin` |
| `404` | об'єкта не існує |
| `405` | метод не підтримується |
| `409` | хаб або жанр має пов'язані ігри |

### 1. Настільні ігри (Games)
* **`GET /api/v1/games`**
  * **Використання:** Отримання переліку ігор із фільтрацією, пошуком та сортуванням.
  * **Request method:** `GET`
  * **Query parameters:**
    * `search` (string) — пошук за назвою
    * `hub_id` (integer) — фільтр за хабом
    * `genre_id` (integer) — фільтр за жанром
    * `min_players` (integer) — мінімальна кількість гравців
    * `complexity` (string) — складність (`Easy`, `Medium`, `Hard`)
    * `sort` (string) — сортування (`price_asc`, `price_desc`, `rating_desc`, `rating_asc`, `popularity`)
  * **Request body:** немає
  * **Response status:** `200 OK`
  * **Response body:**
    ```json
    {
      "count": 12,
      "results": [
        {
          "id": 1,
          "title": "Catan",
          "rental_price_per_day": 150.0,
          "rating": 4.8,
          "min_players": 3,
          "max_players": 4,
          "complexity": "Medium",
          "hub": { "id": 10, "name": "Dice & Roll Kyiv" }
        }
      ]
    }
    ```

* **`GET /api/v1/games/{id}`**
  * **Використання:** Отримання детальної інформації про конкретну гру.
  * **Request method:** `GET`
  * **Request body:** немає
  * **Response status:** `200 OK` / `404 Not Found`
  * **Response body:**
    ```json
    {
      "id": 1,
      "title": "Catan",
      "description": "Класична містобудівна стратегія про освоєння острова...",
      "rental_price_per_day": 150.0,
      "play_time_mins": 90,
      "min_players": 3,
      "max_players": 4,
      "complexity": "Medium",
      "rating": 4.8,
      "hub": { "id": 10, "name": "Dice & Roll Kyiv" },
      "genres": [{ "id": 5, "name": "Стратегії" }]
    }
    ```

* **`POST /api/v1/games`**
  * **Використання:** Додавання нової гри в каталог (лише адміністратор).
  * **Request method:** `POST`
  * **Request body:**
    ```json
    {
      "title": "Catan",
      "description": "Класична містобудівна стратегія...",
      "rental_price_per_day": 150.0,
      "play_time_mins": 90,
      "min_players": 3,
      "max_players": 4,
      "complexity": "Medium",
      "hub_id": 10,
      "genre_ids": [5]
    }
    ```
  * **Response status:** `201 Created`
  * **Response body:**
    ```json
    {
      "id": 1,
      "title": "Catan",
      "status": "created"
    }
    ```

* **`PUT /api/v1/games/{id}`**
  * **Використання:** Повне оновлення даних гри.
  * **Request method:** `PUT`
  * **Request body:**
    ```json
    {
      "title": "Catan (Updated)",
      "description": "Оновлений опис...",
      "rental_price_per_day": 160.0,
      "play_time_mins": 90,
      "min_players": 3,
      "max_players": 4,
      "complexity": "Medium",
      "hub_id": 10,
      "genre_ids": [5]
    }
    ```
  * **Response status:** `200 OK`

* **`DELETE /api/v1/games/{id}`**
  * **Використання:** Видалення гри з каталогу.
  * **Request method:** `DELETE`
  * **Request body:** немає
  * **Response status:** `204 No Content`

---

### 2. Жанри та Категорії (Genres)
* **`GET /api/v1/genres`**
  * **Використання:** Отримання списку всіх жанрів.
  * **Request method:** `GET`
  * **Request body:** немає
  * **Response status:** `200 OK`
  * **Response body:**
    ```json
    [
      { "id": 5, "name": "Стратегії", "description": "Ігри на планування та розвиток" },
      { "id": 6, "name": "Кооперативні", "description": "Командна гра проти ігрового поля" }
    ]
    ```

* **`POST /api/v1/genres`**
  * **Використання:** Створення нового жанру.
  * **Request method:** `POST`
  * **Request body:**
    ```json
    {
      "name": "Стратегії",
      "description": "Ігри на планування та розвиток"
    }
    ```
  * **Response status:** `201 Created`
  * **Response body:**
    ```json
    {
      "id": 5,
      "name": "Стратегії",
      "description": "Ігри на планування та розвиток"
    }
    ```

* **`GET /api/v1/genres/{id}/games`**
  * **Використання:** Отримання всіх ігор обраного жанру.
  * **Request method:** `GET`
  * **Request body:** немає
  * **Response status:** `200 OK`
  * **Response body:**
    ```json
    {
      "genre_id": 5,
      "genre_name": "Стратегії",
      "games": [
        { "id": 1, "title": "Catan", "rating": 4.8 }
      ]
    }
    ```

---

### 3. Ігрові Хаби та Клуби (Hubs)
* **`GET /api/v1/hubs`**
  * **Використання:** Отримання списку локальних хабів.
  * **Request method:** `GET`
  * **Request body:** немає
  * **Response status:** `200 OK`
  * **Response body:**
    ```json
    [
      { "id": 10, "name": "Dice & Roll Kyiv", "address": "вул. Хрещатик, 1", "phone": "+380441234567" }
    ]
    ```

* **`POST /api/v1/hubs`**
  * **Використання:** Створення нового хабу.
  * **Request method:** `POST`
  * **Request body:**
    ```json
    {
      "name": "Dice & Roll Kyiv",
      "address": "вул. Хрещатик, 1",
      "phone": "+380441234567",
      "description": "Хаб у центрі Києва"
    }
    ```
  * **Response status:** `201 Created`
  * **Response body:**
    ```json
    {
      "id": 10,
      "name": "Dice & Roll Kyiv",
      "address": "вул. Хрещатик, 1",
      "phone": "+380441234567",
      "description": "Хаб у центрі Києва"
    }
    ```

* **`GET /api/v1/hubs/{id}/games`**
  * **Використання:** Отримання всіх ігор, наявних у конкретному хабі.
  * **Request method:** `GET`
  * **Request body:** немає
  * **Response status:** `200 OK`
  * **Response body:**
    ```json
    {
      "hub_id": 10,
      "hub_name": "Dice & Roll Kyiv",
      "games": [
        { "id": 1, "title": "Catan", "rental_price_per_day": 150.0 }
      ]
    }
    ```

---

### 4. Відгуки (Reviews) — planned

> Статус: заплановано, у поточній версії не реалізовано.

* **`GET /api/v1/games/{id}/reviews`**
  * **Використання:** Перегляд усіх відгуків для конкретної гри.
  * **Request method:** `GET`
  * **Request body:** немає
  * **Response status:** `200 OK`
  * **Response body:**
    ```json
    [
      {
        "id": 101,
        "user_name": "Олексій",
        "rating": 5,
        "comment": "Чудова гра для компанії!",
        "created_at": "2026-10-10T12:00:00Z"
      }
    ]
    ```

* **`POST /api/v1/games/{id}/reviews`**
  * **Використання:** Додавання відгуку та оцінки авторизованим користувачем.
  * **Request method:** `POST`
  * **Request body:**
    ```json
    {
      "rating": 5,
      "comment": "Чудова гра для компанії!"
    }
    ```
  * **Response status:** `201 Created`

---

### 5. Кошик та Замовлення (Cart & Orders) — planned

> Статус: заплановано, у поточній версії не реалізовано.

* **`GET /api/v1/cart`**
  * **Використання:** Перегляд поточного кошика оренди користувача.
  * **Request method:** `GET`
  * **Request body:** немає
  * **Response status:** `200 OK`
  * **Response body:**
    ```json
    {
      "items": [
        {
          "cart_item_id": 1,
          "game": { "id": 1, "title": "Catan", "rental_price_per_day": 150.0 },
          "rental_days": 3,
          "item_total": 450.0
        }
      ],
      "total_price": 450.0
    }
    ```

* **`POST /api/v1/cart/items`**
  * **Використання:** Додавання гри до кошика.
  * **Request method:** `POST`
  * **Request body:**
    ```json
    {
      "game_id": 1,
      "rental_days": 3
    }
    ```
  * **Response status:** `201 Created`

* **`DELETE /api/v1/cart/items/{id}`**
  * **Використання:** Видалення товару з кошика.
  * **Request method:** `DELETE`
  * **Request body:** немає
  * **Response status:** `204 No Content`

* **`POST /api/v1/orders`**
  * **Використання:** Оформлення замовлення/оренди (конвертує всі товари з кошика в замовлення).
  * **Request method:** `POST`
  * **Request body:** немає *(TODO: за потреби додати поле для коментаря або адреси доставки)*
  * **Response status:** `201 Created`
  * **Response body:**
    ```json
    {
      "order_id": 101,
      "status": "confirmed",
      "total_price": 450.0,
      "created_at": "2026-10-13T15:00:00Z"
    }
    ```

* **`GET /api/v1/orders`**
  * **Використання:** Перегляд історії замовлень поточного користувача.
  * **Request method:** `GET`
  * **Request body:** немає
  * **Response status:** `200 OK`
  * **Response body:**
    ```json
    [
      {
        "order_id": 101,
        "status": "confirmed",
        "total_price": 450.0,
        "created_at": "2026-10-13T15:00:00Z",
        "items": [
          { "game_title": "Catan", "rental_days": 3, "price_per_day": 150.0 }
        ]
      }
    ]
    ```

---

### 6. Авторизація та Профіль (Auth & Profile)

> Реалізовано

#### `POST /api/v1/register`

Реєстрація нового користувача. Доступ: публічний.

Request body:

```json
{
  "username": "alina",
  "first_name": "Аліна",
  "last_name": "Іваненко",
  "email": "alina@example.com",
  "password": "StrongPass1",
  "password_confirmation": "StrongPass1"
}
```

Правила валідації:

| Поле | Обов'язкове | Правила |
|---|---|---|
| `username` | так | до 150 символів, унікальний |
| `first_name` | ні | до 150 символів |
| `last_name` | ні | до 150 символів |
| `email` | так | коректний email, до 254 символів, унікальний без урахування регістру |
| `password` | так | 8–128 символів, велика й мала літери, цифра |
| `password_confirmation` | так | має збігатися з `password` |

Response `201 Created`:

```json
{
  "id": 1,
  "username": "alina",
  "first_name": "Аліна",
  "last_name": "Іваненко",
  "email": "alina@example.com",
  "role": "user"
}
```

Приклад помилки `400 Bad Request`:

```json
{
  "error": {
    "message": "Невалідні дані.",
    "details": {
      "username": ["Користувач з таким username вже існує."],
      "password": ["Пароль має містити хоча б одну велику літеру."]
    }
  }
}
```

Пароль зберігається у вигляді хешу. `Profile` із роллю `user` створюється автоматично.

#### `POST /api/v1/token`

Логін. Доступ: публічний.

Request body:

```json
{
  "username": "alina",
  "password": "StrongPass1"
}
```

Response `200 OK`:

```json
{
  "access": "eyJhbGciOi...",
  "refresh": "eyJhbGciOi..."
}
```

Помилка `401 Unauthorized`:

```json
{
  "error": {
    "message": "Невірний username або пароль.",
    "details": {}
  }
}
```

#### `POST /api/v1/token/refresh`

Отримання нового `access` за `refresh`. Доступ: публічний.

Request body:

```json
{
  "refresh": "eyJhbGciOi..."
}
```

Response `200 OK`:

```json
{
  "access": "eyJhbGciOi..."
}
```

Якщо `refresh` прострочений, битий або це `access`-токен:

```json
{
  "error": {
    "message": "Токен недійсний або прострочений. Увійдіть повторно.",
    "details": {}
  }
}
```

#### `GET /api/v1/users/me`

Дані поточного користувача. Доступ: будь-який автентифікований.

Request headers:

```http
Authorization: Bearer <access>
```

Response `200 OK`:

```json
{
  "id": 1,
  "username": "alina",
  "first_name": "Аліна",
  "last_name": "Іваненко",
  "email": "alina@example.com",
  "role": "admin"
}
```

Без токена — `401 Unauthorized`:

```json
{
  "error": {
    "message": "Потрібна автентифікація. Передайте access-токен у заголовку Authorization.",
    "details": {}
  }
}
```

#### Вихід (logout)

Окремого ендпоінта немає. Клієнт видаляє `access` і `refresh` зі свого сховища
(`localStorage` / `sessionStorage`). Після цього токени не використовуються.

---

## Схема бази даних (Database Schema)

![Database Schema](./db_schema.png)

### Опис таблиць та зв'язків:

1. **`Users`**: `id`, `username`, `password` (хеш), `first_name`, `last_name`, `email`, `is_staff`, `is_superuser`, `is_active`, `date_joined`, `role` (`user` / `admin`)
2. **`Hubs`**: `id`, `name`, `address`, `phone`, `description`
3. **`Genres`**: `id`, `name` (unique), `description`
4. **`Games`**: `id`, `title`, `description`, `rental_price_per_day`, `play_time_mins`, `min_players`, `max_players`, `complexity`, `rating`, `hub_id` *(FK -> Hubs)*
5. **`GameGenres`**: `game_id` *(FK -> Games)*, `genre_id` *(FK -> Genres)* — *(зв'язок M:N)*
6. **`Reviews`**: `id`, `user_id` *(FK -> Users)*, `game_id` *(FK -> Games)*, `rating`, `comment`, `created_at`
7. **`CartItems`**: `id`, `user_id` *(FK -> Users)*, `game_id` *(FK -> Games)*, `rental_days`
8. **`Orders`**: `id`, `user_id` *(FK -> Users)*, `total_price`, `status`, `created_at`
9. **`OrderItems`**: `id`, `order_id` *(FK -> Orders)*, `game_id` *(FK -> Games)*, `rental_days`, `price_per_day`

> Фактичні назви таблиць у БД: `Users` → `auth_user` + `users_profile` (роль зберігається окремо), `Hubs` → `catalog_hub`, `Genres` → `catalog_genre`, `Games` → `catalog_game`, `GameGenres` → `catalog_game_genres`.
> `Reviews`, `CartItems`, `Orders`, `OrderItems` — заплановані, у поточній версії таблиць ще немає.
> `db_schema.png` ілюструє початковий дизайн; актуальна схема — в міграціях (`catalog/migrations`, `users/migrations`).