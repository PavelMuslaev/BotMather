import asyncio
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram import Bot

router = Router()

subscribers = set()

async def notifier(bot: Bot):
    while True:
        if subscribers:
            for user_id in subscribers:
                try:
                    await bot.send_message(user_id, "Муси-пуси!")
                except Exception:
                    pass
        await asyncio.sleep(0.5)


@router.message(Command('start'))
async def start(message: Message):
    await message.answer(
        "Привет!👋 Это <b>BotMater</b>!👩‍🍼 Я могу помочь с рассылкой!👩‍🏭\n"
        "/subscribe - подписаться на уведомления;\n"
        "/unsubscribe - отписка;\n"
        "/subscribers - список подписчиков.\n",
        parse_mode="HTML",
    )


@router.message(Command('subscribe'))
async def start(message: Message):
    subscribers.add(message.from_user.id)
    await message.answer(f"Добавили Вас в общую рассылку.")


@router.message(Command('unsubscribe'))
async def start(message: Message):
    subscribers.remove(message.from_user.id)
    await message.answer(f"Удалили Вас из общей рассылки.")


@router.message(Command('subscribers'))
async def start(message: Message):
    if not subscribers:
        await message.answer("Пока никого нет!")
    else:
        text = "Подписчики:\n"
        for user_id in subscribers:
            text += f"<b>{user_id}</b>\n"

        await message.answer(text)

