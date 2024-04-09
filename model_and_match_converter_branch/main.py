import datetime
from motor.motor_asyncio import AsyncIOMotorClient
import pandas as pd
import json
import numpy as np
from pymongo import MongoClient
import pymongo.errors
import requests


def utility_read_from_json(filename):
    with open(filename) as f:
        lines = f.read()
        return json.loads(lines)


async def utility_work_with_json_object():
    single_match_decomposition = []
    basic_attrs = ['id', 'didRadiantWin', 'durationSeconds', 'startDateTime',
                   'firstBloodTime', 'gameMode']
    doc_size = 0
    less_then_full_match_id = 7451753118  # (await full_match.find_one())['_id']
    print(less_then_full_match_id)
    # arr = utility_read_from_json('dota_db.full_match_collection.json')
    # print(full_match.find_one({"_id": {"$lt": less_then_full_match_id}})['_id'])
    while doc_size < 50000:
        doc_size += 1  #
        print(less_then_full_match_id)
        arr = await full_match.find_one({"_id": {"$gt": less_then_full_match_id}})
        less_then_full_match_id = arr['_id']
        df_dict = {}
        for attr in basic_attrs:
            df_dict[attr] = get_collection_attr(arr, attr)
        print(df_dict)
        radiantNetworthLeads = get_collection_attr(arr, 'radiantNetworthLeads')

        tower_utils = utility_read_from_json('creeps_buildings.json')
        for npc in tower_utils:
            df_dict[npc['name']] = 1
        for minute in range(len(radiantNetworthLeads[2:])):
            obj_dict = df_dict.copy()
            obj_dict['currentMinute'] = minute + 1
            minuteRadiantNetworthLead = radiantNetworthLeads[minute]
            obj_dict['minuteRadiantNetworthLead'] = minuteRadiantNetworthLead
            minuteRadiantExperienceLeads = get_collection_attr(arr, 'radiantExperienceLeads')[minute]
            obj_dict['minuteRadiantExperienceLeads'] = minuteRadiantExperienceLeads
            minuteRadiantKills = get_collection_attr(arr, 'radiantKills')[minute]
            obj_dict['minuteRadiantKills'] = minuteRadiantKills
            minuteDireKills = get_collection_attr(arr, 'direKills')[minute]
            obj_dict['minuteDireKills'] = minuteDireKills
            get_players_data(arr, minute, obj_dict)
            get_tower_barracks_destroy_dict(get_collection_attr(arr, 'towerDeaths'),
                                            minute, df_dict, tower_utils)
            single_match_decomposition.append(obj_dict)
            update = {"$set": obj_dict}
            print(obj_dict)
            result = await dataframe_match_collection.update_one(obj_dict, update, upsert=True)
            print(result)


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

    player_dict[side + pos + '_attackType'] = player['hero']['stats']['attackType']
    player_dict[side + pos + '_startingArmor'] = player['hero']['stats']['startingArmor']
    player_dict[side + pos + '_startingDamageMin'] = player['hero']['stats']['startingDamageMin']
    player_dict[side + pos + '_startingDamageMax'] = player['hero']['stats']['startingDamageMax']
    player_dict[side + pos + '_attackRate'] = player['hero']['stats']['attackRate']
    player_dict[side + pos + '_attackAnimationPoint'] = player['hero']['stats']['attackAnimationPoint']
    player_dict[side + pos + '_attackAcquisitionRange'] = player['hero']['stats']['attackAcquisitionRange']
    player_dict[side + pos + '_attackRange'] = player['hero']['stats']['attackRange']
    player_dict[side + pos + '_primaryAttribute'] = player['hero']['stats']['primaryAttribute']
    player_dict[side + pos + '_strengthBase'] = player['hero']['stats']['strengthBase']
    player_dict[side + pos + '_strengthGain'] = player['hero']['stats']['strengthGain']
    player_dict[side + pos + '_intelligenceBase'] = player['hero']['stats']['intelligenceBase']
    player_dict[side + pos + '_intelligenceGain'] = player['hero']['stats']['intelligenceGain']
    player_dict[side + pos + '_agilityBase'] = player['hero']['stats']['agilityBase']
    player_dict[side + pos + '_agilityGain'] = player['hero']['stats']['agilityGain']
    player_dict[side + pos + '_moveSpeed'] = player['hero']['stats']['moveSpeed']

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

    for item in range(6):
        if player['stats']['inventoryReport'][minute]['item' + str(item)] is not None:
            player_dict[side + pos + '_item_' + item] = \
                player['stats']['inventoryReport'][minute]['item' + str(item)]['itemId']
        else:
            player_dict[side + pos + '_item_' + item] = 0

    for backpack_item in range(3):
        if player['stats']['inventoryReport'][minute]['backPack' + str(backpack_item)] is not None:
            player_dict[side + pos + '_backpack_' + backpack_item] = \
                player['stats']['inventoryReport'][minute]['backPack' + str(backpack_item)]['itemId']
        else:
            player_dict[side + pos + '_backpack_item_' + backpack_item] = 0

    if player['stats']['inventoryReport'][minute]['neutral0'] is not None:
        player_dict[side + pos + '_neutral0'] = \
            player['stats']['inventoryReport'][minute]['neutral0']['itemId']
    else:
        player_dict[side + pos + '_neutral0'] = 0



def work_with_file():
    json_text = utility_read_from_json('dota_db.full_match_collection.json')
    print(json_text)


def create_mongo_connection():
    try:
        # Менять соединение с монгой
        client = AsyncIOMotorClient("localhost", 27017)
        db = client.dota_db
        return client, db
    except pymongo.errors.ServerSelectionTimeoutError as err:
        print(err)


mongo_client, mongo_db = create_mongo_connection()
match_ids_coll = mongo_db.match_id_collection
match_info = mongo_db.match_info_collection
full_match = mongo_db.full_match_collection
pro_match_id = mongo_db.pro_id_collection
pro_info = mongo_db.pro_info_collection
pro_full_match = mongo_db.pro_full_match_collection
dataframe_match_collection = mongo_db.dataframe_match_collection
batch_size = 10


def get_collection_attr(arr, attr_name):
    return arr['match'][attr_name]


def get_data_from_db():
    basic_attrs = ['id', 'didRadiantWin', 'durationSeconds', 'startDateTime', 'towerStatusRadiant',
                   'towerStatusDire', 'barracksStatusRadiant', 'barracksStatusDire', 'firstBloodTime', 'gameMode']
    for i in range(10):  # full_match.count_documents({})
        arr = list(full_match.find(limit=10, batch_size=10))
        df_dict = {}
        for attr in basic_attrs:
            df_dict[attr] = get_collection_attr(arr, attr)
            radiantNetworthLeads = get_collection_attr(arr, 'radiantNetworthLeads')

        for minute in range(len(radiantNetworthLeads)):
            obj_dict = df_dict.copy()
            minuteRadiantNetworthLead = radiantNetworthLeads[minute]
            obj_dict['minuteRadiantNetworthLead'] = minuteRadiantNetworthLead
            minuteRadiantExperienceLeads = get_collection_attr(arr, 'radiantExperienceLeads')[minute]
            obj_dict['minuteRadiantExperienceLeads'] = minuteRadiantExperienceLeads
            minuteRadiantKills = get_collection_attr(arr, 'radiantKills')[minute]
            obj_dict['minuteRadiantKills'] = minuteRadiantKills
            minuteDireKills = get_collection_attr(arr, 'direKills')[minute]
            obj_dict['minuteDireKills'] = minuteDireKills
        break


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    loop = mongo_client.get_io_loop()
    loop.run_until_complete(utility_work_with_json_object())

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
