from aiogram.fsm.state import StatesGroup, State


class PredictionALS(StatesGroup):
    waiting_id = State()