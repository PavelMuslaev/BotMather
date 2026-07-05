from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
import aiosqlite
from os import getenv
from dotenv import load_dotenv

router = Router()

# ---
load_dotenv()
DB_NAME = getenv("DB_NAME")


async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                age INTEGER);
            """
        )
        await db.commit()


async def add_user(username, age):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            """
            INSERT INTO users (username, age) VALUES (?, ?);
            """,
            (username, age),
        )
        await db.commit()


async def get_users():
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("""
            SELECT * FROM users;
        """)
        print(cursor)
        print(cursor.fetchall())
        users = await cursor.fetchall()

    return users


# ---


@router.message(Command('start'))
async def start(message: Message):
    await init_db()
    await message.answer(
        "Привет!👋 Это <b>BotMater</b>!👩‍🍼 Приступим к работе!👩‍🏭\n"
        "Напиши /reg AGE - регистрация пользователя.\n"
        "Пример: <b>/reg 22</b>",
        parse_mode="HTML",
    )


@router.message(Command('reg'))
async def reg(message: Message):
    cmd = message.text.strip().split()
    age = cmd[-1]

    if len(cmd) != 2:
        await message.answer("Команда введена неверно!")
    elif not age.isdigit():
        await message.answer("Возраст должен быть числом!")
    else:
        await add_user(message.from_user.full_name, int(age))

        await message.answer("Всё готово!")


@router.message(Command('users'))
async def users(message: Message):
    users = await get_users()

    if not users:
        await message.answer("В базе нет пользователей!")
    else:
        text = "Пользователи в базе:\n\n"
        for user in users:
            text += f"<code>{user}</code>\n"

        await message.answer(text, parse_mode="HTML")