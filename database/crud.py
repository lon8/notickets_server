from fastapi import APIRouter, HTTPException
import aiomysql

from database.forms import Event, Parser, RegionRequest, EventResponse, VenuePayload, VenueRequest
from database.ai.venues import find_or_create_venue

from decouple import config
from loguru import logger

router = APIRouter()

HOST = config('HOST')
DB = config('DB')
USER = config('LOGIN')
PASSWORD = config('PASSWORD')
PORT = config('PORT')


async def connect_to_database():
    return await aiomysql.connect(
        host=HOST,
        port=int(PORT),
        user=USER,
        password=PASSWORD,
        db=DB,
        autocommit=True,
        charset='utf8mb4'
    )

async def execute_query(query, params, conn):
    async with conn.cursor() as cursor:
        await cursor.execute(query, params)
        return await cursor.fetchall()

#####################################
####   ROUTERS FOR PARSERS       ####
#####################################

@router.post("/api/put_event")
async def put_events(event: Event):
    venue_id = await find_or_create_venue(event.venue)

    check_query = """
        SELECT COUNT(*) FROM all_events
        WHERE name = %s AND link = %s AND parser = %s AND date = %s AND venue_id = %s
    """
    check_params = (event.name, event.link, event.parser, event.date, venue_id)

    conn = await connect_to_database()
    logger.debug('Connection is successful')

    try:
        result = await execute_query(check_query, check_params, conn)
        count = result[0][0]
        if count > 0:
            logger.info(f"Event already exists")
            return {"message": "Event already exists"}

        query = """
            INSERT INTO all_events (name, link, parser, date, venue_id, image_link)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        params = (event.name, event.link, event.parser, event.date, venue_id, event.image_links)

        await execute_query(query, params, conn)
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
    finally:
        conn.close()

    return {"message": "Event added successfully"}

# @router.post("/api/clear_events")
# async def clear_events(parser: Parser):
#     query = "DELETE FROM all_events WHERE parser = %s"
#     params = (parser.parser,)

#     conn = await connect_to_database()
#     try:
#         await execute_query(query, params, conn)
#     except Exception as e:
#         logger.error(f"An error occurred: {e}")
#         raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
#     finally:
#         conn.close()

#     return {"message": "Events cleared successfully"}


#####################################
####   ROUTERS FOR FRONTEND      ####
#####################################


@router.post("/api/get_city_events")
async def get_events(request: RegionRequest):
    query = "SELECT id, name, link, parser, date, venue_id, image_link FROM all_events"

    events = []
    conn = None
    try:
        conn = await connect_to_database()
        logger.debug('Connection is successful')
        async with conn.cursor(aiomysql.DictCursor) as cursor:
            await cursor.execute(query)
            rows = await cursor.fetchall()
            events = [(EventResponse(
                id=row["id"],
                name=row['name'],
                link=row['link'],
                parser=row['parser'],
                date=row['date'].strftime('%Y-%m-%d %H:%M:%S'),
                venue_id=row['venue_id'],
                image_links=[row['image_link']]
            )) for row in rows]

    except aiomysql.MySQLError as e:
        logger.error(f"Database error occurred: {e}")
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
    finally:
        if conn:
            conn.close()
    
    return events

@router.post("/api/get_events_by_venue")
async def get_events_by_venue(payload: VenuePayload):
    query = "SELECT id, name, link, parser, date, venue_id, image_link FROM all_events WHERE venue_id  =  %s"
    params = (payload.venue_id, )

    events = []
    conn = None
    try:
        conn = await connect_to_database()
        logger.debug('Connection is successful')
        async with conn.cursor(aiomysql.DictCursor) as cursor:
            await cursor.execute(query, params)
            rows = await cursor.fetchall()
            
            events = [(Event(
                name=row['name'],
                link=row['link'],
                parser=row['parser'],
                date=row['date'].strftime('%Y-%m-%d %H:%M:%S'),
                venue_id=row['venue_id'],
                image_links=[row['image_link']]
            )) for row in rows]

    except aiomysql.MySQLError as e:
        logger.error(f"Database error occurred: {e}")
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
    finally:
        if conn:
            conn.close()
    
    return events

@router.get('/api/get_cities')
async def get_cities():
    query = "SELECT id, name, latitude, longitude FROM cities"
    
    try:
        conn = await connect_to_database()

        async with conn.cursor() as cursor:

            await cursor.execute(query)
            rows = await cursor.fetchall()
            
            cities_dict = {}
            for row in rows:
                city_id = str(row[0])
                city_name = row[1]
                latitude = row[2]
                longitude = row[3]
                
                cities_dict[city_id] = {
                    "city": city_name,
                    "latitude": latitude,
                    "longitude": longitude
                }

    except aiomysql.MySQLError as e:
        logger.error(f"Database error occurred: {e}")
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
    finally:
        if conn:
            conn.close()

    return cities_dict
    
@router.get('/api/get_venues')
async def get_venues():
    query = "SELECT id, name FROM venues"

    try:
        conn = await connect_to_database()

        async with conn.cursor() as cursor:

            await cursor.execute(query)
            rows = await cursor.fetchall()
            
            # Формируем результат в нужном формате
            venues_dict = {str(row[0]): row[1] for row in rows}

    except aiomysql.MySQLError as e:
        logger.error(f"Database error occurred: {e}")
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
    finally:
        if conn:
            conn.close()

    return venues_dict
