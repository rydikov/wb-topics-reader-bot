import os
import asyncio
import logging
import yaml

import paho.mqtt.client as mqtt

from aiogram.client.bot import DefaultBotProperties
from aiogram import F, Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.utils.markdown import hbold, hcode


LOG_LEVEL = logging.DEBUG if os.environ.get('DEBUG') else logging.INFO

logging.basicConfig(
    level=LOG_LEVEL,
    format='%(asctime)s %(levelname)s: %(message)s',
    datefmt='%d/%m/%Y %H:%M:%S'
)

logger = logging.getLogger(__name__)


TOKEN = os.environ['TELEGRAM_TOKEN']

mqtt_topics = []

with open(os.path.join('users.yml')) as f:
    config = yaml.safe_load(f)

# Collect mqtt topics
for user_id in config['users']:
    for v in config['users'][user_id]:
        if v['topic'] not in mqtt_topics:
            mqtt_topics.append(v['topic'])

logger.info(mqtt_topics)

dp = Dispatcher()
dp.message.filter(F.from_user.id.in_(config['users'].keys()))

# MQTT
topics_data = {}
mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

WB_MQTT_HOST = os.environ['WB_MQTT_HOST']
WB_MQTT_PORT = int(os.environ['WB_MQTT_PORT'])


def on_connect(client, userdata, flags, reason_code, properties):
    logger.info("MQTT подключено")
    subscriptions = [(topic, 0) for topic in mqtt_topics]
    client.subscribe(subscriptions)


def on_message(client, userdata, msg):
    payload = msg.payload.decode('utf-8')
    topics_data[msg.topic] = payload
    logger.debug(f"MQTT: {msg.topic} => {payload}")


mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.connect(WB_MQTT_HOST, WB_MQTT_PORT, 60)
mqtt_client.loop_start()
###


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Hello, {hbold(message.from_user.full_name)}!")


# TG Commands
@dp.message(Command('status'))
async def command_status(message: Message) -> None:

    answer = ""

    for val in config['users'][message.from_user.id]:
        answer += hcode(f"{val['label']}: {topics_data.get(val['topic'], 'Нет данных')} \n")

    await message.answer(answer)
###


@dp.message()
async def default_handler(message: types.Message) -> None:
    await message.answer("Unknown command")


async def main() -> None:
    bot = Bot(TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
