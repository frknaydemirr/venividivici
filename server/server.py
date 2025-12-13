# TODO: Add questions by category endpoints
# TODO: Add POST and DELETE endpoints

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

@app.get("/questions/<question_id:int>")
async def get_specific_question(request: Request, question_id: int):
    question = db.get_specific_question(question_id=question_id)

    if not question:
        raise exceptions.NotFound("Question not found.")

    return json(body=question)


@app.get("/questions/<question_id:int>/counts")
async def get_question_answer_vote_counts(request: Request, question_id: int):
    counts = db.get_question_answer_and_vote_counts(question_id=question_id)

    if not counts:
        raise exceptions.NotFound("Question not found.")

    return json(body=counts)


@app.get("/questions/most-answered")
async def get_most_answered_questions(request: Request):
    offset = int(request.args.get("offset", 0))
    limit = int(request.args.get("limit", 10))

    questions = db.get_most_answered_questions(offset=offset, limit=limit)
    
    if not questions:    
        raise exceptions.NotFound("No questions found.")
    
    return json(body=questions)


@app.get("/questions/most-answered/by-city/<city_id:int>")
async def get_most_answered_questions_by_city(request: Request, city_id: int):
    offset = int(request.args.get("offset", 0))
    limit = int(request.args.get("limit", 10))

    questions = db.get_most_answered_questions_in_city(city_id=city_id, offset=offset, limit=limit)
    
    if not questions:    
        raise exceptions.NotFound("No questions found for the specified city.")
    
    return json(body=questions)


@app.get("/questions/most-answered/by-country/<country_id:int>")
async def get_most_answered_questions_by_country(request: Request, country_id: int):
    offset = int(request.args.get("offset", 0))
    limit = int(request.args.get("limit", 10))

    questions = db.get_most_answered_questions_in_country(country_id=country_id, offset=offset, limit=limit)
    
    if not questions:    
        raise exceptions.NotFound("No questions found for the specified country.")
    
    return json(body=questions)


@app.get("/questions/recent")
async def get_recent_questions(request: Request):
    offset = int(request.args.get("offset", 0))
    limit = int(request.args.get("limit", 10))

    questions = db.get_recent_questions(offset=offset, limit=limit)
    
    if not questions:    
        raise exceptions.NotFound("No questions found.")
    
    return json(body=questions)


@app.get("/questions/recent/by-city/<city_id:int>")
async def get_recent_questions_by_city(request: Request, city_id: int):
    offset = int(request.args.get("offset", 0))
    limit = int(request.args.get("limit", 10))

    questions = db.get_recent_questions_of_city(city_id=city_id, offset=offset, limit=limit)
    
    if not questions:    
        raise exceptions.NotFound("No questions found for the specified city.")
    
    return json(body=questions)


@app.get("/questions/recent/by-country/<country_id:int>")
async def get_recent_questions_by_country(request: Request, country_id: int):
    offset = int(request.args.get("offset", 0))
    limit = int(request.args.get("limit", 10))

    questions = db.get_recent_questions_of_country(country_id=country_id, offset=offset, limit=limit)
    
    if not questions:    
        raise exceptions.NotFound("No questions found for the specified country.")
    
    return json(body=questions)


@app.get("/questions/by-user/<username:str>")
async def get_questions_by_user(request: Request, username: str):
    offset = int(request.args.get("offset", 0))
    limit = int(request.args.get("limit", 10))

    questions = db.get_questions_of_user(username=username, offset=offset, limit=limit)
    
    if not questions:    
        raise exceptions.NotFound("No questions found for the specified user.")
    
    return json(body=questions)



# Search endpoints

@app.get("/search/cities/<query:str>")
async def search_cities(request: Request, query: str):
    offset = int(request.args.get("offset", 0))
    limit = int(request.args.get("limit", 10))

    cities = db.get_cities_matching_query(query_string=query, offset=offset, limit=limit)

    if not cities:
        raise exceptions.NotFound("No cities found matching the query.")

    return json(body=cities)


@app.get("/search/countries/<query:str>")
async def search_countries(request: Request, query: str):
    offset = int(request.args.get("offset", 0))
    limit = int(request.args.get("limit", 10))

    countries = db.get_countries_matching_query(query_string=query, offset=offset, limit=limit)

    if not countries:
        raise exceptions.NotFound("No countries found matching the query.")

    return json(body=countries)


@app.get("/search/questions/<query:str>")
async def search_questions(request: Request, query: str):
    offset = int(request.args.get("offset", 0))
    limit = int(request.args.get("limit", 10))

    questions = db.get_questions_matching_query(query_string=query, offset=offset, limit=limit)

    if not questions:
        raise exceptions.NotFound("No questions found matching the query.")

    return json(body=questions)



# Answers endpoints

@app.get("/answers/<answer_id:int>")
async def get_specific_answer(request: Request, answer_id: int):
    answer = db.get_specific_answer(answer_id=answer_id)

    if not answer:
        raise exceptions.NotFound("Answer not found.")

    return json(body=answer)


@app.get("/answers/<answer_id:int>/counts")
async def get_answer_vote_reply_counts(request: Request, answer_id: int):
    counts = db.get_answer_vote_and_reply_counts(answer_id=answer_id)

    if not counts:
        raise exceptions.NotFound("Answer not found.")

    return json(body=counts)


@app.get("/answers/by-question/<question_id:int>")
async def get_answers_by_question(request: Request, question_id: int):
    offset = int(request.args.get("offset", 0))
    limit = int(request.args.get("limit", 10))

    answers = db.get_answers_of_specific_question(question_id=question_id, offset=offset, limit=limit)

    if not answers:
        raise exceptions.NotFound("No answers found for the specified question.")

    return json(body=answers)


