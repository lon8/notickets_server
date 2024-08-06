from collections import defaultdict
import aiomysql
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import DBSCAN
import asyncio
from decouple import config
from loguru import logger

async def load_data():
    conn = await aiomysql.connect(host=config('HOST'), port=3306,
                                  user=config('LOGIN'), password=config('PASSWORD'),
                                  db=config('DB'), charset='utf8mb4')
    async with conn.cursor() as cur:
        await cur.execute("SELECT id, name, venue_id FROM all_events")
        data = await cur.fetchall()
    conn.close()
    return data

async def get_max_group_id(engine):
    async with engine.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("SELECT COALESCE(MAX(id), 0) FROM grouped_events")
            result = await cur.fetchone()
    return result[0]

async def insert_grouped_events(engine, new_group_ids):
    async with engine.acquire() as conn:
        async with conn.cursor() as cur:
            for group_id in new_group_ids:
                await cur.execute(
                    "INSERT INTO grouped_events (id) VALUES (%s)",
                    (group_id,)
                )
        await conn.commit()

def vectorize_data(names):
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(names)
    return tfidf_matrix

def cluster_data(tfidf_matrix):
    dbscan = DBSCAN(eps=0.5, min_samples=2, metric='cosine')
    clusters = dbscan.fit_predict(tfidf_matrix)
    return clusters

async def update_group_ids(engine, data_with_clusters):
    async with engine.acquire() as conn:
        async with conn.cursor() as cur:
            for row in data_with_clusters:
                event_id, group_id = row
                if group_id != -1:  # Пропускаем "шум"
                    await cur.execute(
                        "UPDATE all_events SET group_id = %s WHERE id = %s",
                        (group_id, event_id)
                    )
        await conn.commit()

async def run_clustering():
    engine = await aiomysql.create_pool(host=config('HOST'), port=3306,
                                  user=config('LOGIN'), password=config('PASSWORD'),
                                  db=config('DB'), charset='utf8mb4')

    # Шаг 1: Загрузка данных
    data = await load_data()

    # Извлечение параметров
    ids = [row[0] for row in data]
    names = [row[1] for row in data]
    venue_ids = [row[2] for row in data]

    # Шаг 2: Векторизация данных (только names)
    try:
        tfidf_matrix = vectorize_data(names)
    except:
        logger.warning('Skip this clustering session. Database is empty')
        engine.close()
        return
    # Шаг 3: Кластеризация данных
    clusters = cluster_data(tfidf_matrix)

    # Шаг 4: Получение текущего максимального group_id
    max_group_id = await get_max_group_id(engine)

    # Шаг 5: Формирование групп и фильтрация по venue_id
    cluster_to_group_id = {}
    next_group_id = max_group_id + 1

    # Группировка данных по кластерам
    cluster_dict = defaultdict(list)
    for i, cluster_id in enumerate(clusters):
        if cluster_id != -1:  # Пропускаем "шум"
            cluster_dict[cluster_id].append((ids[i], venue_ids[i]))

    # Формирование новых group_id
    new_group_ids = []
    for cluster_id, events in cluster_dict.items():
        venue_id_set = {venue_id for _, venue_id in events}
        if len(venue_id_set) == 1:
            group_id = next_group_id
            cluster_to_group_id[cluster_id] = group_id
            new_group_ids.append(group_id)
            next_group_id += 1

    # Шаг 6: Добавление новых group_id в таблицу grouped_events
    if new_group_ids:
        await insert_grouped_events(engine, new_group_ids)

    # Шаг 7: Создание окончательных данных с новыми group_id
    data_with_clusters = []
    for i, cluster_id in enumerate(clusters):
        event_id = ids[i]
        group_id = cluster_to_group_id.get(cluster_id, -1)  # Пропускаем "шум"
        if group_id != -1:
            data_with_clusters.append((event_id, group_id))

    # Шаг 8: Обновление group_id в таблице all_events
    await update_group_ids(engine, data_with_clusters)

    engine.close()

if __name__ == "__main__":
    asyncio.run(run_clustering())
