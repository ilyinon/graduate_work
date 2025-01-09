#### Ссылка на репозиторий
```bash
https://github.com/ilyinon/graduate_work
```

#### Общая схема
##### Схема
![alt text](https://www.plantuml.com/plantuml/png/ZLHDQzj04BtlhnXyJlv03oM-57eflWSTDhBgYDYIaTPGA0KdgTj32avAJwNGbXvwTKrCX6sfVs7s7_LDLd6os38rtkytRzwyCJxAZSxCQD1NoiIc7n5_uuANTioLFUS5rZaNs9KyirF2DBOJN5pm0g0BUmd0Z8PPEaZ3j1lbIkdGf1dnTwvuPJ_n7TOvmYG0vuVdQxxbDHALGWwUiK2GSgpKK8TdkXTHYpzpYGHuH6mfK5uGt_2CLnYbasUlMcyLuNFygXSdRmBrxWb3d9WeItIVsfsNBQfnxP4v3TosCyh2Kvr73yTD6JxDS7JIZqDwdQM9sT2ya5D3EX_PxWxYv4pVOrLN6tsYSw0xQMvwMPHl2_ELU4eTYMgobmuFdzFnKxs1QlRQeNtL0JqZ_iL_1GNc5NXhu-MguZN64kCMpo1LVZB7-9-D2r18tJLVYRJhNiTN6jPrgqS71Eiv9CWV8Fx35UgQaJrl5EkJECSb_5haYbZCXNqFmKkOz07xAIalrsFS_Z2rQNj3RNjY3xRqsokrGqRz2t8E_7Pipki29i2D2LXWU6CFCUOatnl-ufcpnVvp1nkc4i8hNA-TTEJb2bc4trvYbP8c1-vcXO8_ReAbKmX4vI92EKlt9xPJHA-bEF0KGb2V-SvLe8wYf8k_idy0)

##### Допущенные упрощения
```
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

##### endpoints для доступа к сервисам
```
auth(API): http://localhost/api/v1/auth/openapi
promocoes(API): http://localhost/api/v1/promocodes/openapi
purchase(API): http://localhost/api/v1/purchase/openapi

front: http://localhost:3000/
adminka: http://localhost:3001/
```


#### Запуск решения
##### скопировать конфиг
```bash
cp .env_example .env
```

##### запустить infra и все приложения
```bash
make infra
make auth
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
