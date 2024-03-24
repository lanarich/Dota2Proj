import asyncio
import datetime

import aiohttp
import pymongo
from pymongo import MongoClient, UpdateOne
import pymongo.errors


def create_mongo_connection():
    try:
        # Менять соединение с монгой
        client = MongoClient("localhost", 27017)
        db = client.dota_db
        return client, db
    except pymongo.errors.ServerSelectionTimeoutError as err:
        print(err)


mongo_client, mongo_db = create_mongo_connection()

full_match = mongo_db.test_match_coll

local_stratz_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJTdWJqZWN0IjoiYjJjNjQyM2EtZjlmNS00YmI1LWI2MmUtOWRiYzAyZDc2YzQ5IiwiU3RlYW1JZCI6IjM2NzY1MzgzNCIsIm5iZiI6MTY5OTk3MjM5MCwiZXhwIjoxNzMxNTA4MzkwLCJpYXQiOjE2OTk5NzIzOTAsImlzcyI6Imh0dHBzOi8vYXBpLnN0cmF0ei5jb20ifQ.-8nipaADxb1dGUcyKm9aEKtAcE9MS_MVY0khHC3ZhfE"

url = 'https://api.stratz.com/graphql'

headers = {"Authorization": f"Bearer {local_stratz_token}"}


def create_query(match_id):
    my_file = open("graphql_parse_data.txt", "r")
    parsing_string = my_file.read()
    my_file.close()
    graph_query = {'query': '''{
            match(id: %s) {
                %s
            }
        }''' % (match_id, parsing_string)}
    return graph_query


async def fetch_stratz(match_id):
    try:
        async with aiohttp.ClientSession() as session:

            response = await session.post(url, json=match_id, headers=headers)

            return await response.json()
    except Exception as e:
        print(datetime.datetime.now(), ": Что то пошло не так при парсинге стратз батча")
        print(e)


async def stratz_match_request(match_id):
    start = datetime.datetime.now()
    print(start, ": Началась обработка батча")
    stratz_query = create_query(match_id)
    # дожидаемся запросов
    match = await fetch_stratz(stratz_query)
    # проверяем данные
    if match is None:
        return False
    # проверяем конкретный матч
    if match['data']['match'] is None:
        print(datetime.datetime.now(), ': Match is None')

    else:
        # проверяем матч на то что обработан стратзом
        if match['data']['match'].get('parsedDateTime') is None:
            print(datetime.datetime.now(), ': Match[id]: ', match['data']['match'].get('id'),
                  'not parsed by Stratz yet')
            return None
        else:
            _filter = {'_id': match['data']['match'].get('id')}
            update = {"$set": {'_id': match['data']['match'].get('id'),
                               'match': match['data']['match'],
                               'insert_date': datetime.datetime.now()}}
            result = full_match.update_one(_filter, update, upsert=True)

            if result is not None:
                print(result)

    end = datetime.datetime.now()
    print("Матч успешно добавлен в БД, \nВремя добавления составило: ", end - start)
    return match


async def stratz_match_request_wout_db(match_id):
    start = datetime.datetime.now()
    print(start, ": Началась обработка батча")
    stratz_query = create_query(match_id)
    # дожидаемся запросов
    match = await fetch_stratz(stratz_query)
    # проверяем данные
    if match is None:
        return None
    # проверяем конкретный матч
    if match['data']['match'] is None:
        print(datetime.datetime.now(), ': Match is None')
        return None
    else:
        # проверяем матч на то что обработан стратзом
        if match['data']['match'].get('parsedDateTime') is None:
            print(datetime.datetime.now(), ': Match[id]: ', match['data']['match'].get('id'),
                  'not parsed by Stratz yet')
            return None

    end = datetime.datetime.now()
    print("Матч успешно добавлен в БД, \nВремя добавления составило: ", end - start)
    return match


def check_match_presence_in_db(match_id):
    doc = full_match.find_one({"_id": match_id})
    return doc


async def get_match_data(match_id):
    # получаем айдишники в первый раз
    doc = check_match_presence_in_db(match_id)
    if doc is None:
        match_data = await stratz_match_request(match_id)
        return match_data
    else:
        return doc
