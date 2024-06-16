import mysql.connector
import json

# Подключение к базе данных MySQL
db_connection = mysql.connector.connect(
  host="localhost",
  user="lon8",
  password="132465-Cs",
  database="notickets"
)

# Создание курсора для выполнения SQL-запросов
cursor = db_connection.cursor()

# Чтение JSON-файла
with open('cities_full.json') as json_file:
    cities = json.load(json_file)


# Вставка данных в таблицу
for city_id, city_info in cities.items():
    city_name = city_info['city']
    latitude = city_info['coordinates']['latitude']
    longitude = city_info['coordinates']['longitude']
    
    cursor.execute('''
    INSERT INTO cities (id, name, latitude, longitude)
    VALUES (%s, %s, %s, %s)
    ''', (int(city_id), city_name, latitude, longitude))

# Подтверждение изменений
db_connection.commit()

# Закрытие курсора и соединения
cursor.close()
db_connection.close()