import aiomysql
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import DBSCAN
import asyncio
from decouple import config


async def load_data():
    conn = await aiomysql.connect(host=config('HOST'), port=3306,
                                  user=config('LOGIN'), password=config('PASSWORD'),
                                  db=config('DB'), charset='utf8mb4')
    async with conn.cursor() as cur:
        await cur.execute("SELECT id, name, venue_id, date FROM all_events")
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

def vectorize_data(data):
    descriptions = [f"{row[1]} {row[2]} {row[3]}" for row in data]  # Используем name, venue_id и date для описания
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(descriptions)
    return tfidf_matrix

def cluster_data(tfidf_matrix):
    dbscan = DBSCAN(eps=0.5, min_samples=2, metric='cosine')
    clusters = dbscan.fit_predict(tfidf_matrix)
    return clusters

async def update_group_ids(engine, data_with_clusters):
    async with engine.acquire() as conn:
        async with conn.cursor() as cur:
            for row in data_with_clusters:
                event_id, _, _, _, cluster_id = row
                await cur.execute(
                    "UPDATE all_events SET group_id = %s WHERE id = %s",
                    (cluster_id, event_id)
                )
    await conn.commit()

async def run_clustering():
    engine = await aiomysql.create_pool(host='your_host', port=3306,
                                        user='your_username', password='your_password',
                                        db='your_database', charset='utf8mb4')

    # Шаг 1: Загрузка данных
    data = await load_data()

    # Шаг 2: Векторизация данных
    tfidf_matrix = vectorize_data(data)

    # Шаг 3: Кластеризация данных
    clusters = cluster_data(tfidf_matrix)

    # Шаг 4: Получение текущего максимального group_id
    max_group_id = await get_max_group_id(engine)
    
    # Добавляем новые идентификаторы кластерам
    cluster_map = {}
    next_group_id = max_group_id + 1
    new_group_ids = []

    for i, cluster_id in enumerate(clusters):
        if cluster_id == -1:
            continue  # Пропускаем шум
        if cluster_id not in cluster_map:
            cluster_map[cluster_id] = next_group_id
            new_group_ids.append(next_group_id)
            next_group_id += 1
    
    # Шаг 5: Добавление новых group_id в таблицу grouped_events
    await insert_grouped_events(engine, new_group_ids)

    # Обновляем данные с новыми group_id
    data_with_clusters = [list(row) + [cluster_map.get(clusters[i], -1)] for i, row in enumerate(data)]

    # Шаг 6: Обновление group_id в таблице all_events
    await update_group_ids(engine, data_with_clusters)

    engine.close()

if __name__ == "__main__":
    asyncio.run(run_clustering())
