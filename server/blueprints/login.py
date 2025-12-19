from sanic import Blueprint, Request, exceptions, json
import jwt

bp = Blueprint("Login", url_prefix="/login")

@bp.post("/")
async def get_token(request: Request):
    username = request.json.get("username")
    password = request.json.get("password")
    
    if not username or not password:
        raise exceptions.InvalidUsage("Username and password are required.")
    
    if not request.app.ctx.db.get_user_exists(username) or not request.app.ctx.db.get_user_password_match(username, password):
        raise exceptions.Unauthorized("Invalid username or password.")

    client_token = jwt.encode({"user_id": request.app.ctx.db.get_user_id(username)}, key="SERVER_SECRET", algorithm="HS256")

    return json(body={"token": client_token})