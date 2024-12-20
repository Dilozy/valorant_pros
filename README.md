# Проект Valorant Pro Players

**Valorant Pro Players** - это проект, который представляет из себя базу данных про-игроков дисциплины Valorant.
Каждая команда VCT имеет собственную страницу, на которой можно оставлять комментарии. Каждый игрок имеет собственную страницу,
на которую можно добавлять хайлайты, а также рекомендовать игрока по электронной почте

## Установка

### 1. Клонируйте репозиторий с GitHub

```git clone https://github.com/Dilozy/valorant_pros.```


### 2. Создайте .env файл
Затем отредактируйте файл **.env**, указав нужные значения для переменных:

    YOUTUBE_API_KEY= "Ваш Youtube API Key"
    DB_NAME= "Название базы данных"
    DB_USER= "Имя польхзователя"
    DB_PASSWORD= "Пароль пользователя БД"
    DB_HOST= "Имя хоста"
    DB_PORT= "Номер порта для БД"
    EMAIL_HOST_USER="Email пользователя smtp сервера"
    EMAIL_HOST= "Хоста smtp, например, smtp.gmail.com"
    EMAIL_HOST_PASSWORD= "Специальный пароль для доступа к smtp серверу"
    EMAIL_PORT= "Порт для smtp сервера"
    SOCIAL_AUTH_TWITCH_KEY= "API ключ для авторизации через Twitch"
    SOCIAL_AUTH_TWITCH_SECRET= "Секретный ключ для авторизации через Twitch"
    DJANGO_SECRET_KEY= "Секретный ключ для приложения Django"

### 3. Соберите и запустите контейнеры командой
```docker-compose up -d```

### 4. Доступ к приложению
После запуска контейнеров, приложение будет доступно по адресу: ```http://127.0.0.1```

### 5. Остановка контейнеров
Когда вы закончите работу, остановите контейнеры командой:
```docker-compose down```
Это остановит и удалит контейнеры, но сохранит образы.

## Описание API

### 1. Игроки (Players)

- **Получить список всех игроков**  
`GET /players/`  
Возвращает список всех игроков, зарегистрированных в системе.

- **Добавить нового игрока**  
`POST /players/`  
Создает нового игрока с указанными данными.

- **Получить информацию о конкретном игроке**  
`GET /players/{player_id}/`  
Возвращает информацию об игроке с заданным `player_id`.

- **Обновить информацию об игроке**  
`PUT /players/{player_id}/`  
Обновляет информацию об игроке с указанным `player_id`.

- **Удалить игрока**  
`DELETE /players/{player_id}/`  
Удаляет игрока с заданным `player_id`.

### 2. Команды (Teams)

- **Получить список всех команд**  
`GET /teams/`  
Возвращает список всех команд в системе.

- **Создать новую команду**  
`POST /teams/`  
Создает новую команду с указанными данными.

- **Получить информацию о конкретной команде**  
`GET /teams/{team_id}/`  
Возвращает информацию о команде с заданным `team_id`.

- **Обновить информацию о команде**  
`PUT /teams/{team_id}/`  
Обновляет информацию о команде с указанным `team_id`.

- **Удалить команду**  
`DELETE /teams/{team_id}/`  
Удаляет команду с указанным `team_id`.

### 3. Связи между игроками и командами

- **Добавить игрока в команду**  
`POST /teams/{team_id}/players/`  
Добавляет игрока в команду по `team_id`.

- **Удалить игрока из команды**  
`DELETE /teams/{team_id}/players/{player_id}/`  
Удаляет игрока из команды по `team_id` и `player_id`.

---

Этот API позволяет управлять игроками и командами, а также регулировать связи между ними.


## Контакты
    Email: denfil228@yandex.ru

    Telegram: https://t.me/Dilozy
