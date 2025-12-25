from sanic import Blueprint, Request, exceptions, json
from server.common.check_token import check_token
from server.common.datetime_json import datetime_to_json_formatting

from server.common.check_schema import check_schema
from server.common.schemas.replies import post_reply_schema

import asyncio

bp = Blueprint("Replies", url_prefix="/replies")

@bp.delete("/<reply_id:int>")
async def delete_reply(request: Request, reply_id: int):
    user_id = await check_token(request)

    reply = await asyncio.to_thread(request.app.ctx.db.get_specific_reply, reply_id=reply_id)
    
    if not reply:
        raise exceptions.NotFound("Reply not found.")

    user_id_of_username = await asyncio.to_thread(request.app.ctx.db.get_user_id, reply["username"])
    if user_id_of_username != user_id:
        raise exceptions.Forbidden("You do not have permission to delete this reply.")

    await asyncio.to_thread(request.app.ctx.db.delete_specific_reply, reply_id=reply_id)

    return json(body={"status": "SUCCESS"})


@bp.post("/")
async def post_new_reply(request: Request):
    await asyncio.to_thread(check_schema, request.json, post_reply_schema)

    user_id = await check_token(request)
    
    new_reply_id = await asyncio.to_thread(request.app.ctx.db.post_new_reply,
        user_id=user_id,
        answer_id=request.json["answer-id"],
        reply_body=request.json["reply-body"]
    )

    return json(body={"reply-id": new_reply_id})


@bp.get("/<reply_id:int>")
async def get_specific_reply(request: Request, reply_id: int):
    reply = await asyncio.to_thread(request.app.ctx.db.get_specific_reply, reply_id=reply_id)

    if not reply:
        raise exceptions.NotFound("Reply not found.")

    return json(body=reply, default=datetime_to_json_formatting)


@bp.get("/by-answer/<answer_id:int>")
async def get_replies_of_answer(request: Request, answer_id: int):
    offset = int(request.args.get("offset", 0))
    limit = int(request.args.get("limit", 10))

    replies = await asyncio.to_thread(request.app.ctx.db.get_replies_of_specific_answer, answer_id=answer_id, offset=offset, limit=limit)

    if not replies:
        raise exceptions.NotFound("No replies found for the specified answer.")

    return json(body=replies, default=datetime_to_json_formatting)


@bp.get("/<reply_id:int>/counts")
async def get_reply_vote_counts(request: Request, reply_id: int):
    counts = await asyncio.to_thread(request.app.ctx.db.get_vote_counts_for_specific_reply, reply_id=reply_id)

    if not counts:
        raise exceptions.NotFound("Reply not found.")

    return json(body=counts)


@bp.get("/by-user/<username:str>")
async def get_replies_of_user(request: Request, username: str):
    offset = int(request.args.get("offset", 0))
    limit = int(request.args.get("limit", 10))

    replies = await asyncio.to_thread(request.app.ctx.db.get_replies_of_user, username=username, offset=offset, limit=limit)

    if not replies:
        raise exceptions.NotFound("No replies found for the specified user.")

    return json(body=replies, default=datetime_to_json_formatting)