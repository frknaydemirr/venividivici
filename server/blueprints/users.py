from sanic import Blueprint, Request, exceptions, json
from server.common.datetime_json import datetime_to_json_formatting

import asyncio

bp = Blueprint("Users", url_prefix="/users")

@bp.get("/<username:str>/info")
async def get_user_info(request: Request, username: str):
    user_info = await asyncio.to_thread(request.app.ctx.db.get_user_info, username=username)

    if not user_info:
        raise exceptions.NotFound("User not found.")

    return json(body=user_info, default=datetime_to_json_formatting)