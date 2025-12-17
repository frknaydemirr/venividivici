from sanic import Blueprint, Request, exceptions, json

bp = Blueprint("Users", url_prefix="/users")

@bp.get("/<username:str>/info")
async def get_user_info(request: Request, username: str):
    user_info = request.app.ctx.db.get_user_info(username=username)

    if not user_info:
        raise exceptions.NotFound("User not found.")

    return json(body=user_info)