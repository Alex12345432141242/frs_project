from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


def places_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton(
            text="🏛 Нижний парк Петергофа",
            callback_data="place_peterhof",
        )
    )
    return keyboard


def attractions_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=2)
    buttons = [
        InlineKeyboardButton(text="🏛 Большой дворец", callback_data="attraction_palace"),
        InlineKeyboardButton(text="💧 Большой каскад", callback_data="attraction_cascade"),
        InlineKeyboardButton(text="🦁 Самсон", callback_data="attraction_samson"),
        InlineKeyboardButton(text="⛲ Фонтан «Адам»", callback_data="attraction_adam"),
        InlineKeyboardButton(text="⛲ Фонтан «Ева»", callback_data="attraction_eve"),
        InlineKeyboardButton(text="🏠 Монплезир", callback_data="attraction_monplaisir"),
        InlineKeyboardButton(text="🏡 Дворец Марли", callback_data="attraction_marli"),
        InlineKeyboardButton(text="🏛 Колоннады", callback_data="attraction_voronikhin"),
        InlineKeyboardButton(text="🐉 Шахматная гора", callback_data="attraction_chess"),
        InlineKeyboardButton(text="✨ Золотая гора", callback_data="attraction_gold"),
        InlineKeyboardButton(text="🏺 Римские фонтаны", callback_data="attraction_roman"),
        InlineKeyboardButton(text="🌊 Финский залив", callback_data="attraction_gulf"),
    ]
    keyboard.add(*buttons)
    keyboard.add(
        InlineKeyboardButton(
            text="⬅️ Назад к местам",
            callback_data="back_to_places",
        )
    )
    return keyboard
