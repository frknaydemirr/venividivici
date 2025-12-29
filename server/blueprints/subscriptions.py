from sanic import Blueprint, Request, exceptions, json
from server.common.check_token import check_token

from server.common.check_schema import check_schema
from server.common.schemas.subscriptions import post_city_sub_unsub_schema, post_country_sub_unsub_schema

import asyncio

bp = Blueprint("Subscriptions", url_prefix="/subscriptions")

@bp.get("/questions")
async def get_user_questions_from_subscriptions(request: Request):
    user_id = await check_token(request)

    offset = int(request.args.get("offset", 0))
    limit = int(request.args.get("limit", 10))

    questions = await asyncio.to_thread(request.app.ctx.db.get_questions_from_subscriptions, user_id=user_id, offset=offset, limit=limit)

    if not questions:
        raise exceptions.NotFound("No questions found from subscriptions.")

    return json(body=questions)


@bp.get("/cities")
async def get_user_city_subscriptions(request: Request):
    user_id = await check_token(request)

    cities = await asyncio.to_thread(request.app.ctx.db.get_subscribed_cities, user_id=user_id)

    if not cities:
        raise exceptions.NotFound("No city subscriptions found for the user.")

    return json(body=cities)


@bp.post("/cities")
async def post_user_city_subscription(request: Request):
    await asyncio.to_thread(check_schema, request.json, post_city_sub_unsub_schema)

    user_id = await check_token(request)

    city_id = request.json["city-id"]
    subscription_type = request.json["subscription-type"]
    if subscription_type not in [True, False]:
        raise exceptions.InvalidUsage("Invalid subscription action.")

    await asyncio.to_thread(request.app.ctx.db.post_subscribe_city, user_id=user_id, city_id=city_id, subscription_type=subscription_type)

    return json(body={"status": "SUCCESS"})


@bp.get("/countries")
async def get_user_country_subscriptions(request: Request):
    user_id = await check_token(request)

    countries = await asyncio.to_thread(request.app.ctx.db.get_subscribed_countries, user_id=user_id)

    if not countries:
        raise exceptions.NotFound("No country subscriptions found for the user.")

    return json(body=countries)


@bp.post("/countries")
async def post_user_country_subscription(request: Request):
    await asyncio.to_thread(check_schema, request.json, post_country_sub_unsub_schema)

    user_id = await check_token(request)

    country_id = request.json["country-id"]
    subscription_type = request.json["subscription-type"]
    if subscription_type not in [True, False]:
        raise exceptions.InvalidUsage("Invalid subscription action.")

    await asyncio.to_thread(request.app.ctx.db.post_subscribe_country, user_id=user_id, country_id=country_id, subscription_type=subscription_type)

    return json(body={"status": "SUCCESS"})