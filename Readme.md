# Установка

Бот работает через Docker

## Docker
https://wirenboard.com/wiki/Docker

## Клонирование проекта
```
git clone https://github.com/rydikov/wb-topics-reader-bot.git
```

## Переменные окружения
В каталоге с проектом необходимо создать файл **.env** и добавить в него следующие переменные в формате:
```
ПЕРЕМЕННАЯ = ЗНАЧЕНИЕ
```
Список обязательных переменных:
```
TELEGRAM_TOKEN = Токен бота (создается в @BotFather)
WB_MQTT_HOST = Адрес хоста mqtt (обычно 127.0.0.1)
WB_MQTT_PORT = Порт mqtt (обычно 1883)
```

Для просмотра отладочных сообщений добавьте:
```
DEBUG = True
```


Далее надо создать файл **users.yml** в котором будут соотвествия топиков и пользователей

Пример для 2х пользователей:

```yaml
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

Число в конфигурации это уникальный идентификатор пользователя, можно узнать у бота  @getmyid_bot


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
 