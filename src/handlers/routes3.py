from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
import aiohttp
from typing import TypedDict, Required


class Product(TypedDict, total=False):
    id: Required[int]
    title: str
    price: float
    description: str
    category: str


router = Router()


async def get_product(product_id: int) -> Product | None:
    url = f"https://fakestoreapi.com/products/{product_id}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                return await resp.json()
            else:
                return None


def display_product(product: Product) -> str:
    return (
        f"<b>Информация по найденному товару:</b>\n"
        f"ID: {product.get("id")}\n"
        f"Название: <i>{product.get('title', 'Без названия.')}</i>\n"
        f"Цена: <i>{product.get('price', 'Не указана.')} $</i>\n"
        f"Описание: <i>{product.get('description', 'Не указано.')}</i>\n"
        f"Категория: <i>{product.get('category', 'Не указана.')}</i>\n"
    )


@router.message(Command("start"))
async def start(message: Message):
    await message.answer(
        "Привет!👋 Это <b>BotMater</b>!👩‍🍼 Приступим к работе!👩‍🏭\n"
        "Напиши /product ID\n"
        "Example: <b>/product 1</b>",
        parse_mode="HTML",
    )


@router.message(Command("product"))
async def get_product_cmd(message: Message):
    parts = message.text.strip().split()
    product_id = parts[-1]

    if len(parts) != 2:
        await message.answer(
            "Некорректный ввод! Используйте: /product ID. Example: <b>/product 1</b>",
            parse_mode="HTML",
        )
    elif not product_id.isdigit():
        await message.answer(
            "Некорректный ввод! Используйте: /product ID. Example: <b>/product 1</b>",
            parse_mode="HTML",
        )
    else:
        await message.answer(f"Ищу товар с id: {product_id}")

    try:
        product = await get_product(int(product_id))
    except Exception as e:
        await message.answer(f"Ошибка подключения к серверу! {e}")
    else:
        if product is None:
            await message.answer(f"Товара с ID: {product_id} не найдено!")
        else:
            await message.answer(
                display_product(product),
                parse_mode="HTML",
            )
