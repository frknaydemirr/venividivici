from sanic import Sanic, text, Request, json, exceptions
from http import HTTPMethod
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from database.definitions import *
from database.helpers import Database 

import jwt

database_url: str = "MOCK_DATABASE_URL"
engine = create_engine(database_url)
session = Session(engine)

db: Database = Database(session)
app = Sanic(__name__)

# Authentication helper function
def check_token(request: Request, user_id: int):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise exceptions.Unauthorized("Authorization header missing or invalid.")
    
    token = auth_header.split(" ")[1]
    try:
        decoded_token = jwt.decode(token, key="SERVER_SECRET", algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise exceptions.Unauthorized("Token has expired.")
    except jwt.InvalidTokenError:
        raise exceptions.Unauthorized("Invalid token.")
    
    if decoded_token.get("user_id") != user_id:
        raise exceptions.Forbidden("You do not have access to this user's information.")
    
    user_query: Users = session.query(Users).filter(Users.user_id == user_id).first()
    if not user_query:
        raise exceptions.NotFound()


# Login endpoint to get JWT token
@app.post("/login")
async def get_token(request: Request):
    username = request.json.get("username")
    password = request.json.get("password")
    
    if not username or not password:
        raise exceptions.InvalidUsage("Username and password are required.")
    
    if not db.get_user_exists(username) or not db.get_user_password_match(username, password):
        raise exceptions.Unauthorized("Invalid username or password.")

    client_token = jwt.encode({"user_id": db.get_user_id(username)}, key="SERVER_SECRET", algorithm="HS256")

    return json(body={"token": client_token})


# Cities endpoints

@app.get("/cities/<city_id:int>")
async def get_city(request: Request, city_id: int):
    city = db.get_specific_city(city_id=city_id)
    
    if not city:
        raise exceptions.NotFound("City not found.")

    return json(body=city)


@app.get("/cities/<city_id:int>/counts")
async def get_city_qa_counts(request: Request, city_id: int):
    counts = db.get_city_question_and_answer_counts(city_id=city_id)

    return json(body=counts)


@app.get("/cities/by-country/<country_id:int>")
async def get_cities_in_specific_country(request: Request, country_id: int):
    offset = int(request.args.get("offset", 0))
    limit = int(request.args.get("limit", 10))

    cities = db.get_cities_in_specific_country(country_id=country_id, offset=offset, limit=limit)

    if not cities:
        raise exceptions.NotFound("No cities found for the specified country.")

    return json(body=cities)


# TODO : Add limit to the Swagger documentation
@app.get("/cities/most-conquered")
async def get_most_conquered_cities(request: Request):
    limit = int(request.args.get("limit", 10))

    cities = db.get_most_conquered_cities(limit)

    if not cities:
        raise exceptions.NotFound("No cities found.")

    return json(cities)


# Countries endpoints

@app.get("/countries")
async def get_all_categories(request: Request):
    countries = db.get_all_countries()

    if not countries:
        raise exceptions.NotFound("No countries found.")

    return json(body=countries)


@app.get("/countries/<country_id:int>/counts")
async def get_country_qa_counts(request: Request, country_id: int):
    counts = db.get_country_question_and_answer_counts(country_id=country_id)

    if not counts:
        raise exceptions.NotFound("Country not found.")

    return json(body=counts)


@app.get("/countries/<country_id:int>")
async def get_country(request: Request, country_id: int):
    country = db.get_specific_country(country_id=country_id)

    if not country:
        raise exceptions.NotFound("Country not found.")

    return json(body=country)


# TODO : Add limit to the Swagger documentation
@app.get("/countries/most-conquered")
async def get_most_conquered_countries(request: Request):
    limit = int(request.args.get("limit", 10))

    countries = db.get_most_conquered_countries(limit=limit)

    if not countries:
        raise exceptions.NotFound("No countries found.")

    return json(body=countries)



# Questions endpoints
