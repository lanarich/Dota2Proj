import datetime

import aiohttp
import asyncio

from matches_parsing_script.utils import url, headers


class StratzRequest:

    async def stratz_request(self, query):
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, data=query) as resp:
                return await resp.json()

    async def fetch(self, session, data):
        async with session.post(url, data=data, headers=headers) as response:
            return await response.json()

    async def stratz_api_calls(self, query_batch):
        try:
            async with aiohttp.ClientSession() as session:
                # формируем таски из батчей запросов
                tasks = [
                    asyncio.ensure_future(
                        self.fetch(
                            session,
                            data)) for data in query_batch]
                # выполняем таски, получая запросы в респонс
                responses = await asyncio.gather(*tasks)
                return responses
        except Exception as e:
            print(
                datetime.datetime.now(),
                ": Что то пошло не так при парсинге стратз батча")
            print(e)
