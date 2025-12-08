from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session, Query
from definitions import Countries, Cities

import requests
from requests import Response

# /countries/flag/images
def insert_all_countries(r: Response, session: Session) -> bool:
    if r.status_code != 200:
        return False
    
    json: dict = r.json()

    for country_dict in json["data"]:
        session.add(Countries(country_name=country_dict["name"], country_img_url=country_dict["flag"]))

    session.commit()

# /countries
def insert_all_cities(r: Response, session: Session) -> bool:
    if r.status_code != 200:
        return False

    json: dict = r.json()

    for country_dict in json["data"]:
        country_query: Query = session.query(Countries).filter(text(f"country_name='{country_dict["country"]}'")).first()
        if country_query:
            for city in country_dict["cities"]:
                session.add(Cities(city_name=city, country_id=country_query.country_id))
            session.commit()