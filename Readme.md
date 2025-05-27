# Установка

## Docker
https://wirenboard.com/wiki/Docker

## Клонирование проекта
```
git clone https://github.com/rydikov/wb-topics-reader-bot.git
```

## Переменные окружения
В каталоге с проектом необходимо создать файл .env и добавить в него следующие переменные в формате:
```
ПЕРЕМЕННАЯ = ЗНАЧЕНИЕ
```
Список обязательных переменных:
```
TELEGRAM_TOKEN - Токен бота
WB_MQTT_HOST - Адрес хоста mqtt
WB_MQTT_PORT - Порт mqtt
```

Далее надо создать файл users.yml в котором будут соотвествия топиков и пользователей

Пример для 2х пользователей:

```
users:
  53757777:
    - topic: /devices/system/controls/Current uptime
      label: Аптайм 
    - topic: /devices/hwmon/controls/CPU Temperature
      label: Температура процессора
  53757111:
    - topic: /devices/hwmon/controls/Board Temperature
      label: Температура материнской платы
```

Число в конфигурации это уникальный идентификатор пользователя


## Сборка 
Внутри каталога с проектом выполните
```
docker compose build
```

## Запуск
Внутри каталога с проектом выполните
```
docker compose up
```
Если нужно запустить в режиме демона, то
```
docker compose up -d
```

## Доступные команды бота
```
/status - Получить показания топиков
```
 

