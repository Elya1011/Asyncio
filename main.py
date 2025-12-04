import asyncio
import aiohttp
from more_itertools import chunked
from models import DbSession, SwapiPeople, close_orm, init_orm


async def get_people(people_id, session):
    response = await session.get(f"https://www.swapi.tech/api/people/{people_id}/")
    if response.status != 200:
        return None

    json_data = await response.json()

    person = json_data.get('result')
    if not person:
        return None

    properties = person.get('properties')
    if not properties:
        return None

    data = {
        "id": person.get('uid'),
        "birth_year": properties.get('birth_year'),
        "eye_color": properties.get('eye_color'),
        "gender": properties.get('gender'),
        "hair_color": properties.get('hair_color'),
        "homeworld": properties.get('homeworld'),
        "mass": properties.get('mass'),
        "name": properties.get('name'),
        "skin_color": properties.get('skin_color'),
    }
    return data

async def insert_people(people_data: list[dict]):
    async with DbSession() as session:
        orm_people = [SwapiPeople(json=person) for person in people_data]
        session.add_all(orm_people)
        await session.commit()

async def main():
    await init_orm()
    async with aiohttp.ClientSession() as session:
        people_ids = range(1, 84)
        for people_ids in chunked(people_ids, 5):
            coros  = [get_people(i, session) for i in people_ids]
            results = await asyncio.gather(*coros)
            task = asyncio.create_task(insert_people(results))
        tasks = asyncio.all_tasks()
        main_task = asyncio.current_task()
        tasks.remove(main_task)
        await asyncio.gather(*tasks)
    await close_orm()

asyncio.run(main())