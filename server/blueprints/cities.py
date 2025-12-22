from sanic import Blueprint, Request, exceptions, json
import json as json_lib

bp = Blueprint("Cities", url_prefix="/cities")

@bp.get("/<city_id:int>")
async def get_city(request: Request, city_id: int):
    city = request.app.ctx.db.get_specific_city(city_id=city_id)
    
    if not city:
        raise exceptions.NotFound("City not found.")

    return json(body=city)


@bp.get("/<city_id:int>/counts")
async def get_city_qa_counts(request: Request, city_id: int):
    counts = request.app.ctx.db.get_city_question_and_answer_counts(city_id=city_id)

    return json(body=counts)


@bp.get("/by-country/<country_id:int>")
async def get_cities_in_specific_country(request: Request, country_id: int):
    offset = int(request.args.get("offset", 0))
    limit = int(request.args.get("limit", 10))

    cities = request.app.ctx.db.get_cities_in_specific_country(country_id=country_id, offset=offset, limit=limit)

    if not cities:
        raise exceptions.NotFound("No cities found for the specified country.")

    return json(body=cities)


@bp.get("/most-conquered")
async def get_most_conquered_cities(request: Request):
    r = request.app.ctx.redis
    
    cached = await r.get("most_conquered_cities")
    if cached:
        return json(body=json_lib.loads(cached))

    limit = int(request.args.get("limit", 10))

    cities = request.app.ctx.db.get_most_conquered_cities(limit)

    if not cities:
        raise exceptions.NotFound("No cities found.")

    await r.set("most_conquered_cities", json_lib.dumps(cities), ex=600)  # Cache for 10 minutes
    return json(cities)
