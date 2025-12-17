from sanic import Blueprint, Request, exceptions, json
from common.check_token import check_token

bp = Blueprint("Votes", url_prefix="/votes")

@bp.delete("/questions/<question_id:int>")
async def delete_user_vote_for_question(request: Request, question_id: int):
    user_id = check_token(request)

    request.app.ctx.db.delete_user_vote_for_question(user_id=user_id, question_id=question_id)

    return json(body={"status": "SUCCESS"})


@bp.get("/questions/<question_id:int>")
async def get_user_vote_for_question(request: Request, question_id: int):
    user_id = check_token(request)

    vote = request.app.ctx.db.get_user_vote_for_question(user_id=user_id, question_id=question_id)

    return json(body={"vote-type": vote})


@bp.post("/questions/<question_id:int>")
async def post_user_vote_for_question(request: Request, question_id: int):
    user_id = check_token(request)

    vote_type = request.json["vote-type"]
    if vote_type not in [True, False]:
        raise exceptions.InvalidUsage("Invalid vote type. Must be upvote or downvote.")

    request.app.ctx.db.post_user_vote_for_question(user_id=user_id, question_id=question_id, vote_type=vote_type)

    return json(body={"status": "SUCCESS"})


@bp.delete("/answers/<answer_id:int>")
async def delete_user_vote_for_answer(request: Request, answer_id: int):
    user_id = check_token(request)

    request.app.ctx.db.delete_user_vote_for_answer(user_id=user_id, answer_id=answer_id)

    return json(body={"status": "SUCCESS"})


@bp.get("/answers/<answer_id:int>")
async def get_user_vote_for_answer(request: Request, answer_id: int):
    user_id = check_token(request)

    vote = request.app.ctx.db.get_user_vote_for_answer(user_id=user_id, answer_id=answer_id)

    return json(body={"vote-type": vote})


@bp.post("/answers/<answer_id:int>")
async def post_user_vote_for_answer(request: Request, answer_id: int):
    user_id = check_token(request)

    vote_type = request.json["vote-type"]
    if vote_type not in [True, False]:
        raise exceptions.InvalidUsage("Invalid vote type. Must be upvote or downvote.")

    request.app.ctx.db.post_user_vote_for_answer(user_id=user_id, answer_id=answer_id, vote_type=vote_type)

    return json(body={"status": "SUCCESS"})


@bp.delete("/replies/<reply_id:int>")
async def delete_user_vote_for_reply(request: Request, reply_id: int):
    user_id = check_token(request)

    request.app.ctx.db.delete_user_vote_for_reply(user_id=user_id, reply_id=reply_id)

    return json(body={"status": "SUCCESS"})


@bp.get("/replies/<reply_id:int>")
async def get_user_vote_for_reply(request: Request, reply_id: int):
    user_id = check_token(request, user_id)

    vote = request.app.ctx.db.get_user_vote_for_reply(user_id=user_id, reply_id=reply_id)

    return json(body={"vote-type": vote})


@bp.post("/replies/<reply_id:int>")
async def post_user_vote_for_reply(request: Request, reply_id: int):
    user_id = check_token(request)

    vote_type = request.json["vote-type"]
    if vote_type not in [True, False]:
        raise exceptions.InvalidUsage("Invalid vote type. Must be upvote or downvote.")

    request.app.ctx.db.post_user_vote_for_reply(user_id=user_id, reply_id=reply_id, vote_type=vote_type)

    return json(body={"status": "SUCCESS"})