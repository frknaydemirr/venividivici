from sanic import Request, exceptions
import jwt
import asyncio

async def check_token(request: Request) -> int:
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise exceptions.Unauthorized("Authorization header missing or invalid.")
    
    token = auth_header.split(" ")[1]
    try:
        decoded_token = jwt.decode(token, key="SERVER_SECRET", algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise exceptions.Unauthorized("Token has expired.")
    except jwt.InvalidTokenError:
        raise exceptions.Unauthorized("Invalid token.")
    
    user_exists = await asyncio.to_thread(request.app.ctx.db.get_user_exists_by_id, decoded_token.get("user_id"))
    if not user_exists:
        raise exceptions.Unauthorized("Invalid token.")

    return decoded_token.get("user_id")