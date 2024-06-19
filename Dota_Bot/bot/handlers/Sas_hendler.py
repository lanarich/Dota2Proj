from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
import torch
from utils.SasModel import SASRec
from state.hero_prediction import PredictionState
from utils.dictionary import heroes_strengh, heroes_agility, heroes_intelligence, heroes_universal
from utils.corrected_heroes_id import corrected_heroes_id
from utils.corrected_heroes_id_for_responce import corrected_heroes_id_for_responce
from keyboards.predict_hero_kb import build_main_kb

from aiogram.enums.parse_mode import ParseMode

from keyboards.predict_hero_kb import Pagination

router_sas = Router()

NUM_HEROES = 124
embed_dim = 64
num_heads = 1
num_layers = 1
model = SASRec(NUM_HEROES, embed_dim, num_heads, num_layers)
model.load_state_dict(torch.load('utils\seq_rec_model'))
model.eval()

def convert_to_ids(heroes, hero_to_id):
    return [hero_to_id.get(hero, 0) for hero in heroes]

def check_sequence(ids):
    found_zero = False
    for hero_id in ids:
        if hero_id == 0:
            found_zero = True
        elif found_zero:
            return False
    return True

def get_new_index(hero_id, heroes_mapping):
    return heroes_mapping.get(hero_id, 0)

id_to_hero = {v: k for k, v in corrected_heroes_id_for_responce.items()}

def generate_message_text(data, top_heroes_names):
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
        '==========================================\n\n'
        f'*Топ 5* рекомендованных героев для следующего пика:\n\n {top_heroes_names}'
    )

@router_sas.callback_query(Pagination.filter(F.action == 'predict'))
async def predict_pick(call: CallbackQuery, state: FSMContext):
    await state.set_state(PredictionState)
    data = await state.get_data()
    hero_to_id = heroes_strengh | heroes_agility | heroes_intelligence | heroes_universal
    allies_ids = convert_to_ids(data['Allies'].values(), hero_to_id)
    enemies_ids = convert_to_ids(data['Enemies'].values(), hero_to_id)
    
    allies_new_ids = [get_new_index(hero_id, corrected_heroes_id) for hero_id in allies_ids]
    enemies_new_ids = [get_new_index(hero_id, corrected_heroes_id) for hero_id in enemies_ids]

    if len(allies_new_ids) < 5:
        allies_new_ids.extend([0] * (4 - len(allies_ids)))
    if len(enemies_new_ids) < 5:
        enemies_new_ids.extend([0] * (4 - len(enemies_ids)))
        
    if not check_sequence(allies_new_ids) or not check_sequence(enemies_new_ids):
        await call.answer('Неправильная последовательность героев. Герои должны быть заполнены последовательно без пропусков.')
    
    else:
        allies_tensor = torch.tensor([allies_new_ids])
        enemies_tensor = torch.tensor([enemies_new_ids])
        pred = model(allies_tensor, enemies_tensor)
        top_heroes_indices = torch.topk(pred, 5)[1].tolist()[0]
        top_heroes_names = [id_to_hero[index] for index in top_heroes_indices]
        await call.message.edit_text(generate_message_text(data, top_heroes_names), reply_markup=build_main_kb(), parse_mode=ParseMode.MARKDOWN)