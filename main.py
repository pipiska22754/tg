from telethon import TelegramClient
from handlers import register_handlers, read_chat_ids_from_file
import os

# Данные из переменных окружения
api_id = os.environ.get('API_ID')
api_hash = os.environ.get('API_HASH')
phone_1 = os.environ.get('PHONE_1')
phone_2 = os.environ.get('PHONE_2')
bot_token = os.environ.get('BOT_TOKEN')

# Инициализация клиентов
client_1 = TelegramClient('session_1', api_id, api_hash)
client_2 = TelegramClient('session_2', api_id, api_hash)
bot_client = TelegramClient('bot_session', api_id, api_hash).start(bot_token=bot_token)

# Регистрация обработчиков
register_handlers(bot_client, client_1, client_2)

# Запуск
with client_1, client_2, bot_client:
    client_1.start()
    client_2.start()
    bot_client.run_until_disconnected()