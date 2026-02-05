from aiogram import Bot, Dispatcher, executor, types
import time
import os

TOKEN = os.environ.get("8266204920:AAGmiHhMiwV88oYBGJgubnalGm4g1PFLOS8")
PASSWORD = "F6h0Ksu1Nm₽"

MAX_ATTEMPTS = 5
BLOCK_TIME = 10 * 60 * 60

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

users = {}

def get_user(user_id):
    if user_id not in users:
        users[user_id] = {
            "attempts": 0,
            "blocked_until": 0,
            "access": False
        }
    return users[user_id]

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    user = get_user(message.from_user.id)
    now = time.time()

    if user["blocked_until"] > now:
        await message.answer("⛔ Блокировка. Попробуйте позже.")
        return

    if user["access"]:
        await message.answer("✅ Доступ уже есть")
    else:
        await message.answer("🔐 Введите пароль:")

@dp.message_handler()
async def check(message: types.Message):
    user = get_user(message.from_user.id)
    now = time.time()

    if user["access"]:
        return

    if user["blocked_until"] > now:
        await message.answer("⛔ Слишком много попыток. Ждите.")
        return

    if message.text == PASSWORD:
        user["access"] = True
        user["attempts"] = 0
        await message.answer("✅ Пароль верный. Доступ открыт")
    else:
        user["attempts"] += 1
        if user["attempts"] >= MAX_ATTEMPTS:
            user["blocked_until"] = now + BLOCK_TIME
            user["attempts"] = 0
            await message.answer("⛔ 5 ошибок. Блок на 10 часов.")
        else:
            await message.answer("❌ Неверный пароль")

if __name__ == "__main__":
    executor.start_polling(dp)
