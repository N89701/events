# Проект EventsAPI
Проект является API для приложения по создания календаря официальных мероприятий с возможностью переписки между пользователями.

## Запуск приложения на локальной машине
1. Клонируйте репозиторий к себе на компьютер
```
git clone git@github.com:N89701/events.git
```
2. Откройте папку проекта в вашей IDE
3. Откройте терминал и перейдите в папку infra, а затем запустите докер-оркестр
```
cd infra
docker compose up
```
Приложение запущено!
## А что оно может?
### Регистрация
Для регистрации необходимо отправить POST-запрос на:
```
http://127.0.0.1:8001/api/users/
```
следующего вида
```
{
"email":"yourbox@mail.ru",
"first_name": "Ivan",
"last_name": "Petrov",
"password": "icantbehacked"
}
```
Также необязательными аргументами при регистрации являются phone_number (например, +79265416580) и organization (например, 2 - id существующей в БД организации).
Также данный эндпоинт имеет метод GET (получение списка пользователей и конкретного пользователя), а при добавлении /me/ к URL можно получить (GET) и отредактировать (PATCH) информацию о себе.
### Вход и выход из системы
После регистрации нужно отправить POST-запрос на:
```
http://127.0.0.1:8001/api/token/login/
```
следующего вида
```
{
"email":"yourbox@mail.ru",
"password": "icantbehacked"
}
```
в ответ придет token, который нужно скопировать и вставить в Headers запроса (Key:Authorization, Value: Token <ваша-строка-токена>). Теперь все следующие запросы будут как от залогиненного пользователя.
Для того, чтобы разлогиниться, необходимо сделать залогиненный запрос на
```
http://127.0.0.1:8001/api/token/logout/
```
### Создание и просмотр организаций
Для создания организации необходимо отправить POST-запрос на:
```
http://127.0.0.1:8001/api/organizations/
```
следующего вида
```
{
"title":"Ростехнологии",
"description": "Компания прорывных технологий и смелых людей",
"address": "РФ, г. Санкт-Петербург, Невский проспект 5, этаж 4, офис 78",
"postcode": "191186"
}
```
Также можно отправить GET запрос для просмотра существующих организаций. Редактирования\удаление организаций доступно только пользователям с правами админа (is_superuser=True).
### Создание и просмотр мероприятий
Для создания мероприятия необходимо отправить POST-запрос на:
```
http://127.0.0.1:8001/api/events/
```
следующего вида
```
{
"title":"Корпоратив 2023\2024",
"description": "Корпоратив в стиле пижамной вечеринки, фото и видео съемка запрещены",
"organizations": [1, 2, 3],
"image": (можно отправить файл в Postman в режиме form-data)
"date": 25.12.2023 18:00
}
```
При создании мероприятия включается sleep(60), но запросы с других вкладок\для других пользователей на это время остаются доступны.
Для просмотра мероприятий нужно отправить GET запрос на этот же адрес. Доступны:
1. Фильтрация по дате. Можно выбирать мероприятия до\после\до и после определенного периода. Например, запрос на показ мероприятий после 10 утра 1 декабря 2020 года будет выглядеть как:
```
http://127.0.0.1:8001/api/events/?date>=01/12/2020 10.00
```
2. Сортировка по дате. Например, запрос на получение мероприятий от свежих к давним будет выглядеть так:
```
http://127.0.0.1:8001/api/events/?ordering=-date
```
3. Поиск по названию (по частичному вхождению). Например, если я хочу, чтобы в названии было слово "тусовка", запрос будет выглядеть так:
```
http://127.0.0.1:8001/api/events/?search=тусовка
```
4. Если я боюсь разорваться от выбора куда пойти, то можно ограничить количество мероприятий на странице. Например, запрос для получения мероприятий по 2 штуки на странице:
```
http://127.0.0.1:8001/api/events/?limit=2
```
Все 4 функции выше можно комбинировать с помощью символа &. Например, запрос на мероприятия, отсортированне по дате после 10 утра 1 декабря 2020 года будет выглядеть как:
```
http://127.0.0.1:8001/api/events/?date>=01/12/2020 10.00&ordering=-date
```
### Чаты
Для того чтобы начать чат, нужно сначала его создать. Для этого нужно отправить POST-запрос на:
```
http://127.0.0.1:8001/chats/
```
следующего вида (receiver - это id пользователя, с которым вы хотите начать чат)
```
{
"receiver": 1
}
```
После того, как чат создан, можно перейти к работе по Websocket-протоколу. В Headers нужно указать 2 параметра : Cookie: token=<ваш-токен>; Origin: http://127.0.0.1:8001/. В самой адресной строке нужно прописать адрес:
```
ws://127.0.0.1:8001/ws/chats/<id чата>/
```
После этого нажать Connect и появившаяся надпись на зеленом фоне даст знать, что вы на верном пути. Чтобы отправить сообщение в чат, нужно в Message прописать:
```
{"message":"Привет! Будешь сегодня на органном концерте?"}
```
и нажать Send. Сообщение отправлено, Вы великолепны!
### Контакт для обратной связи - Tg:@N89701
