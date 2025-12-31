from sanic import Blueprint, Request, exceptions, json
from server.common.check_token import check_token
from server.common.datetime_json import datetime_to_json_formatting

from server.common.check_schema import check_schema
from server.common.schemas.questions import post_question_schema

import json as json_lib

import asyncio

bp = Blueprint("Questions", url_prefix="/questions")

@bp.delete("/<question_id:int>")
async def delete_question(request: Request, question_id: int):
    user_id = await check_token(request)

    question = await asyncio.to_thread(request.app.ctx.db.get_specific_question, question_id=question_id)
    
    if not question:
        raise exceptions.NotFound("Question not found.")

    user_id_of_username = await asyncio.to_thread(request.app.ctx.db.get_user_id, question["username"])
    if user_id_of_username != user_id:
        raise exceptions.Forbidden("You do not have permission to delete this question.")

    await asyncio.to_thread(request.app.ctx.db.delete_specific_question, question_id=question_id)

    return json(body={"status": "SUCCESS"})


@bp.post("/")
async def post_new_question(request: Request):
    await asyncio.to_thread(check_schema, request.json, post_question_schema)

    user_id = await check_token(request)
    
    new_question_id = await asyncio.to_thread(request.app.ctx.db.post_new_question,
        user_id=user_id,
        city_id=request.json["city-id"],
        question_title=request.json["question-title"],
        question_body=request.json["question-body"],
        category_ids=request.json["category-ids"]
    )

    return json(body={"question-id": new_question_id})

@bp.get("/<question_id:int>")
async def get_specific_question(request: Request, question_id: int):
    question = await asyncio.to_thread(request.app.ctx.db.get_specific_question, question_id=question_id)

    if not question:
        raise exceptions.NotFound("Question not found.")

    return json(body=question, default=datetime_to_json_formatting)


@bp.get("/<question_id:int>/counts")
async def get_question_answer_vote_counts(request: Request, question_id: int):
    counts = await asyncio.to_thread(request.app.ctx.db.get_question_answer_and_vote_counts, question_id=question_id)

    if not counts:
        raise exceptions.NotFound("Question not found.")

    return json(body=counts, default=datetime_to_json_formatting)


@bp.get("/most-answered")
async def get_most_answered_questions(request: Request):
    r = request.app.ctx.redis

    cached = await r.get("most_answered_questions")
    if cached:
        return json(body=json_lib.loads(cached))

    offset = int(request.args.get("offset", 0))
    limit = int(request.args.get("limit", 10))

    questions = await asyncio.to_thread(request.app.ctx.db.get_most_answered_questions, offset=offset, limit=limit)
    
    if not questions:    
        raise exceptions.NotFound("No questions found.")
    
    await r.set("most_answered_questions", json_lib.dumps(questions, default=datetime_to_json_formatting), ex=600)  # Cache for 10 minutes
    return json(body=questions, default=datetime_to_json_formatting)


@bp.get("/most-answered/by-city/<city_id:int>")
async def get_most_answered_questions_by_city(request: Request, city_id: int):
    r = request.app.ctx.redis

    cached = await r.get(f"{city_id}_city_most_answered_questions")
    if cached:
        return json(body=json_lib.loads(cached))

    offset = int(request.args.get("offset", 0))
    limit = int(request.args.get("limit", 10))

    questions = await asyncio.to_thread(request.app.ctx.db.get_most_answered_questions_in_city, city_id=city_id, offset=offset, limit=limit)
    
    if not questions:    
        raise exceptions.NotFound("No questions found for the specified city.")
    
    await r.set(f"{city_id}_city_most_answered_questions", json_lib.dumps(questions, default=datetime_to_json_formatting), ex=600)  # Cache for 10 minutes
    return json(body=questions, default=datetime_to_json_formatting)


@bp.get("/most-answered/by-country/<country_id:int>")
async def get_most_answered_questions_by_country(request: Request, country_id: int):
    r = request.app.ctx.redis

    cached = await r.get(f"{country_id}_country_most_answered_questions")
    if cached:
        return json(body=json_lib.loads(cached))

    offset = int(request.args.get("offset", 0))
    limit = int(request.args.get("limit", 10))

    questions = await asyncio.to_thread(request.app.ctx.db.get_most_answered_questions_in_country, country_id=country_id, offset=offset, limit=limit)
    
    if not questions:    
        raise exceptions.NotFound("No questions found for the specified country.")
    
    await r.set(f"{country_id}_country_most_answered_questions", json_lib.dumps(questions, default=datetime_to_json_formatting), ex=600)  # Cache for 10 minutes
    return json(body=questions, default=datetime_to_json_formatting)


@bp.get("/recent")
async def get_recent_questions(request: Request):
    r = request.app.ctx.redis

    cached = await r.get("recent_questions")
    if cached:
        return json(body=json_lib.loads(cached))

    offset = int(request.args.get("offset", 0))
    limit = int(request.args.get("limit", 10))

    questions = await asyncio.to_thread(request.app.ctx.db.get_recent_questions, offset=offset, limit=limit)
    
    if not questions:    
        raise exceptions.NotFound("No questions found.")
    
    await r.set("recent_questions", json_lib.dumps(questions, default=datetime_to_json_formatting), ex=600)  # Cache for 10 minutes
    return json(body=questions, default=datetime_to_json_formatting)


@bp.get("/recent/by-city/<city_id:int>")
async def get_recent_questions_by_city(request: Request, city_id: int):
    r = request.app.ctx.redis

    cached = await r.get(f"{city_id}_city_recent_questions")
    if cached:
        return json(body=json_lib.loads(cached))

    offset = int(request.args.get("offset", 0))
    limit = int(request.args.get("limit", 10))

    questions = await asyncio.to_thread(request.app.ctx.db.get_recent_questions_of_city, city_id=city_id, offset=offset, limit=limit)
    
    if not questions:    
        raise exceptions.NotFound("No questions found for the specified city.")
    
    await r.set(f"{city_id}_city_recent_questions", json_lib.dumps(questions, default=datetime_to_json_formatting), ex=600)  # Cache for 10 minutes
    return json(body=questions, default=datetime_to_json_formatting)


@bp.get("/recent/by-country/<country_id:int>")
async def get_recent_questions_by_country(request: Request, country_id: int):
    r = request.app.ctx.redis

    cached = await r.get(f"{country_id}_country_recent_questions")
    if cached:
        return json(body=json_lib.loads(cached))

    offset = int(request.args.get("offset", 0))
    limit = int(request.args.get("limit", 10))

    questions = await asyncio.to_thread(request.app.ctx.db.get_recent_questions_of_country, country_id=country_id, offset=offset, limit=limit)
    
    if not questions:    
        raise exceptions.NotFound("No questions found for the specified country.")
    
    await r.set(f"{country_id}_country_recent_questions", json_lib.dumps(questions, default=datetime_to_json_formatting), ex=600)  # Cache for 10 minutes
    return json(body=questions, default=datetime_to_json_formatting)


@bp.get("/by-user/<username:str>")
async def get_questions_by_user(request: Request, username: str):
    offset = int(request.args.get("offset", 0))
    limit = int(request.args.get("limit", 10))

    questions = await asyncio.to_thread(request.app.ctx.db.get_questions_of_user, username=username, offset=offset, limit=limit)
    
    if not questions:    
        raise exceptions.NotFound("No questions found for the specified user.")
    
    return json(body=questions, default=datetime_to_json_formatting)