@app.get("/answers/by-user/<username:str>")
async def get_answers_by_user(request: Request, username: str):
    offset = int(request.args.get("offset", 0))
    limit = int(request.args.get("limit", 10))

    answers = db.get_answers_of_user(username=username, offset=offset, limit=limit)

    if not answers:
        raise exceptions.NotFound("No answers found for the specified user.")

    return json(body=answers)



# Replies endpoints

@app.get("/replies/<reply_id:int>")
async def get_specific_reply(request: Request, reply_id: int):
    reply = db.get_specific_reply(reply_id=reply_id)

    if not reply:
        raise exceptions.NotFound("Reply not found.")

    return json(body=reply)


@app.get("/replies/by-answer/<answer_id:int>")
async def get_replies_of_answer(request: Request, answer_id: int):
    offset = int(request.args.get("offset", 0))
    limit = int(request.args.get("limit", 10))

    replies = db.get_replies_of_specific_answer(answer_id=answer_id, offset=offset, limit=limit)

    if not replies:
        raise exceptions.NotFound("No replies found for the specified answer.")

    return json(body=replies)


@app.get("/replies/<reply_id:int>/counts")
async def get_reply_vote_counts(request: Request, reply_id: int):
    counts = db.get_vote_counts_for_specific_reply(reply_id=reply_id)

    if not counts:
        raise exceptions.NotFound("Reply not found.")

    return json(body=counts)


@app.get("/replies/by-user/<username:str>")
async def get_replies_of_user(request: Request, username: str):
    offset = int(request.args.get("offset", 0))
    limit = int(request.args.get("limit", 10))

    replies = db.get_replies_of_user(username=username, offset=offset, limit=limit)

    if not replies:
        raise exceptions.NotFound("No replies found for the specified user.")

    return json(body=replies)



# Categories endpoints

@app.get("/categories")
async def get_all_categories(request: Request):
    categories = db.get_all_categories()

    if not categories:
        raise exceptions.NotFound("No categories found.")

    return json(body=categories)


@app.get("/categories/<question_id:int>")
async def get_categories_of_question(request: Request, question_id: int):
    categories = db.get_categories_of_question(question_id=question_id)

    if not categories:
        raise exceptions.NotFound("No categories found for the specified question.")

    return json(body=categories)


@app.get("/categories/<category_id:int>")
async def get_specific_category(request: Request, category_id: int):
    category = db.get_specific_category(category_id=category_id)

    if not category:
        raise exceptions.NotFound("Category not found.")

    return json(body=category)


@app.get("/categories/by-city/<city_id:int>")
async def get_categories_with_stats_in_city(request: Request, city_id: int):
    categories = db.get_all_categories_of_city_with_stats(city_id=city_id)

    if not categories:
        raise exceptions.NotFound("No categories found for the specified city.")

    return json(body=categories)


@app.get("/categories/by-country/<country_id:int>")
async def get_categories_with_stats_in_country(request: Request, country_id: int):
    categories = db.get_all_categories_of_country_with_stats(country_id=country_id)

    if not categories:
        raise exceptions.NotFound("No categories found for the specified country.")

    return json(body=categories)



# User endpoints

@app.get("/users/<user_id:int>/info")
async def get_user_info(request: Request, user_id: int):
    check_token(request, user_id)

    user_info = db.get_user_info(user_id=user_id)

    if not user_info:
        raise exceptions.NotFound("User not found.")

    return json(body=user_info)



# Votes endpoints

# TODO: Change return JSON in Swagger documentation in all votes GETs
@app.get("/votes/questions/<question_id:int>/<user_id:int>")
async def get_user_vote_for_question(request: Request, question_id: int, user_id: int):
    check_token(request, user_id)

    vote = db.get_user_vote_for_question(user_id=user_id, question_id=question_id)

    return json(body={"vote": vote})


@app.get("/votes/answers/<answer_id:int>/<user_id:int>")
async def get_user_vote_for_answer(request: Request, answer_id: int, user_id: int):
    check_token(request, user_id)

    vote = db.get_user_vote_for_answer(user_id=user_id, answer_id=answer_id)

    return json(body={"vote": vote})


@app.get("/votes/replies/<reply_id:int>/<user_id:int>")
async def get_user_vote_for_reply(request: Request, reply_id: int, user_id: int):
    check_token(request, user_id)

    vote = db.get_user_vote_for_reply(user_id=user_id, reply_id=reply_id)

    return json(body={"vote": vote})



# Subscriptions endpoints

@app.get("/subscriptions/questions/<user_id:int>")
async def get_user_questions_from_subscriptions(request: Request, user_id: int):
    check_token(request, user_id)

    offset = int(request.args.get("offset", 0))
    limit = int(request.args.get("limit", 10))

    questions = db.get_questions_from_subscriptions(user_id=user_id, offset=offset, limit=limit)

    if not questions:
        raise exceptions.NotFound("No questions found from subscriptions.")

    return json(body=questions)


@app.get("/subscriptions/cities/<user_id:int>")
async def get_user_city_subscriptions(request: Request, user_id: int):
    check_token(request, user_id)

    cities = db.get_subscribed_cities(user_id=user_id)

    if not cities:
        raise exceptions.NotFound("No city subscriptions found for the user.")

    return json(body=cities)


@app.get("/subscriptions/countries/<user_id:int>")
async def get_user_country_subscriptions(request: Request, user_id: int):
    check_token(request, user_id)

    countries = db.get_subscribed_countries(user_id=user_id)

    if not countries:
        raise exceptions.NotFound("No country subscriptions found for the user.")

    return json(body=countries)