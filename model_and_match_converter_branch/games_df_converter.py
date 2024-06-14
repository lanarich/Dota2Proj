import pandas as pd
from tqdm import tqdm
from motor.motor_asyncio import AsyncIOMotorClient
import json
import pymongo.errors

from model_and_match_converter_branch.main import get_collection_attr, utility_read_from_json


def create_mongo_connection():
    try:
        # Менять соединение с монгой
        client = AsyncIOMotorClient("localhost", 27017)
        db = client.dota_db
        return client, db
    except pymongo.errors.ServerSelectionTimeoutError as err:
        print(err)

mongo_client, mongo_db = create_mongo_connection()
full_match = mongo_db.full_match_collection

async def read_main_match_data():
    single_match_decomposition = []
    #  массив общих признаков
    basic_attrs = ['id', 'didRadiantWin', 'durationSeconds', 'startDateTime',
                   'firstBloodTime', 'gameMode', 'barracksStatusRadiant', 'barracksStatusDire',
                   'towerStatusRadiant', 'towerStatusDire', 'firstBloodTime']
    doc_size = 0
    #  закомментировано то, что необходимо для работы с локальной монго
    less_then_full_match_id = 7451753118  # (await full_match.find_one())['_id']
    # arr = utility_read_from_json('dota_db.full_match_collection.json')

    for _ in tqdm(range(20000)):
        try:
            #  берем матчи, большие по id чем базовый
            arr = await full_match.find_one(
                {"_id": {"$gt": less_then_full_match_id}})
            #  присваиваем его id
            less_then_full_match_id = arr['_id']
            #  словарь для будущих преобразований
            df_dict = {}
            for attr in basic_attrs:
                #  добавляем базовые аттрибуты
                df_dict[attr] = get_collection_attr(arr, attr)

            radiantNetworthLeads = get_collection_attr(arr, 'radiantNetworthLeads')[-1]
            radiantXPLeads = get_collection_attr(arr, 'radiantExperienceLeads')[-1]

            radianKills = sum(get_collection_attr(arr, 'radiantKills'))
            direKills = sum(get_collection_attr(arr, 'direKills'))

            df_dict['radiantNetworthLeads'] = radiantNetworthLeads
            df_dict['radiantXPLeads'] = radiantXPLeads
            df_dict['radianKills'] = radianKills
            df_dict['direKills'] = direKills

            for player in get_collection_attr(arr, 'players'):
                single_df_string = process_player_data(df_dict, player)
                single_match_decomposition.append(single_df_string)
        except:
            continue

    df = pd.DataFrame(single_match_decomposition)

    df.to_csv('output.csv')

def process_player_data(df_dict, player):
    obj_dict = df_dict.copy()
    # Flatten the player data to extract the required fields
    flat_data = {
        "playerSlot": player.get("playerSlot"),
        "steamAccountId": player["steamAccount"]["id"],
        "isRadiant": player.get("isRadiant"),
        "heroId": player["hero"]["id"],
        "heroName": player["hero"]["name"],
        "kills": player.get("kills"),
        "deaths": player.get("deaths"),
        "assists": player.get("assists"),
        "numLastHits": player.get("numLastHits"),
        "numDenies": player.get("numDenies"),
        "goldPerMinute": player.get("goldPerMinute"),
        "networth": player.get("networth"),
        "experiencePerMinute": player.get("experiencePerMinute"),
        "level": player.get("level"),
        "gold": player.get("gold"),
        "goldSpent": player.get("goldSpent"),
        "heroDamage": player.get("heroDamage"),
        "towerDamage": player.get("towerDamage"),
        "heroHealing": player.get("heroHealing"),
        "lane": player.get("lane"),
        "position": player.get("position"),
        "role": player.get("role"),
        "roleBasic": player.get("roleBasic"),
        "award": player.get("award"),
    }
    return dict(list(obj_dict.items()) + list(flat_data.items()))


if __name__ == '__main__':
    loop = mongo_client.get_io_loop()
    loop.run_until_complete(read_main_match_data())
