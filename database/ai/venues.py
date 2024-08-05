from fastapi import HTTPException

from decouple import config
import aiomysql
import asyncio
from loguru import logger

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

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
        autocommit=True
    )


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


async def get_venue_names_from_database():
    
    data = await get_venues()
    result = list(data.values())

    return result


async def create_venue(venue):
    query = "INSERT INTO venues (name) VALUES (%s)"
    params = (venue, )
    
    conn = await connect_to_database()
    try:
        async with conn.cursor(aiomysql.DictCursor) as cursor:
            await cursor.execute(query, params)
            await conn.commit()
            lastrowid = cursor.lastrowid
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    return lastrowid
        
# Функция для поиска или создания площадки
async def find_or_create_venue(input_venue_name: str) -> int:
    venue_names = await get_venue_names_from_database()

    # Преобразуем исходные названия площадок в векторы TF-IDF
    vectorizer = TfidfVectorizer()
    try:
        tfidf_matrix = vectorizer.fit_transform(venue_names)
    except ValueError:
        return await create_venue(input_venue_name)

    # Преобразуем новое название площадки в вектор TF-IDF
    new_tfidf_vector = vectorizer.transform([input_venue_name])

    # Расчет косинусного сходства между новым названием и всеми площадками
    cosine_similarities = linear_kernel(new_tfidf_vector, tfidf_matrix).flatten()

    # Находим индекс площадки с наивысшим косинусным сходством
    best_match_index = cosine_similarities.argmax()

    # Если ближайшее соответствие имеет достаточно высокий балл, возвращаем id
    if cosine_similarities[best_match_index] >= 0.8:
        # Индексация начинается с 0, поэтому добавляем 1.
        venue_id = int(best_match_index + 1)
    else:
        # Если не найдено подходящего соответствия, создаем новую площадку
        venue_id = await create_venue(input_venue_name)
        venue_id = int(venue_id)

    return venue_id


# Пример использования

async def main():
    input_venue_name = "Театр Ленком"
    venue_id = await find_or_create_venue(input_venue_name)
    print(f"ID площадки '{input_venue_name}': {venue_id}")

if __name__ == '__main__':
    asyncio.run(main())