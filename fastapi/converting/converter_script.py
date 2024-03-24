import asyncio
import json

import pandas as pd

from api_requests.get_graphql_match import get_match_data, create_mongo_connection

mongo_client, mongo_db = create_mongo_connection()

dataframe_match_collection = mongo_db.test_match_df_coll

'''
Читаем вспомогательные файлы, такие как creeps_biuldings
'''


def utility_read_from_json(filename):
    with open(filename) as f:
        lines = f.read()
        return json.loads(lines)


'''
Просто чтобы было красивее
'''


def get_collection_attr(match, attr_name):
    return match['match'][attr_name]


'''
Основной файл для преобразования данных в датафрейм
'''


def convert_match_data_into_df(current_match_data):
    #  будущий массив всех строк матча
    single_match_decomposition = []
    basic_attrs = ['id', 'didRadiantWin', 'durationSeconds', 'startDateTime',
                   'firstBloodTime', 'gameMode']
    df_dict = {}
    #  добавляем общие аттрибуты
    for attr in basic_attrs:
        df_dict[attr] = get_collection_attr(current_match_data, attr)

    #  массив, по которому будем считать количество минут
    radiantNetworthLeads = get_collection_attr(current_match_data, 'radiantNetworthLeads')

    #  читаем постройки и заполняем единицами, потому что сначала они все целы
    tower_utils = utility_read_from_json('../creeps_buildings.json')
    for npc in tower_utils:
        df_dict[npc['name']] = 1

    #  теперь собираем статистику за каждую минуту
    for minute in range(len(radiantNetworthLeads[2:])):
        obj_dict = df_dict.copy()
        #  текущая минута
        obj_dict['currentMinute'] = minute + 1
        minuteRadiantNetworthLead = radiantNetworthLeads[minute]
        #  преимущество в золоте
        obj_dict['minuteRadiantNetworthLead'] = minuteRadiantNetworthLead
        minuteRadiantExperienceLeads = get_collection_attr(current_match_data, 'radiantExperienceLeads')[minute]
        #  преимущество в опыте
        obj_dict['minuteRadiantExperienceLeads'] = minuteRadiantExperienceLeads
        minuteRadiantKills = get_collection_attr(current_match_data, 'radiantKills')[minute]
        #  количество убийств свет
        obj_dict['minuteRadiantKills'] = minuteRadiantKills
        minuteDireKills = get_collection_attr(current_match_data, 'direKills')[minute]
        #  количество убийств тьма
        obj_dict['minuteDireKills'] = minuteDireKills
        #  функция, собирающая инфу по каждому игроку
        get_players_data(current_match_data, minute, obj_dict)
        #  читаем сломанные постройки

        get_tower_barracks_destroy_dict(get_collection_attr(current_match_data, 'towerDeaths'),
                                        minute, df_dict, tower_utils)
        single_match_decomposition.append(obj_dict)
        #update = {"$set": obj_dict}

        #result = dataframe_match_collection.update_one(obj_dict, update, upsert=True)

    return single_match_decomposition


def get_tower_barracks_destroy_dict(arr_tower_deaths, minute, obj_dict, tower_utils):
    npc_id = []
    for tower in arr_tower_deaths:
        if int(tower['time'] / 60) == minute:
            npc_id.append(tower['npcId'])
    for building in tower_utils:
        if building['id'] in npc_id:
            obj_dict[building['name']] = 0


def get_players_data(arr, minute, player_dict):
    players = get_collection_attr(arr, 'players')
    for player in players:
        if player['isRadiant']:
            single_player_data(player_dict, minute, player, "radiant_", player['position'])
        else:
            single_player_data(player_dict, minute, player, "dire_", player['position'])


