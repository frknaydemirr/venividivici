from sanic import Blueprint, Request, exceptions, json
import json as json_lib

from server.common.datetime_json import datetime_to_json_formatting

import asyncio

bp = Blueprint("Countries", url_prefix="/countries")

@bp.get("/")
async def get_all_countries(request: Request):
    r = request.app.ctx.redis

    cached = await r.get("all_countries")
    if cached:
        return json(body=json_lib.loads(cached))

    countries = await asyncio.to_thread(request.app.ctx.db.get_all_countries)

    if not countries:
        raise exceptions.NotFound("No countries found.")

    await r.set("all_countries", json_lib.dumps(countries, default=datetime_to_json_formatting), ex=3600)  # Cache for 1 hour
    return json(body=countries)


@bp.get("/<country_id:int>/counts")
async def get_country_qa_counts(request: Request, country_id: int):
    r = request.app.ctx.redis

    cached = await r.get(f"{country_id}_country_qa_counts")
    if cached:
        return json(body=json_lib.loads(cached))

    counts = await asyncio.to_thread(request.app.ctx.db.get_country_question_and_answer_counts, country_id=country_id)

    if not counts:
        raise exceptions.NotFound("Country not found.")

    await r.set(f"{country_id}_country_qa_counts", json_lib.dumps(counts, default=datetime_to_json_formatting), ex=600)  # Cache for 10 minutes
    return json(body=counts)


@bp.get("/<country_id:int>")
async def get_country(request: Request, country_id: int):
    country = await asyncio.to_thread(request.app.ctx.db.get_specific_country, country_id=country_id)

    if not country:
        raise exceptions.NotFound("Country not found.")

    return json(body=country)


@bp.get("/most-conquered")
async def get_most_conquered_countries(request: Request):
    r = request.app.ctx.redis
    
    cached = await r.get("most_conquered_countries")
    if cached:
        return json(body=json_lib.loads(cached))

    limit = int(request.args.get("limit", 10))

    countries = await asyncio.to_thread(request.app.ctx.db.get_most_conquered_countries, limit=limit)

    if not countries:
        raise exceptions.NotFound("No countries found.")

    await r.set("most_conquered_countries", json_lib.dumps(countries, default=datetime_to_json_formatting), ex=600)  # Cache for 10 minutes
    return json(body=countries)