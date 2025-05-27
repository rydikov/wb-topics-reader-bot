import ast
import os
import asyncio
import logging

import paho.mqtt.client as mqtt

from aiogram.client.bot import DefaultBotProperties
from aiogram import F, Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.utils.markdown import hbold, hcode


logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s: %(message)s',
    datefmt='%d/%m/%Y %H:%M:%S'
)

logger = logging.getLogger(__name__)


TOKEN = os.environ['TELEGRAM_TOKEN']
MQTT_TOPICS_WITH_ADMINS = ast.literal_eval(os.environ["MQTT_TOPICS_WITH_ADMINS"])

MQTT_TOPICS = list(set(item for sublist in MQTT_TOPICS_WITH_ADMINS.values() for item in sublist))

logger.info(MQTT_TOPICS)
logger.info(MQTT_TOPICS_WITH_ADMINS)

dp = Dispatcher()
admin_ids = [int(admin_id) for admin_id in MQTT_TOPICS_WITH_ADMINS.keys()]
dp.message.filter(F.from_user.id.in_(admin_ids))

### MQTT
topics_data = {}
mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)

WB_MQTT_HOST = os.environ['WB_MQTT_HOST']
WB_MQTT_PORT = int(os.environ['WB_MQTT_PORT'])

def on_connect(client, userdata, flags, rc):
    logger.info("MQTT подключено")
    subscriptions = [(topic, 0) for topic in MQTT_TOPICS]
    client.subscribe(subscriptions)

def on_message(client, userdata, msg):
    payload = msg.payload.decode('utf-8')
    topics_data[msg.topic] = payload
    logger.info(f"MQTT: {msg.topic} => {payload}")

mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.connect(WB_MQTT_HOST, WB_MQTT_PORT, 60)
mqtt_client.loop_start()
###

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Hello, {hbold(message.from_user.full_name)}!")

### TG Commands
@dp.message(Command('status'))
async def command_status(message: Message) -> None:

    answer = ""

    for val in MQTT_TOPICS_WITH_ADMINS[message.from_user.id]:
        answer += f"{topics_data.get(val, 'No value')} \n"

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
