import json
from sqlalchemy import create_engine, Column, Integer, Float, String, Text, DateTime, ForeignKey, MetaData
from sqlalchemy.orm import declarative_base, sessionmaker
from decouple import config

Base = declarative_base(metadata=MetaData())

DATABASE_LINK = config('DATABASE_LINK')

engine = create_engine(DATABASE_LINK)

class AllEvents(Base):
    __tablename__ = 'all_events'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))  # Размер 255 (замените на нужный)
    link = Column(String(255))  # Размер 255 (замените на нужный)
    parser = Column(String(255))  # Размер 255 (замените на нужный)
    venue_id = Column(Integer, ForeignKey('venues.id'))
    date = Column(DateTime)
    image_link  = Column(String(255))

class Categories(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, autoincrement=True)
    category_name = Column(String(255))  # Размер 255 (замените на нужный)


class EventCategories(Base):
    __tablename__ = 'event_categories'

    event_id = Column(Integer, ForeignKey('all_events.id'), primary_key=True)
    category_id = Column(Integer, ForeignKey('categories.id'), primary_key=True)


class Venues(Base):
    __tablename__ = 'venues'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))  # Размер 255 (замените на нужный)
    description = Column(Text)


class Cities(Base):
    __tablename__ = 'cities'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))  # Размер 255 (замените на нужный)
    latitude = Column(Float)
    longitude  = Column(Float)


class CityVenues(Base):
    __tablename__ = 'city_venues'

    city_id = Column(Integer, ForeignKey('cities.id'), primary_key=True)
    venue_id = Column(Integer, ForeignKey('venues.id'), primary_key=True)


class GroupedEvents(Base):
    __tablename__ = 'grouped_events'

    id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey('all_events.id'))
    description = Column(Text)
    venue_id = Column(Integer, ForeignKey('venues.id'))


class Sites(Base):
    __tablename__ = 'sites'

    id = Column(Integer, primary_key=True, autoincrement=True)
    site = Column(String(255))  # Размер 255 (замените на нужный)


class EventSites(Base):
    __tablename__ = 'event_sites'

    event_id = Column(Integer, ForeignKey('all_events.id'), primary_key=True)
    site_id = Column(Integer, ForeignKey('sites.id'), primary_key=True)


Session = sessionmaker(bind=engine)

metadata = Base.metadata.create_all(bind=engine)

session = Session()

# Чтение JSON-файла
with open('temp/cities_full.json') as json_file:
    cities = json.load(json_file)

# Вставка данных в таблицу
for city_id, city_info in cities.items():
    city = Cities(
        id=int(city_id),
        name=city_info['city'],
        latitude=city_info['coordinates']['latitude'],
        longitude=city_info['coordinates']['longitude']
    )
    session.add(city)

# Подтверждение изменений
session.commit()

# Закрытие сессии
session.close()