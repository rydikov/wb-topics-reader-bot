# Установка

## Docker
https://wirenboard.com/wiki/Docker

## Клонирование проекта
```
git clone git@github.com:rydikov/wb-topics-reader-bot.git
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

MQTT_TOPICS_WITH_ADMINS = Словарь, где ключ это ID пользователя телеграмм, значение список топиков
```

Пример:

```
MQTT_TOPICS_WITH_ADMINS = "{12345678: ['/devices/system/controls/Current uptime', '/devices/hwmon/controls/CPU Temperature']}"
```
Важно: ID пользователя указывается как INT, без кавычек


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
 

