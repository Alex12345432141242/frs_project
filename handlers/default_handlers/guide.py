import os

from telebot.types import CallbackQuery, Message

from data.peterhof import ATTRACTIONS, PETERHOF_ASSETS_DIR, PETERHOF_MAP_PATH
from keyboards.inline.guide import attractions_keyboard, places_keyboard
from loader import bot

PLACES_TEXT = "📍 Выберите место, для которого хотите открыть путеводитель:"
PETERHOF_CAPTION = (
    "🏛 Нижний парк Петергофа\n\n"
    "Перед вами карта Нижнего парка. "
    "Выберите достопримечательность, о которой хотите узнать:"
)
NEXT_ATTRACTION_TEXT = "Выберите другую достопримечательность:"


def send_places_menu(chat_id: int) -> None:
    bot.send_message(chat_id, PLACES_TEXT, reply_markup=places_keyboard())


def send_peterhof_guide(chat_id: int) -> None:
    if os.path.exists(PETERHOF_MAP_PATH):
        with open(PETERHOF_MAP_PATH, "rb") as map_file:
            bot.send_photo(chat_id, map_file)
    else:
        bot.send_message(chat_id, "Карта пока не добавлена.")

    bot.send_message(chat_id, PETERHOF_CAPTION, reply_markup=attractions_keyboard())


def send_attraction(chat_id: int, callback_data: str) -> None:
    attraction = ATTRACTIONS.get(callback_data)
    if attraction is None:
        bot.send_message(chat_id, "Эта достопримечательность пока недоступна.")
        return

    bot.send_message(
        chat_id,
        f"{attraction['title']}\n\n{attraction['text']}",
    )

    for photo_name in attraction.get("photos", []):
        photo_path = os.path.join(PETERHOF_ASSETS_DIR, photo_name)
        if not os.path.exists(photo_path):
            continue
        with open(photo_path, "rb") as photo_file:
            bot.send_photo(chat_id, photo_file)

    bot.send_message(
        chat_id,
        NEXT_ATTRACTION_TEXT,
        reply_markup=attractions_keyboard(),
    )


@bot.message_handler(commands=["guide"])
def bot_guide(message: Message) -> None:
    bot.delete_state(message.from_user.id, message.chat.id)
    send_places_menu(message.chat.id)


@bot.callback_query_handler(func=lambda call: call.data == "place_peterhof")
def peterhof_place_callback(call: CallbackQuery) -> None:
    bot.answer_callback_query(call.id)
    send_peterhof_guide(call.message.chat.id)


@bot.callback_query_handler(func=lambda call: call.data == "back_to_places")
def back_to_places_callback(call: CallbackQuery) -> None:
    bot.answer_callback_query(call.id)
    send_places_menu(call.message.chat.id)


@bot.callback_query_handler(func=lambda call: call.data in ATTRACTIONS)
def attraction_callback(call: CallbackQuery) -> None:
    bot.answer_callback_query(call.id)
    send_attraction(call.message.chat.id, call.data)
