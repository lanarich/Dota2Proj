import asyncio
import time

import aiohttp
from pymongo import UpdateOne

from matches_parsing_script.MongoDB import MongoDBWorker
from matches_parsing_script.StratzRequest import StratzRequest
import matches_parsing_script.utils as utils


class BaseParser(StratzRequest, MongoDBWorker):

    def __init__(self, query_name, host, port):
        MongoDBWorker.__init__(self, host, port)
        self.client, self.db = self.create_mongo_connection()
        self.query = query_name
        self.queries = None

    def __create_ids_queries(self, id_array):
        full_query = self.query
        self.queries = [full_query.format(hero_id) for hero_id in id_array]

    def __create_batches(self, lst, n):
        for i in range(0, len(lst), n):
            yield lst[i:i + n]

    async def get_heroes_ids(self):
        response = await self.stratz_request(self.query)
        result = 'Empty'
        if response is None:
            print('Response == None')
            return
        hero_ids = response['data']['constants']['heroes']
        id_list = []
        for _id in hero_ids:
            id_list.append(_id['id'])
        print('ids successfully written')
        return id_list

    async def create_batch_request(self, hero_ids):
        response_array = []
        batch_index = 0
        self.__create_ids_queries(hero_ids)
        query_batches = list(self.__create_batches(self.queries, utils.BATCH_SIZE))
        while batch_index < len(query_batches):
            requests = query_batches[batch_index]
            response = await self.stratz_api_calls(requests)
            response_array.append(response)
            time.sleep(1)
            if response is not None:
                pass
            batch_index += 1

        return response_array

    def parse_response(self, response, mode):
        result = 'Empty'
        if response is None:
            print('Response == None')
            return
        if mode == 'banDay':
            updates = []
            ban_days = response['data']['heroStats']
            for hero in ban_days['banDay']:
                print(hero)
                hero_id = hero.get('heroId')

                _filter = {'_id': hero_id}
                update = {
                    "$set": {
                        '_id': hero_id,
                        'bans': hero
                    }}
                updates.append(UpdateOne(_filter, update, upsert=True))
            if len(updates) > 0:
                result = self.db.matchup_coll.bulk_write(updates)

        if mode == 'winDay':
            updates = []
            winrate = response['data']['heroStats']
            for hero in winrate['winDay']:
                print(hero)
                hero_id = hero.get('heroId')

                _filter = {'_id': hero_id}
                update = {
                    "$set": {
                        '_id': hero_id,
                        'wins': hero
                    }}
                updates.append(UpdateOne(_filter, update, upsert=True))
            if len(updates) > 0:
                result = self.db.matchup_coll.bulk_write(updates)

        if mode == 'hero_stats':
            updates = []
            stats = response['data']['heroStats']
            for hero in stats['stats']:
                print(hero)
                hero_id = hero.get('heroId')

                _filter = {'_id': hero_id}
                update = {
                    "$set": {
                        '_id': hero_id,
                        'stats': hero
                    }}
                updates.append(UpdateOne(_filter, update, upsert=True))
            if len(updates) > 0:
                result = self.db.matchup_coll.bulk_write(updates)

        if mode == 'hero_attrs':
            updates = []
            attributes = response['data']['constants']
            for hero in attributes['heroes']:
                print(hero)
                hero_id = hero.get('id')

                _filter = {'_id': hero_id}
                update = {
                    "$set": {
                        '_id': hero_id,
                        'attributes': hero
                    }}
                updates.append(UpdateOne(_filter, update, upsert=True))
            if len(updates) > 0:
                result = self.db.matchup_coll.bulk_write(updates)

        # Запрос на каждого героя
        if mode == 'heroes_matchup':
            updates = []
            for combined in response:
                for hero in combined:
                    stats = hero['data']['heroStats']['heroVsHeroMatchup']
                    for advantage in stats['advantage']:
                        print(advantage)
                        hero_id = advantage.get('heroId')

                        _filter = {'_id': hero_id}
                        update = {
                            "$set": {
                                '_id': hero_id,
                                'matchup': advantage
                            }}
                        updates.append(UpdateOne(_filter, update, upsert=True))
            if len(updates) > 0:
                result = self.db.matchup_coll.bulk_write(updates)

        print(result)


async def main():
    # Получить id героев
    heroes = BaseParser(utils.hero_ids_query, 'localhost', 27017)
    hero_ids = await heroes.get_heroes_ids()

    # Комбинированне статы
    combo = BaseParser(utils.two_heroes_stats_query, 'localhost', 27017)
    response = await combo.create_batch_request(hero_ids)
    combo.parse_response(response, 'heroes_matchup')
    time.sleep(1)

    # Парсинг статистики за неделю
    hero_stat_for_week = BaseParser(utils.hero_stats_query, 'localhost', 27017)
    response = await hero_stat_for_week.stratz_request(hero_stat_for_week.query)
    hero_stat_for_week.parse_response(response, 'hero_stats')
    time.sleep(1)

    # Парсинг банов за день
    ban_ids = BaseParser(utils.ban_query, 'localhost', 27017)
    response = await ban_ids.stratz_request(ban_ids.query)
    ban_ids.parse_response(response, 'banDay')
    time.sleep(1)

    # Парсинг винрейта за 12 дней
    winrate = BaseParser(utils.winrate_query, 'localhost', 27017)
    response = await winrate.stratz_request(winrate.query)
    winrate.parse_response(response, 'winDay')
    time.sleep(1)

    # Базовые аттрибуты
    attributes = BaseParser(utils.hero_attributes, 'localhost', 27017)
    response = await attributes.stratz_request(attributes.query)
    attributes.parse_response(response, 'hero_attrs')
    time.sleep(1)

    print('Готово')


if __name__ == '__main__':
    asyncio.run(main())