def single_player_data(player_dict, minute, player, side, pos):
    player_dict[side + pos + '_id'] = player['steamAccount']['id']
    player_dict[side + pos + '_seasonRank'] = player['steamAccount']['seasonRank']
    if 'seasonLeaderboardRank' in player['steamAccount']:
        player_dict[side + pos + '_seasonLeaderboardRank'] = player['steamAccount']['seasonLeaderboardRank']
    else:
        player_dict[side + pos + '_seasonLeaderboardRank'] = 0
    player_dict[side + pos + '_hero_id'] = player['hero']['id']
    player_dict[side + pos + '_leaverStatus'] = player['leaverStatus']
    player_dict[side + pos + '_position'] = player['position']
    player_dict[side + pos + '_intentionalFeeding'] = player['intentionalFeeding']
    player_dict[side + pos + '_isRadiant'] = player['isRadiant']
    player_dict[side + pos + '_LastHitsPerMinute'] = player['stats']['lastHitsPerMinute'][minute]
    player_dict[side + pos + '_GoldPerMinute'] = player['stats']['goldPerMinute'][minute]
    player_dict[side + pos + '_ExperiencePerMinute'] = player['stats']['experiencePerMinute'][minute]
    player_dict[side + pos + '_HealPerMinute'] = player['stats']['healPerMinute'][minute]
    player_dict[side + pos + '_HeroDamagePerMinute'] = player['stats']['heroDamagePerMinute'][minute]
    player_dict[side + pos + '_TowerDamagePerMinute'] = player['stats']['towerDamagePerMinute'][minute]
    player_dict[side + pos + '_ActionsPerMinute'] = player['stats']['actionsPerMinute'][minute]
    #  Статы, которых нет в базовой модели
    # player_dict[side + pos + '_attackType'] = player['hero']['stats']['attackType']
    # player_dict[side + pos + '_startingArmor'] = player['hero']['stats']['startingArmor']
    # player_dict[side + pos + '_startingDamageMin'] = player['hero']['stats']['startingDamageMin']
    # player_dict[side + pos + '_startingDamageMax'] = player['hero']['stats']['startingDamageMax']
    # player_dict[side + pos + '_attackRate'] = player['hero']['stats']['attackRate']
    # player_dict[side + pos + '_attackAnimationPoint'] = player['hero']['stats']['attackAnimationPoint']
    # player_dict[side + pos + '_attackAcquisitionRange'] = player['hero']['stats']['attackAcquisitionRange']
    # player_dict[side + pos + '_attackRange'] = player['hero']['stats']['attackRange']
    # player_dict[side + pos + '_primaryAttribute'] = player['hero']['stats']['primaryAttribute']
    # player_dict[side + pos + '_strengthBase'] = player['hero']['stats']['strengthBase']
    # player_dict[side + pos + '_strengthGain'] = player['hero']['stats']['strengthGain']
    # player_dict[side + pos + '_intelligenceBase'] = player['hero']['stats']['intelligenceBase']
    # player_dict[side + pos + '_intelligenceGain'] = player['hero']['stats']['intelligenceGain']
    # player_dict[side + pos + '_agilityBase'] = player['hero']['stats']['agilityBase']
    # player_dict[side + pos + '_agilityGain'] = player['hero']['stats']['agilityGain']
    # player_dict[side + pos + '_moveSpeed'] = player['hero']['stats']['moveSpeed']

    # for item in range(6):
    # if player['stats']['inventoryReport'][minute]['item' + str(item)] is not None:
    # player_dict[side + pos + '_item_' + str(item)] = \
    # player['stats']['inventoryReport'][minute]['item' + str(item)]['itemId']
    # else:
    # player_dict[side + pos + '_item_' + str(item)] = 0

    # for backpack_item in range(3):
    # if player['stats']['inventoryReport'][minute]['backPack' + str(backpack_item)] is not None:
    # player_dict[side + pos + '_backpack_' + str(backpack_item)] = \
    # player['stats']['inventoryReport'][minute]['backPack' + str(backpack_item)]['itemId']
    # else:
    # player_dict[side + pos + '_backpack_item_' + str(backpack_item)] = 0

    # if player['stats']['inventoryReport'][minute]['neutral0'] is not None:
    # player_dict[side + pos + '_neutral0'] = \
    # player['stats']['inventoryReport'][minute]['neutral0']['itemId']
    # else:
    # player_dict[side + pos + '_neutral0'] = 0


def check_for_presence_in_db(match_id):
    # получаем айдишники в первый раз
    doc = dataframe_match_collection.find({"id": match_id})
    return list(doc)


def get_decomposed_match_data(match_id):
    doc = check_for_presence_in_db(match_id)
    if len(doc) < 1:
        single_match = asyncio.run(get_match_data(match_id))
        return convert_match_data_into_df(single_match)
    else:
        return doc


def create_dataframe(converted_match_data):
    match_df = pd.DataFrame(data=converted_match_data)
    print(match_df)
    return match_df
