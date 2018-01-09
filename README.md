# Тестовое задание
web-api по [заданию](https://docs.google.com/document/d/1e06lBw7CaIMYRPGi9OD_kdCtjjrtPZQ96JdXDQx3os4/edit#)

## Инструкция по запуску проекта
**Зависимости**: *python 3.6*

**Последовательность действий**:
* Создать папку под проект
* Открыть консоль и перейти в директорию созданной папки
* Создать виртуальное окружение для проекта (выполнив команду `python3 -m venv имя_окружения`)
* Слить себе репозиторий командой `git clone https://github.com/Kit-Angelov/surf_test.git`
* Войти в окружения командой
    * для linux: `source имя_окружения/bin/activate`
    * для windows: `имя_окружения\Scripts\acitvate`
* Перейти в директорию **bookShop**
* Выполнить команду `pip install requirements.txt` (установка зависимостей)
* Выполнить команду `python manage.py makemigrations` (создания файла миграции)
* Выполнить команду `python manage.py migrate` (выполнение миграций)
* Выполнить команду `python manage.py runserver` (тем самым запустив сервер django)

## Генерация данных
Для генерации данных используйте **mixer** (он есть в зависимостях)

Для генерации данных необходимо:
* Войти в консоль python выполнив команду `python manage.py shell`
* Импортировать модели приложения командой `from bookRental import models`
* Сгенерировать данные моделей (Пример команды генерации 4х авторов: `mixer.cycle(4).blend(models.Author)'

## Тесты
Для запуска тестов следует выполнить команду `python manage.py test bookRental` из директории с файлом **manage.py**

## Запросы
Для выполнения запросов к серверу можно использовать утилиту cURL

Пример запроса списка книг: `curl -X GET http://192.168.0.104:8000/books/ -H "Authorization: token 9fe36fadd696c9de75f1e0afb629b1d03553a539"`

Пример запроса авторизации: `curl -X GET http://192.168.0.104:8000/login/ -H "Content-Type: application/json" -d {"username":"_username_", "password": "_password_"}`



