from telethon.sync import events
import json
import os

# Словарь для хранения статистики
message_stats = {'sent': 0, 'not_sent': 0}
chat_ids = read_chat_ids_from_file()  # Читаем ID чатов из файла

async def handle_command(event, client_1, client_2):
    command = event.text.lower()

    if command == '/start':
        await event.respond('Бот готов к работе!')
    elif command == '/info':
        await event.respond(f'Отправлено: {message_stats["sent"]}\nНе отправлено: {message_stats["not_sent"]}')
    elif command.startswith('/chats_dobavit'):
        parts = command.split()
        if len(parts) < 2:
            await event.respond('Ошибка: /chats_dobavit chat_id')
            return
        chat_id = parts[1]
        chat_ids.append(chat_id)
        save_chat_ids_to_file()
        await event.respond(f'Чат {chat_id} добавлен.')
    elif command.startswith('/chat_remove'):
        parts = command.split()
        if len(parts) < 2:
            await event.respond('Ошибка: /chat_remove chat_id')
            return
        chat_id = parts[1]
        if chat_id in chat_ids:
            chat_ids.remove(chat_id)
            save_chat_ids_to_file()
            await event.respond(f'Чат {chat_id} удален.')
        else:
            await event.respond('Чат не найден.')
    elif command.startswith('/message'):
        await event.respond('Введите текст рассылки:')
        @client_1.on(events.NewMessage(incoming=True))
        async def handle_broadcast(event):
            message_text = event.text
            for chat_id in chat_ids:
                try:
                    await client_1.send_message(chat_id, message_text)
                    await client_2.send_message(chat_id, message_text)
                    message_stats['sent'] += 1
                except Exception as e:
                    message_stats['not_sent'] += 1
            await event.respond('Рассылка завершена.')
    elif command == '/login':
        await event.respond('Введите номер и код через пробел:')
        @client_1.on(events.NewMessage(incoming=True))
        async def handle_login(event):
            try:
                phone, code = event.text.split()
                await client_1.start(phone=phone, code=code)
                await client_2.start(phone=phone, code=code)
                await event.respond('Авторизация успешна!')
            except Exception as e:
                await event.respond(f'Ошибка: {str(e)}')
    else:
        await event.respond('Неизвестная команда.')

def register_handlers(bot_client, client_1, client_2):
    bot_client.add_event_handler(lambda e: handle_command(e, client_1, client_2), events.NewMessage(incoming=True))

def save_chat_ids_to_file():
    with open('groups.txt', 'w') as f:
        for chat_id in chat_ids:
            f.write(f"{chat_id}\n")

def read_chat_ids_from_file():
    if not os.path.exists('groups.txt'):
        return []
    with open('groups.txt', 'r') as f:
        return [line.strip() for line in f if line.strip()]