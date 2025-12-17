class External_API_Helpers:
    def __init__(self, session: Session):
        self.__session = session

    def insert_all_countries(self):
        r = requests.get("https://countriesnow.space/api/v0.1/countries/flag/images")
        
        if r.status_code != 200:
            return False
    
        json: dict = r.json()

        for country_dict in json["data"]:
            self.__session.add(Countries(country_name=country_dict["name"], country_img_url=country_dict["flag"]))

        self.__session.commit()

    def insert_all_cities(self):
        r = requests.get("https://countriesnow.space/api/v0.1/countries")
        
        if r.status_code != 200:
            return False

        json: dict = r.json()

        for country_dict in json["data"]:
            country_query: Countries = self.__session.query(Countries) \
                .filter(Countries.country_name == country_dict["country"]) \
                .first()
            if country_query:
                for city in country_dict["cities"]:
                    self.__session.add(Cities(city_name=city, country_id=country_query.country_id))
                self.__session.commit()

    def check_if_database_is_empty(self) -> bool:
        countries_query: Query = self.__session.query(Countries.country_id)
        cities_query: Query = self.__session.query(Cities.city_id)

        if countries_query.count() == 0 and cities_query.count() == 0:
            return True
        return False

from sqlalchemy.orm import Session, Query
from .models import Cities, Countries, Base

import requests
from requests import Response