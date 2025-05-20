from process_new_post import process_new_post
from telethon import TelegramClient
from dotenv import load_dotenv
import asyncio
import os
import threading
import random

# Замените на свои API ID и API Hash
load_dotenv()
api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")

channel_username = "RKadyrov_95"  

# ==== Флаг паузы ====
paused = False
stop_signal = False
stop_program = False

def get_random_sleep_time():
    """
    Возвращает случайное время ожидания от 30 минут до 1,5 часа в секундах.
    """
    return random.randint(15*60, 60*60)

# ==== Командный ввод ====
def input_listener():
    global paused, stop_signal, stop_program
    while True:
        command = input().strip().lower()
        if command == "p":
            paused = True
            print("⏸️ Скрипт поставлен на паузу.")
        elif command == "r":
            paused = False
            print("▶️ Скрипт возобновлён.")
        elif command == "q":
            stop_program = True
            print("⛔ Скрипт завершён по команде.")
            break


async def main(channel_username):
    client = TelegramClient('session_name', api_id, api_hash)
    await client.start()
    channel = await client.get_entity(channel_username)

    while not stop_program:
        if paused:
            await asyncio.sleep(1)
            continue

        print("📡 Поиск последнего поста... \n Команды: [p] — пауза, [r] — продолжить, [q] — выход")

        async for message in client.iter_messages(channel, limit=1):
            print(f"🔄 Последний пост ID {message.id}")
            await process_new_post(client, channel, message)
            break  # только первый (последний) пост

        print("⏳ Ожидание до следующего комментария...")
        await asyncio.sleep(get_random_sleep_time()) # ожидание от 30 минут до 1,5 часа

if __name__ == "__main__":
    threading.Thread(target=input_listener, daemon=True).start()
    asyncio.run(main(channel_username))