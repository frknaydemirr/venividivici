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


@bp.post("/register")
async def register_user(request: Request):
    db = request.app.ctx.db
    
    if db.get_user_exists(request.json.get("username")):
        raise exceptions.BadRequest("Username already exists.")

    if db.get_email_exists(request.json.get("e-mail-addr")):
        raise exceptions.BadRequest("E-mail address already registered.")

    if db.get_valid_password(request.json.get("password")) is False:
        raise exceptions.BadRequest("Password does not meet complexity requirements.")

    await asyncio.to_thread(db.post_register_user,
        username=request.json["username"],
        e_mail_addr=request.json["e-mail-addr"],
        password=request.json["password"],
        full_name=request.json.get("full-name"),
        city_id=request.json.get("city-id")
    )

    return json(body={})