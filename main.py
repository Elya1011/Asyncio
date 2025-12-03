import asyncio
import aiohttp
from more_itertools import chunked


async def get_character(id_ch):
    session = aiohttp.ClientSession()
    response = await session.get(f"https://www.swapi.tech/api/people/{id_ch}/")
    json_data = await response.json()
    await session.close()
    return json_data

async def main():
    coro1 = get_character(3)
    coro2 = get_character(4)
    coro3 = get_character(10)
    result = await asyncio.gather(coro2, coro3, coro1)
    print(result)

asyncio.run(main())