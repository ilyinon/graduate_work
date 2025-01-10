#### Ссылка на репозиторий
```bash
https://github.com/ilyinon/graduate_work
```

#### Общая схема
##### Схема
![alt text](https://www.plantuml.com/plantuml/png/ZLHDQzj04BtlhnXyJlv03oM-57eflWSTDhBgYDYIaTPGA0KdgTj32avAJwNGbXvwTKrCX6sfVs7s7_LDLd6os38rtkytRzwyCJxAZSxCQD1NoiIc7n5_uuANTioLFUS5rZaNs9KyirF2DBOJN5pm0g0BUmd0Z8PPEaZ3j1lbIkdGf1dnTwvuPJ_n7TOvmYG0vuVdQxxbDHALGWwUiK2GSgpKK8TdkXTHYpzpYGHuH6mfK5uGt_2CLnYbasUlMcyLuNFygXSdRmBrxWb3d9WeItIVsfsNBQfnxP4v3TosCyh2Kvr73yTD6JxDS7JIZqDwdQM9sT2ya5D3EX_PxWxYv4pVOrLN6tsYSw0xQMvwMPHl2_ELU4eTYMgobmuFdzFnKxs1QlRQeNtL0JqZ_iL_1GNc5NXhu-MguZN64kCMpo1LVZB7-9-D2r18tJLVYRJhNiTN6jPrgqS71Eiv9CWV8Fx35UgQaJrl5EkJECSb_5haYbZCXNqFmKkOz07xAIalrsFS_Z2rQNj3RNjY3xRqsokrGqRz2t8E_7Pipki29i2D2LXWU6CFCUOatnl-ufcpnVvp1nkc4i8hNA-TTEJb2bc4trvYbP8c1-vcXO8_ReAbKmX4vI92EKlt9xPJHA-bEF0KGb2V-SvLe8wYf8k_idy0)

##### FR / NFR
Функциональные требовния: [docs/FR.md](docs/FR.md)
НеФункциональные требования: [docs/NFR.md](docs/NFR.md)

##### Допущенные упрощения
```
Purchase по факту сервис заглушка который делает отображение тарифов, checkout и эмулирует оплату.
```

##### Описание сервисов
```
- Auth - отвечает за аутентификацию, регистрацию, проверку ролей
- Purchase - эмулирует сервис оплаты, а также используется для проверки стоимости подписки, через него фронт запрашивает список тарифов
- Promocodes - предоставляет список, генерирует, использует и возвращает в пользование промокоды
```


##### Описание процесса покупки
```
1. Пользователь, залогинившись, через фронт выбирает тариф. Тарифы отдаются из purchase и хранятся в БД postgres
2. Когда тариф выбран, предоставляется возможность использовать промокод, в случае работающего промокода стоимость пересчитывается.
3. Промокод при отправке, уходит в purchase, который сам запрашивает promocodes. Цена формируется со стороны purchase. 
4. Промокод проверяется перед покупкой на разные условия, такие как: срок действия, возомжно ли его использовать ( не вышел ли лимит).
5. При покупке, на purchase уходит ID выбранного тарифа и прмокод, по UUID пользователю ему будет ( после оплаты добавлен тариф). Во время покупки происходит использоание промокода ( увеличивается счётчик использований), если покупка не прошла - то счётчик откатывается.
```


#### Запуск решения
##### скопировать конфиг
```bash
cp .env_example .env
```

##### запустить infra и все приложения
```bash
make infra
make all
```

###### Добавить пользователя с ролью admin
```bash
docker-compose exec -ti auth python cli/manage.py
```

###### Добавить сервисного пользователя, для межсервисного общения
```bash
docker-compose exec -ti auth python cli/service.py
```


##### endpoints для доступа к сервисам
```
auth(API): http://localhost/api/v1/auth/openapi
promocoes(API): http://localhost/api/v1/promocodes/openapi
purchase(API): http://localhost/api/v1/purchase/openapi

front: http://localhost:3000/
adminka: http://localhost:3001/
```


#####  Сервис промокодов
<details>
<summary>http://localhost/api/v1/promocodes/openapi</summary>

![alt text](images/promocodes.png)

###### Список промокодов

```bash
curl -X 'GET' \
  'http://localhost/api/v1/promocodes/list/?skip=0&limit=100' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer <token>'
```

```bash
[
  {
    "id": "8aa35a86-1be4-4e52-96de-caa24bc07db3",
    "promocode": "FREE-STANDARD-FOR-ONE-MONTH",
    "discount_percent": 0,
    "discount_rubles": 399,
    "start_date": "2025-01-01T00:00:00",
    "end_date": "2025-12-31T00:00:00",
    "usage_limit": 10,
    "used_count": 0,
    "is_active": true,
    "is_one_time": false
  },
  {
    "id": "331472ba-ae64-4df5-ae7d-2ffa8ee4dbd5",
    "promocode": "MINUS-TEN-PERCENTS",
    "discount_percent": 10,
    "discount_rubles": 0,
    "start_date": "2025-01-01T00:00:00",
    "end_date": "2025-12-31T00:00:00",
    "usage_limit": 0,
    "used_count": 0,
    "is_active": true,
    "is_one_time": false
  },
  {
    "id": "ea54ad6b-09ae-4048-9b5e-59db3c0d20e6",
    "promocode": "MINUS100",
    "discount_percent": 0,
    "discount_rubles": 100,
    "start_date": "2025-01-01T00:00:00",
    "end_date": "2025-12-31T00:00:00",
    "usage_limit": 0,
    "used_count": 0,
    "is_active": true,
    "is_one_time": false
  }
]
```

###### Применить промокод
```bash
curl -X 'POST' \
  'http://localhost/api/v1/promocodes/apply/MINUS100' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer <token>' \
  -d ''
```

```bash
{
  "detail": "Промокод успешно применен"
}
```

###### Отменить использование промокода
```bash
curl -X 'POST' \
  'http://localhost/api/v1/promocodes/revoke/MINUS100' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiYWU0NzMxMjMtMjFlOC00OGIxLWE1NTktNGQxZTc5YzAxNDBhIiwiZW1haWwiOiJzZXJ2aWNlQGNpbmVtYS5pbyIsInJvbGVzIjpbInNlcnZpY2UiXSwiZXhwIjoxNzY3NTI2MjQ5LCJqdGkiOiJjZjE5ODA5Mi04MmY4LTRlYTgtYWMwYi04YmRiNjg1NzFiMjIifQ.oYM8Afkua_33_50ttiiclMQs0Xdtc5fDAkN_ukAkZCs' \
  -d ''
```

```bash
{
  "detail": "Использование промокода отменено"
}
```


###### Проверить промокод
```bash
curl -X 'GET' \
  'http://localhost/api/v1/promocodes/validate/MINUS100' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiYWU0NzMxMjMtMjFlOC00OGIxLWE1NTktNGQxZTc5YzAxNDBhIiwiZW1haWwiOiJzZXJ2aWNlQGNpbmVtYS5pbyIsInJvbGVzIjpbInNlcnZpY2UiXSwiZXhwIjoxNzY3NTI2MjQ5LCJqdGkiOiJjZjE5ODA5Mi04MmY4LTRlYTgtYWMwYi04YmRiNjg1NzFiMjIifQ.oYM8Afkua_33_50ttiiclMQs0Xdtc5fDAkN_ukAkZCs'
```

```bash
{
  "promocode": "MINUS100",
  "discount_percent": 0,
  "discount_rubles": 100
}
```

###### Сгенерировать промокод
```bash
curl -X 'POST' \
  'http://localhost/api/v1/promocodes/generate/' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiYWU0NzMxMjMtMjFlOC00OGIxLWE1NTktNGQxZTc5YzAxNDBhIiwiZW1haWwiOiJzZXJ2aWNlQGNpbmVtYS5pbyIsInJvbGVzIjpbInNlcnZpY2UiXSwiZXhwIjoxNzY3NTI2MjQ5LCJqdGkiOiJjZjE5ODA5Mi04MmY4LTRlYTgtYWMwYi04YmRiNjg1NzFiMjIifQ.oYM8Afkua_33_50ttiiclMQs0Xdtc5fDAkN_ukAkZCs' \
  -H 'Content-Type: application/json' \
  -d '{
  "discount_percent": 15,
  "discount_rubles": 0,
  "start_date": "2025-01-10T16:10:18.928Z",
  "end_date": "2025-12-31T16:10:18.928Z",
  "usage_limit": 0,
  "is_active": true,
  "is_one_time": true
}'
```

```bash
{
  "id": "90eabb83-ec68-41ef-80a0-cab4aa3b0fec",
  "promocode": "XA7Q4EWMEGMY",
  "discount_percent": 15,
  "discount_rubles": 0,
  "start_date": "2025-01-10T16:10:18.928000",
  "end_date": "2025-12-31T16:10:18.928000",
  "usage_limit": 0,
  "used_count": 0,
  "is_active": true,
  "is_one_time": true
}
```

###### Применить промокод со стороны администратора
```bash
curl -X 'POST' \
  'http://localhost/api/v1/promocodes/assign/' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiYWU0NzMxMjMtMjFlOC00OGIxLWE1NTktNGQxZTc5YzAxNDBhIiwiZW1haWwiOiJzZXJ2aWNlQGNpbmVtYS5pbyIsInJvbGVzIjpbInNlcnZpY2UiXSwiZXhwIjoxNzY3NTI2MjQ5LCJqdGkiOiJjZjE5ODA5Mi04MmY4LTRlYTgtYWMwYi04YmRiNjg1NzFiMjIifQ.oYM8Afkua_33_50ttiiclMQs0Xdtc5fDAkN_ukAkZCs' \
  -H 'Content-Type: application/json' \
  -d '{
  "user_email": "user@cinema.io",
  "promocode": "MINUS100"
}'
```

```bash
{
  "success": true,
  "message": "Промокод успешно применен к аккаунту пользователя"
}
```
</details>

##### Сервис purchase
<details>
<summary>http://localhost/api/v1/purchase/openapi</summary>



![alt text](images/purchase.png)
</details>

#####   Front
<details>
<summary>http://localhost:3000</summary>
Добавлен тестовый фронт, где можно зарегистировать, залогиниться под пользователем, ввести промокод, увидеть цену со скидкой и "купить".

![alt text](images/front1.png)
![alt text](images/front2.png)

</details>

#####   Adminka
<details>
<summary>http://localhost:3001</summary>
Добавлена админка где можно залогиниться под админом ( добавляем скриптом).
Доступно: генерация промокода, валидация, просмотр списка промокодов, а также назначение прмокодома пользователю вручную


![alt text](images/adminka.png)

![alt text](images/adminka0.png)
![alt text](images/adminka1.png)

![alt text](images/adminka_validate.png)

![alt text](images/adminka_list.png)

![alt text](images/adminka_assign.png)

</details>

#### Запуск тестов

```bash
make test_promocodes
```

```bash
============================= test session starts ==============================
platform linux -- Python 3.12.8, pytest-7.4.3, pluggy-1.5.0 -- /usr/local/bin/python3
cachedir: .pytest_cache
rootdir: /opt
plugins: asyncio-0.23.8, mock-resources-2.12.1, Faker-30.1.0, postgresql-6.1.1, alembic-0.11.1, anyio-4.8.0
asyncio: mode=Mode.STRICT
collecting ... collected 10 items

tests/functional/src/auth/test_promocodes.py::test_validate_promocode PASSED [ 10%]
tests/functional/src/auth/test_promocodes.py::test_invalid_promocode PASSED [ 20%]
tests/functional/src/auth/test_promocodes.py::test_list_promocodes PASSED [ 30%]
tests/functional/src/auth/test_promocodes.py::test_apply_promocode PASSED [ 40%]
tests/functional/src/auth/test_promocodes.py::test_apply_invalid_promocode PASSED [ 50%]
tests/functional/src/auth/test_promocodes.py::test_revoke_promocode PASSED [ 60%]
tests/functional/src/auth/test_promocodes.py::test_revoke_invalid_promocode PASSED [ 70%]
tests/functional/src/auth/test_promocodes.py::test_generate_promocode PASSED [ 80%]
tests/functional/src/auth/test_promocodes.py::test_invalid_generate_promocode PASSED [ 90%]
tests/functional/src/auth/test_promocodes.py::test_assign_promocode PASSED [100%]

======================== 10 passed, 4 warnings in 1.71s ========================
```


##### Оповещение в ТГ

![alt text](images/tg.png)

##### Sentry 

Отправляем исключения в Sentry
```bash
if promocodes_settings.sentry_enable:
    sentry_sdk.init(
        dsn=promocodes_settings.sentry_dsn,
        traces_sample_rate=promocodes_settings.sentry_traces_sample_rate,
        _experiments={
            "continuous_profiling_auto_start": True,
        },
    )
```

##### Github Actions
Запускаются проверки, пример: https://github.com/ilyinon/graduate_work/actions/runs/12713326064/job/35440964847
![alt text](images/github.png)