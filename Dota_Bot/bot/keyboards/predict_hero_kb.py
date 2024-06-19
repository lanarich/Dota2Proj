from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData
from utils.dictionary import heroes_strengh, heroes_agility, heroes_intelligence, heroes_universal

class Pagination(CallbackData, prefix = 'pag'):
    action:str
    
class TeamData(CallbackData, prefix="team"):
    action: str
    position: int
    team: str
    
class HeroAttributeData(CallbackData, prefix="attr"):
    attribute: str
    team: str
    position: int
    
class HeroData(CallbackData, prefix="hero"):
    name: str
    team: str
    position: int


def build_main_kb():
    kb = InlineKeyboardBuilder()
    kb.button(text='Пики героев', callback_data=Pagination(action='pick').pack())
    kb.button(text='Предсказать следующего персонажа', callback_data=Pagination(action='predict').pack())
    kb.button(text='Очистить информацию', callback_data=Pagination(action='delete').pack())
    kb.adjust(1)
    return kb.as_markup()

def build_pick_kb():
    kb = InlineKeyboardBuilder()
    kb.button(text='Добавить союзника', callback_data=Pagination(action='add_friend').pack())
    kb.button(text='Добавить противника', callback_data=Pagination(action='add_enemy').pack())
    kb.button(text='Удалить союзника', callback_data=Pagination(action='delete_friend').pack())
    kb.button(text='Удалить противника', callback_data=Pagination(action='delete_enemy').pack())
    kb.button(text='◀️ Назад ◀️', callback_data=Pagination(action='back_main_page').pack())
    kb.adjust(2)
    return kb.as_markup()

def build_slot_select_kb(team: str):
    kb = InlineKeyboardBuilder()
    for i in range(1, 6):
        kb.button(text=f'Герой {i}', callback_data=TeamData(action='select', team=team, position=i).pack())
    kb.button(text='◀️ Назад ◀️', callback_data=Pagination(action='back_main_page').pack())
    kb.adjust(1)
    return kb.as_markup()


def build_attribute_select_kb(team: str, position: int):
    kb = InlineKeyboardBuilder()
    kb.button(text='Сила', callback_data=HeroAttributeData(attribute='strength', team=team, position=position).pack())
    kb.button(text='Ловкость', callback_data=HeroAttributeData(attribute='agility', team=team, position=position).pack())
    kb.button(text='Интеллект', callback_data=HeroAttributeData(attribute='intelligence', team=team, position=position).pack())
    kb.button(text='Универсал', callback_data=HeroAttributeData(attribute='universal', team=team, position=position).pack())
    kb.button(text='◀️ Назад ◀️', callback_data=Pagination(action='back_main_page').pack())
    kb.adjust(1)
    return kb.as_markup()

def build_hero_select_kb(attribute: str, team: str, position: int):
    kb = InlineKeyboardBuilder()
    
    hero_dict = {
        'strength': heroes_strengh,
        'agility': heroes_agility,
        'intelligence': heroes_intelligence,
        'universal': heroes_universal
    }

    heroes = hero_dict.get(attribute, {})
    for name, hero_id in heroes.items():
        kb.button(text=name, callback_data=HeroData(name=name, team=team, position=position).pack())
    
    kb.button(text='◀️ Назад ◀️', callback_data=Pagination(action='back_main_page').pack())
    kb.adjust(4)
    return kb.as_markup()