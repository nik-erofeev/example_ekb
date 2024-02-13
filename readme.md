# Установка и запуск
Создайте в корне приложения файл **.env** и определите в нём все переменные, указанные в [.env.example](./.env.example).


## Запуск через docker-compose

#### Собрать и запустить приложение с помощью
```sh
$ docker-compose build
$ docker-compose up
```
#### Остановить приложение с помощью
```sh
$ docker-compose down
```


#### Перейти на [http://localhost:8000/docs/](http://localhost:8000/docs)



## Локально

#### Установить и активировать виртуальное окружение с помощью команд:
```sh
$ python3.11 -m venv venv
$ source venv/bin/activate
```

#### Установить зависимости:
```sh
$ pip install -r requirements.txt
```


#### Прогнать миграции с помощью с помощью [alembic](https://alembic.sqlalchemy.org/en/latest/):
```sh
$ alembic upgrade head
```

#### Запусить тесты [alembic](https://alembic.sqlalchemy.org/en/latest/):
```sh
$ poetry run pytest
```

#### Запустить приложение с помощью [uvicorn](https://www.uvicorn.org/):
```sh
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
