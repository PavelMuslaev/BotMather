from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import (
    Message,
    CallbackQuery,
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)


router = Router()


def get_main_reply_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="/about_us")],
            [KeyboardButton(text="/start"), KeyboardButton(text="/help")],
        ],
        resize_keyboard=True,
    )

    return keyboard


def get_main_inline_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Открыть сайт", url="https://nastya.loxic.com")],
            [InlineKeyboardButton(text="Подробнее", callback_data="info_more")],
        ]
    )

    return keyboard


@router.callback_query(lambda q: q.data == "info_more")
async def info_more(callback: CallbackQuery):
    await callback.message.answer("Вот более подробная информация...")
    await callback.answer()


@router.message(Command("start"))
@router.message(F.text.lower() == "старт")
async def start(message: Message):
    await message.answer(
        "Привет!👋 Это *BotMater*!👩‍🍼 Приступим к работе!👩‍🏭\n"
        "Напиши /help для помощи!💁‍♀️",
        parse_mode="Markdown",
    )


@router.message(Command("help"))
async def help(message: Message):
    await message.answer(
        "Команды:\n"
        "<b>/start</b> - запустить бота;\n"
        "<b>/help</b> - список команд;\n"
        "<b>/about_us</b> - про нас;\n",
        parse_mode="HTML",
    )


@router.message(Command("about_us"))
async def about_us(message: Message):
    await message.answer(
        f"Мы команда BotMater! Наша главная задача XXXX.\n"
        f"Нам очень приятно, <i>{message.from_user.first_name}</i>, что Вы с нами!\n\n"
        f"Ссылка на наш сайт: <a href='https://nastya.loxic.com'>https://nastya.loxic.com</a>",
        parse_mode="HTML",
        reply_markup=get_main_inline_keyboard(),
    )


@router.message()
async def all_messages(message):
    await message.answer("<b><i>Такая команда не найдена!</i></b>", parse_mode="HTML")
