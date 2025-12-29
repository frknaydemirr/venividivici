from sanic import Blueprint, Request, exceptions, json
import jwt
import asyncio


bp = Blueprint("Login", url_prefix="/login")

@bp.post("/")
async def get_token(request: Request):
    username = request.json.get("username")
    password = request.json.get("password")
    
    if not username or not password:
        raise exceptions.InvalidUsage("Username and password are required.")
    
    user_exists = await asyncio.to_thread(request.app.ctx.db.get_user_exists, username)
    user_password_match = await asyncio.to_thread(request.app.ctx.db.get_user_password_match, username, password)
    if not user_exists or not user_password_match:
        raise exceptions.Unauthorized("Invalid username or password.")

    user_id = await asyncio.to_thread(request.app.ctx.db.get_user_id, username)
    client_token = jwt.encode({"user_id": user_id}, key="SERVER_SECRET", algorithm="HS256")

    return json(body={"token": client_token})