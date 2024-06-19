from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram import Router, F, Bot
from aiogram.enums.parse_mode import ParseMode
from keyboards.stats_kb import stats_kb
from keyboards.predict_item_kb import predict_item_keyboard
from state.als import PredictionALS
from utils.ALS import als_predict_heroes


router_als = Router()

@router_als.message(F.text == "🌐 Предсказать персонажа M2 🌐")
async def previews_kb(message: Message, bot: Bot, state: FSMContext):
    await bot.send_message(message.from_user.id, 'Введите Ваш Steam id:')
    await state.set_state(PredictionALS.waiting_id)
    
@router_als.message(PredictionALS.waiting_id)
async def prediction_match(message: Message, state: FSMContext):
    hero_id, rating = als_predict_heroes(int(message.text))
    print(hero_id, rating)
    await state.set_state(None)
