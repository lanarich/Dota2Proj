
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram import Router, F, Bot
from state.hero_prediction import PredictionState
from keyboards.predict_hero_kb import TeamData, build_attribute_select_kb, HeroAttributeData, build_hero_select_kb, HeroData, build_main_kb, build_pick_kb, Pagination, build_slot_select_kb

from aiogram.enums.parse_mode import ParseMode


router_pick = Router()

def generate_message_text(data):
    heroes = data['Allies']
    enemy_heroes = data['Enemies']
    
    return (
        '😇 *Ваша команда* 😇\n\n'
        '==========================================\n'
        f'[[{heroes.get("hero1", "Герой 1")}]] [[{heroes.get("hero2", "Герой 2")}]] [[{heroes.get("hero3", "Герой 3")}]] [[{heroes.get("hero4", "Герой 4")}]] [[{heroes.get("hero5", "Герой 5")}]]\n'
        '==========================================\n\n'
        '😈 *Команда противников* 😈\n\n'
        '==========================================\n'
        f'[[{enemy_heroes.get("hero1", "Герой 1")}]] [[{enemy_heroes.get("hero2", "Герой 2")}]] [[{enemy_heroes.get("hero3", "Герой 3")}]] [[{enemy_heroes.get("hero4", "Герой 4")}]] [[{enemy_heroes.get("hero5", "Герой 5")}]]\n'
        '==========================================\n'
    )

@router_pick.message(F.text == "🥠 Предсказать персонажа M1 🥠")
async def main_table(message: Message, bot: Bot, state: FSMContext):
    await state.set_state(PredictionState.heroes)
    await state.update_data(Allies={'hero1': 'Герой 1', 'hero2': 'Герой 2', 'hero3': 'Герой 3', 'hero4': 'Герой 4', 'hero5': 'Герой 5'},
                            Enemies={'hero1': 'Герой 1', 'hero2': 'Герой 2', 'hero3': 'Герой 3', 'hero4': 'Герой 4', 'hero5': 'Герой 5'})
    data = await state.get_data()
    await bot.send_message(message.from_user.id, generate_message_text(data), reply_markup=build_main_kb(), parse_mode=ParseMode.MARKDOWN)

@router_pick.callback_query(Pagination.filter(F.action == 'pick'))
async def process_pick(call: CallbackQuery):
    await call.answer()
    await call.message.edit_reply_markup(reply_markup=build_pick_kb())

@router_pick.callback_query(Pagination.filter(F.action == 'delete'))
async def delete_information(call: CallbackQuery, state: FSMContext):
    await state.update_data(Allies={'hero1': 'Герой 1', 'hero2': 'Герой 2', 'hero3': 'Герой 3', 'hero4': 'Герой 4', 'hero5': 'Герой 5'},
                            Enemies={'hero1': 'Герой 1', 'hero2': 'Герой 2', 'hero3': 'Герой 3', 'hero4': 'Герой 4', 'hero5': 'Герой 5'})
    data = await state.get_data()
    await call.message.edit_text(generate_message_text(data), reply_markup=build_main_kb(), parse_mode=ParseMode.MARKDOWN)
    await call.answer("Информация очищена.")

@router_pick.callback_query(Pagination.filter(F.action == 'add_friend'))
async def add_friend(call: CallbackQuery):
    await call.answer()
    await call.message.edit_reply_markup(reply_markup=build_slot_select_kb('Allies'))

@router_pick.callback_query(Pagination.filter(F.action == 'add_enemy'))
async def add_enemy(call: CallbackQuery):
    await call.answer()
    await call.message.edit_reply_markup(reply_markup=build_slot_select_kb('Enemies'))

@router_pick.callback_query(Pagination.filter(F.action == 'delete_friend'))
async def delete_friend(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    for i in range(1, 6):
        data['Allies'][f'hero{i}'] = f'Герой {i}'
    await state.update_data(data)
    await call.message.edit_text(generate_message_text(data), reply_markup=build_main_kb(), parse_mode=ParseMode.MARKDOWN)
    await call.answer("Союзники удалены.")

@router_pick.callback_query(Pagination.filter(F.action == 'delete_enemy'))
async def delete_enemy(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    for i in range(1, 6):
        data['Enemies'][f'hero{i}'] = f'Герой {i}'
    await state.update_data(data)
    await call.message.edit_text(generate_message_text(data), reply_markup=build_main_kb(), parse_mode=ParseMode.MARKDOWN)
    await call.answer("Противники удалены.")

@router_pick.callback_query(Pagination.filter(F.action =='back_main_page'))
async def back_to_main(call: CallbackQuery):
    await call.answer()
    await call.message.edit_reply_markup(reply_markup=build_main_kb())


@router_pick.callback_query(TeamData.filter(F.action == 'select'))
async def select_attribute(call: CallbackQuery, callback_data: TeamData):
    await call.answer()
    await call.message.edit_reply_markup(reply_markup=build_attribute_select_kb(callback_data.team, callback_data.position))

@router_pick.callback_query(HeroAttributeData.filter())
async def select_hero(call: CallbackQuery, callback_data: HeroAttributeData):
    if callback_data.attribute:
        await call.answer()
        await call.message.edit_reply_markup(reply_markup=build_hero_select_kb(callback_data.attribute, callback_data.team, callback_data.position))
    else:
        await call.answer()
        await call.message.edit_reply_markup(reply_markup=build_attribute_select_kb(callback_data.team, callback_data.position))

@router_pick.callback_query(HeroData.filter())
async def confirm_hero_selection(call: CallbackQuery, callback_data: HeroData, state: FSMContext):
    data = await state.get_data()
    data[callback_data.team][f'hero{callback_data.position}'] = callback_data.name
    await state.update_data(data)
    await call.message.edit_text(generate_message_text(data), reply_markup=build_main_kb(), parse_mode=ParseMode.MARKDOWN)
    await call.answer(f"Герой {callback_data.name} выбран для позиции {callback_data.position} в команде {callback_data.team}.")