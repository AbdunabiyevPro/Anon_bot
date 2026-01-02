import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from states import Language_State, ChatState, AnonState
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

logging.basicConfig(level=logging.INFO)
TOKEN = "8540365444:AAHUspCNh31XP25BYoNNvoHafrugwKuZ47Y"

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)


@dp.message(Command("start"))
async def second_handler(message: types.Message, state: FSMContext):
    args = message.text.split()
    if len(args) > 1:
        receiver_id = args[1]
        await state.update_data(target_id=receiver_id)
        await state.set_state(ChatState.waiting_for_msg)
        await message.answer(
            "Вы можете отправить анонимное сообщение. Напишите свой текст ниже личные данные не сохраняются.")

    else:
        bot_info = await bot.get_me()
        user_id = message.from_user.id
        my_link = f"https://t.me/{bot_info.username}?start={user_id}"

        text = (f"Здравствуйте, {message.from_user.full_name}!\n\n"
                f"Ваша личная ссылка:\n{my_link}\n\n"
                f"Разместите эту ссылку на своём канале или в профиле. "
                f"Если кто-то напишет вам, я передам сообщение вам!")
        await message.answer(text, parse_mode="HTML")


@dp.message(ChatState.waiting_for_msg)
async def forward_message(message: types.Message, state: FSMContext):
    data = await state.get_data()
    target_id = data.get("target_id")
    sender = message.from_user
    reply_markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Ответить ✍️", callback_data=f"reply_{message.from_user.id}")]
    ])

    info = (f"📩 <b>новое сообщение!</b>\n\n"
            f"👤 <b>кого:</b> {sender.full_name}\n"
            f"🔗 <b>Имя пользователя:</b> @{sender.username if sender.username else 'Mavjud emas'}\n"
            f"🆔 <b>ID:</b> <code>{sender.id}</code>\n\n"
            f"💬 <b>сообщение:</b> {message.text}")

    try:
        await bot.send_message(target_id, info, reply_markup=reply_markup, parse_mode="HTML")
        await message.answer("Ваше сообщение доставлено! ✅")
        await state.clear()
    except Exception:
        await message.answer("Xatolik! Bu foydalanuvchi botni bloklagan bo'lishi mumkin.")
        await state.clear()


@dp.callback_query(F.data.startswith("reply_"))
async def ask_reply(call: types.CallbackQuery, state: FSMContext):
    user_id = call.data.split("_")[1]

    await state.update_data(reply_to_id=user_id)

    await state.set_state(AnonState.waiting_for_reply)

    await call.message.answer("Напишите ваш ответ:")
    await call.answer()


@dp.message(AnonState.waiting_for_reply)
async def send_reply(message: types.Message, state: FSMContext):
    data = await state.get_data()
    target_id = data.get("reply_to_id")

    try:
        await bot.send_message(target_id, f"📩 <b>Вам пришёл ответ:</b>\n\n{message.text}", parse_mode="HTML")
        await message.answer("Ваш ответ доставлен! ✅ ✅")
    except Exception:
        await message.answer("Xatolik! Foydalanuvchi botni bloklagan bo'lishi mumkin.")

    await state.clear()


async def main():
    print("Bot ishga tushdi...")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot to'xtatildi!")
