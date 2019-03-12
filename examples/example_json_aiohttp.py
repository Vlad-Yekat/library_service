""" В этом модуле примеры внешних запросов """
import json
import aiohttp
import asyncio

URL_LIBRARY_SERVICE = "http://localhost:8000"


async def fetch(session, url):
    test_add_writer = {
        "method": "add_writer",
        "params": {
            "name": "Adam",
            "surname": "Smith",
            "city": "Kirkcaldy",
            "birth_date": "1723-06-17",
        },
        "jsonrpc": "2.0",
        "id": 123,
    }
    print("->", json.dumps(test_add_writer, indent=4, sort_keys=False))
    async with session.post(url, json=test_add_writer) as response:
        return await response.json()


async def main():
    async with aiohttp.ClientSession() as session:
        result = await fetch(session, URL_LIBRARY_SERVICE)
        print("<-", result)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
