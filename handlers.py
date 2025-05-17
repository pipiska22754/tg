from telethon.sync import events
import json

# Словарь для хранения количества отправленных и не отправленных сообщений
message_stats = {'sent': 0, 'not_sent': 0}

# Список для хранения ID чатов
chat_ids = read_chat_ids_from_file()  # Читаем ID чатов из файла при запуске

async def handle_command(event):
    # Получаем команду от пользователя
    command = event.text.lower()

    if command == '/start':
        await event.respond('Бот готов к работе!')
    elif command == '/info':
        await event.respond(f'Отправлено сообщений: {message_stats["sent"]}\nНе отправлено сообщений: {message_stats["not_sent"]}')
    elif command.startswith('/chats_dobavit'):
        parts = command.split()
        if len(parts) < 2:
            await event.respond('Некорректная команда. Пример: /chats_dobavit chat_id')
            return

        chat_id = parts[1]
        chat_ids.append(chat_id)
        await event.respond(f'Чат {chat_id} добавлен в список.')
        save_chat_ids_to_file()  # Сохраняем изменения в файл
    elif command.startswith('/chat_remove'):
        parts = command.split()
        if len(parts) < 2:
            await event.respond('Некорректная команда. Пример: /chat_remove chat_id')
            return

        chat_id = parts[1]
        if chat_id in chat_ids:
            chat_ids.remove(chat_id)
            await event.respond(f'Чат {chat_id} удален из списка.')
            save_chat_ids_to_file()  # Сохраняем изменения в файл
        else:
            await event.respond(f'Чат {chat_id} не найден в списке.')
    elif command.startswith('/message'):
        await event.respond('Введите текст рассылки.')
        # Обработка текста рассылки
        @bot_client.on(events.NewMessage(incoming=True))
        async def handle_message(event):
            message_text = event.text
            for chat_id in chat_ids:
                await send_message(client_1, chat_id, message_text)
                await send_message(client_2, chat_id, message_text)
            await event.respond('Рассылка выполнена.')
    elif command == '/login':
        await event.respond('Введите данные для авторизации аккаунтов (номер телефона и код).')
        # Обработка авторизации аккаунтов
        @bot_client.on(events.NewMessage(incoming=True))
        async def handle_login(event):
            login_data = event.text
            try:
                # Разделение данных на номер телефона и код
                phone, code = login_data.split()
                # Авторизация первого аккаунта
                await client_1.send_code_request(phone)
                await client_1.sign_in(phone, code)
                # Авторизация второго аккаунта
                await client_2.send_code_request(phone)
                await client_2.sign_in(phone, code)
                await event.respond('Авторизация выполнена.')
            except Exception as e:
                await event.respond(f'Ошибка авторизации: {str(e)}')
    else:
        await event.respond('Неизвестная команда')

def register_handlers(bot_client):
    bot_client.add_event_handler(handle_command, events.NewMessage(incoming=True))

# Функция для сохранения ID чатов в файл
def save_chat_ids_to_file():
    with open('groups.txt', 'w') as file:
        for chat_id in chat_ids:
            file.write(f'{chat_id}\n')

# Функция для чтения ID чатов из файла
def read_chat_ids_from_file():
    chat_ids = []
    if os.path.exists('groups.txt'):
        with open('groups.txt', 'r') as file:
            for line in file:
                chat_ids.append(line.strip())
    return chat_ids
