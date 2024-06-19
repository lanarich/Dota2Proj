from aiogram.fsm.state import StatesGroup, State


class PredictionState(StatesGroup):
    heroes = State()
    bans = State()
    selecting_attribute = State()
    selecting_hero = State()
