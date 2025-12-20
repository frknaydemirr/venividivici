from sanic import Blueprint, Request, exceptions, json
from server.common.check_token import check_token
from server.common.datetime_json import datetime_to_json_formatting

bp = Blueprint("Answers", url_prefix="/answers")

@bp.delete("/<answer_id:int>")
async def delete_answer(request: Request, answer_id: int):
    user_id = check_token(request)

    answer = request.app.ctx.db.get_specific_answer(answer_id=answer_id)
    
    if request.app.ctx.db.get_user_id(answer["username"]) != user_id:
        raise exceptions.Forbidden("You do not have permission to delete this answer.")

    request.app.ctx.db.delete_specific_answer(answer_id=answer_id)

    return json(body={"status": "SUCCESS"})


@bp.post("/")
async def post_new_answer(request: Request):
    user_id = check_token(request)
    
    new_answer_id = request.app.ctx.db.post_new_answer(
        user_id=user_id,
        question_id=request.json["question-id"],
        answer_body=request.json["answer-body"]
    )

    return json(body={"answer-id": new_answer_id})


@bp.get("/<answer_id:int>")
async def get_specific_answer(request: Request, answer_id: int):
    answer = request.app.ctx.db.get_specific_answer(answer_id=answer_id)

    if not answer:
        raise exceptions.NotFound("Answer not found.")

    return json(body=answer, default=datetime_to_json_formatting)


@bp.get("/<answer_id:int>/counts")
async def get_answer_vote_reply_counts(request: Request, answer_id: int):
    counts = request.app.ctx.db.get_answer_vote_and_reply_counts(answer_id=answer_id)

    if not counts:
        raise exceptions.NotFound("Answer not found.")

    return json(body=counts)


@bp.get("/by-question/<question_id:int>")
async def get_answers_by_question(request: Request, question_id: int):
    offset = int(request.args.get("offset", 0))
    limit = int(request.args.get("limit", 10))

    answers = request.app.ctx.db.get_answers_of_specific_question(question_id=question_id, offset=offset, limit=limit)

    if not answers:
        raise exceptions.NotFound("No answers found for the specified question.")

    return json(body=answers)


@bp.get("/by-user/<username:str>")
async def get_answers_by_user(request: Request, username: str):
    offset = int(request.args.get("offset", 0))
    limit = int(request.args.get("limit", 10))

    answers = request.app.ctx.db.get_answers_of_user(username=username, offset=offset, limit=limit)

    if not answers:
        raise exceptions.NotFound("No answers found for the specified user.")

    return json(body=answers)