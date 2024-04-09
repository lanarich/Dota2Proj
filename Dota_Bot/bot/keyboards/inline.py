from aiogram.utils.keyboard import InlineKeyboardBuilder


def place_kb():
    kb = InlineKeyboardBuilder()
    kb.button(text="🌟", callback_data="set:1")
    kb.button(text="🌟🌟", callback_data="set:2")
    kb.button(text="🌟🌟🌟", callback_data="set:3")
    kb.button(text="🌟🌟🌟🌟", callback_data="set:4")
    kb.button(text="🌟🌟🌟🌟🌟", callback_data="set:5")
    kb.adjust(1)
    return kb.as_markup()
