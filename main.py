from telethon import TelegramClient
from telethon.sync import events
from handlers import register_handlers
import os

# Замените на ваши данные
api_id = 'YOUR_API_ID'
api_hash = 'YOUR_API_HASH'
phone_number_1 = 'YOUR_PHONE_NUMBER_1'
phone_number_2 = 'YOUR_PHONE_NUMBER_2'
bot_token = 'YOUR_BOT_TOKEN'

# Инициализация клиентов
client_1 = TelegramClient(phone_number_1, api_id, api_hash)
client_2 = TelegramClient(phone_number_2, api_id, api_hash)
bot_client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

# Регистрация обработчиков команд
register_handlers(bot_client)

# Функция для отправки сообщения с аккаунта
async def send_message(client, chat_id, message, file=None):
    if file:
        await client.send_file(chat_id, file, caption=message)
    else:
        await client.send_message(chat_id, message)

# Чтение ID чатов из файла
def read_chat_ids_from_file():
    chat_ids = []
    if os.path.exists('groups.txt'):
        with open('groups.txt', 'r') as file:
            for line in file:
                chat_ids.append(line.strip())
    return chat_ids

# Запуск клиентов
with client_1, client_2, bot_client:
    client_1.start()
    client_2.start()
    bot_client.run_until_disconnected()
