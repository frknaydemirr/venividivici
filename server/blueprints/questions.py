from sanic import Blueprint, Request, exceptions, json
from server.common.check_token import check_token

bp = Blueprint("Questions", url_prefix="/questions")

@bp.delete("/<question_id:int>")
async def delete_question(request: Request, question_id: int):
    user_id = check_token(request)

    question = request.app.ctx.db.get_specific_question(question_id=question_id)
    
    if request.app.ctx.db.get_user_id(question["username"]) != user_id:
        raise exceptions.Forbidden("You do not have permission to delete this question.")

    request.app.ctx.db.delete_specific_question(question_id=question_id)

    return json(body={"status": "SUCCESS"})


@bp.post("/")
async def post_new_question(request: Request):
    user_id = check_token(request)
    
    new_question_id = request.app.ctx.db.post_new_question(
        user_id=user_id,
        city_id=request.json["city-id"],
        question_title=request.json["question-title"],
        question_body=request.json["question-body"],
        category_ids=request.json["category-ids"]
    )

    return json(body={"question-id": new_question_id})

@bp.get("/<question_id:int>")
async def get_specific_question(request: Request, question_id: int):
    question = request.app.ctx.db.get_specific_question(question_id=question_id)

    if not question:
        raise exceptions.NotFound("Question not found.")

    return json(body=question)


@bp.get("/<question_id:int>/counts")
async def get_question_answer_vote_counts(request: Request, question_id: int):
    counts = request.app.ctx.db.get_question_answer_and_vote_counts(question_id=question_id)

    if not counts:
        raise exceptions.NotFound("Question not found.")

    return json(body=counts)


@bp.get("/most-answered")
async def get_most_answered_questions(request: Request):
    offset = int(request.args.get("offset", 0))
    limit = int(request.args.get("limit", 10))

    questions = request.app.ctx.db.get_most_answered_questions(offset=offset, limit=limit)
    
    if not questions:    
        raise exceptions.NotFound("No questions found.")
    
    return json(body=questions)


@bp.get("/most-answered/by-city/<city_id:int>")
async def get_most_answered_questions_by_city(request: Request, city_id: int):
    offset = int(request.args.get("offset", 0))
    limit = int(request.args.get("limit", 10))

    questions = request.app.ctx.db.get_most_answered_questions_in_city(city_id=city_id, offset=offset, limit=limit)
    
    if not questions:    
        raise exceptions.NotFound("No questions found for the specified city.")
    
    return json(body=questions)


@bp.get("/most-answered/by-country/<country_id:int>")
async def get_most_answered_questions_by_country(request: Request, country_id: int):
    offset = int(request.args.get("offset", 0))
    limit = int(request.args.get("limit", 10))

    questions = request.app.ctx.db.get_most_answered_questions_in_country(country_id=country_id, offset=offset, limit=limit)
    
    if not questions:    
        raise exceptions.NotFound("No questions found for the specified country.")
    
    return json(body=questions)


@bp.get("/recent")
async def get_recent_questions(request: Request):
    offset = int(request.args.get("offset", 0))
    limit = int(request.args.get("limit", 10))

    questions = request.app.ctx.db.get_recent_questions(offset=offset, limit=limit)
    
    if not questions:    
        raise exceptions.NotFound("No questions found.")
    
    return json(body=questions)


@bp.get("/recent/by-city/<city_id:int>")
async def get_recent_questions_by_city(request: Request, city_id: int):
    offset = int(request.args.get("offset", 0))
    limit = int(request.args.get("limit", 10))

    questions = request.app.ctx.db.get_recent_questions_of_city(city_id=city_id, offset=offset, limit=limit)
    
    if not questions:    
        raise exceptions.NotFound("No questions found for the specified city.")
    
    return json(body=questions)


@bp.get("/recent/by-country/<country_id:int>")
async def get_recent_questions_by_country(request: Request, country_id: int):
    offset = int(request.args.get("offset", 0))
    limit = int(request.args.get("limit", 10))

    questions = request.app.ctx.db.get_recent_questions_of_country(country_id=country_id, offset=offset, limit=limit)
    
    if not questions:    
        raise exceptions.NotFound("No questions found for the specified country.")
    
    return json(body=questions)


@bp.get("/by-user/<username:str>")
async def get_questions_by_user(request: Request, username: str):
    offset = int(request.args.get("offset", 0))
    limit = int(request.args.get("limit", 10))

    questions = request.app.ctx.db.get_questions_of_user(username=username, offset=offset, limit=limit)
    
    if not questions:    
        raise exceptions.NotFound("No questions found for the specified user.")
    
    return json(body=questions)
