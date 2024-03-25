from fastapi import APIRouter, HTTPException

from database.models import session, AllEvents
from database.forms import Event

from decouple import config

router = APIRouter()

HOST = config('HOST')
DB = config('DB')
USER = config('USER')
PASSWORD = config('PASSWORD')
PORT = config('PORT')


async def connect_to_database():
    return await aiomysql.connect(
        host=HOST,
        port=PORT,
        user=USER,
        password=PASSWORD,
        db=DB,
        autocommit=True
    )


async def execute_query(query, conn):
    async with conn.cursor() as cursor:
        await cursor.execute(query)
        return await cursor.fetchall()


@router.post("/put_event/")
async def put_events(event: Event):
    query = f"INSERT INTO all_events (name, link, parser, date, venue) VALUES ('{event.name}', '{event.link}', '{event.parser}', '{event.date}', '{event.venue}')"

    conn = await connect_to_database()
    try:
        await execute_query(query, conn)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
    finally:
        conn.close()

    return {"message": "Event added successfully"}


@router.post('/put_events/')
def put_events(event: Event):
    print(event.name, event.parser)

    new_event = AllEvents(
        name=event.name,
        link=event.link,
        parser=event.parser,
        date=event.date,
        venue=event.venue
    )
    session.add(new_event)
    session.commit()
