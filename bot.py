import asyncio
import logging

from aiogram import Bot, Dispatcher, Router, types, F
from aiogram.filters import Command, CommandObject, Text
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from config_reader import config
from sqlite import db_start, create_profile, edit_profile


async def on_startup(_):
    await db_start()


bot = Bot(token=config.bot_token.get_secret_value(), parse_mode="HTML")
rt = Router()


@rt.message(Command("start"))
async def start(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="Да!",
        callback_data="Да")
    )
    builder.add(types.InlineKeyboardButton(
        text="Нет(",
        callback_data="Нет")
    )
    await message.answer(
        "Хочешь быть вешалкой?",
        reply_markup=builder.as_markup()
    )
    kb = [
        [types.KeyboardButton(text="Узнать об  отряде!")],
        [types.KeyboardButton(text="5 причин почему отряд не нравится тимлиду")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb)
    await message.answer("Хочешь узнать больше?", reply_markup=keyboard)

    await create_profile(user_id=message.from_user.id)


@rt.message(Text("5 причин почему отряд не нравится тимлиду"))
async def inf(message: types.Message):
    await message.answer("1. Горят дедлайны 2.Дедлайны горят 3. Антон дебик 4. Миша выздоравливай)",
                         reply_markup=types.ReplyKeyboardRemove())


@rt.callback_query(Text("Да"))
async def send_random_value(callback: types.CallbackQuery):
    await callback.message.answer("Отлично!")
    await callback.answer(
        text="Спасибо за ответ!",
        show_alert=True
    )


@rt.callback_query(Text("Нет"))
async def send_random_value(callback: types.CallbackQuery):
    await callback.message.answer("Миша доволен")
    await callback.answer(
        text="Но Леха больше!",
        show_alert=True
    )


@rt.message(F.animation)
async def echo_gif(message: types.Message):
    await message.reply_animation(message.animation.file_id)


@rt.message(F.photo)
async def download_photo(message: types.Message, bot: Bot):
    await bot.download(
        message.photo[-1],
        destination=f"D:/Work/{message.photo[-1].file_id}.jpg")

async def main():
    dp = Dispatcher()
    dp.include_router(rt)
    await dp.start_polling(bot, on_startup=on_startup)


if __name__ == "__main__":
    asyncio.run(main())
