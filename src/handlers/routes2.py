from aiogram.filters import Command
from aiogram import Router, F
from aiogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
    FSInputFile,
)
from aiogram.fsm.context import FSMContext
from aiogram import Bot

from src.forms.user import Form

router = Router()

@router.message(Command('cancel'))
async def cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Анкета окончена!")

@router.message(Command('start'))
async def start(message: Message, state: FSMContext):
    await message.answer("Давайте начнем заполнять анкету!\nСперва введите ваше имя:")
    await state.set_state(Form.name)

@router.message(Form.name, F.text)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Отлично!\nПродолжим, введите возраст:")
    await state.set_state(Form.age)

@router.message(Form.age, F.text)
async def process_age(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Возраст должен быть числом!")
    elif int(message.text) < 1 or int(message.text) > 100:
        await message.answer("Возраст должен быть от 0 до 100!")
    else:
        await state.update_data(age=int(message.text))
        await message.answer("Отлично!\nПродолжим, введите email:")
        await state.set_state(Form.email)

@router.message(Form.email, F.text)
async def process_email(message: Message, state: FSMContext):
    email_text = message.text
    if "@" not in email_text or "." not in email_text:
        await message.answer("Email некорректен!")
    else:
        await state.update_data(email=email_text)
        data = await state.get_data()
        await message.answer(f"Отлично! Мы зарегистрировали Вас!\n"
                             f"Имя: {data['name']}. Возраст: {data['age']}. Почта: {data['email']}.")
        await state.clear()


@router.message(F.photo)
async def process_photo(message: Message):
    photo = message.photo[-1]
    file_id = photo.file_id
    file_size = photo.file_size

    await message.answer_photo(
        file_id,
        caption=f"Вы отправили фото:\n"
            f"Id photo: <code>{file_id}</code>\n"
            f"Size photo: <code>{file_size}</code>\n",
        parse_mode="HTML"
    )


@router.message(F.video)
async def process_video(message: Message):
    video = message.video
    file_id = video.file_id
    duration = video.duration

    await message.answer_video(
        file_id,
        caption=f"Вы отправили видео:\n"
                f"Id video: <code>{file_id}</code>\n"
                f"Duration video: <code>{duration}</code>\n",
        parse_mode="HTML"
    )

@router.message(F.animation)
async def process_video(message: Message):
    animation = message.animation

    await message.answer_animation(
        animation.file_id,
        caption=f"Вы отправили анимацию:\n"
    )

@router.message(F.document)
async def process_video(message: Message, bot: Bot):
    doc = message.document
    file_id = doc.file_id

    file = await bot.get_file(file_id)
    file_path = file.file_path

    local_path = f"downloads/{doc.file_name}"

    await bot.download_file(file_path=file_path, destination=local_path)
    await message.answer("Файл сохранен!")


@router.message(Command('file'))
async def send_file(message: Message):
    file = FSInputFile('files/example.txt')
    await message.answer_document(file)