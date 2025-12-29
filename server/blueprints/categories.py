from sanic import Blueprint, Request, exceptions, json
import asyncio

bp = Blueprint("Categories", url_prefix="/categories")

@bp.get("/")
async def get_all_categories(request: Request):
    r = request.app.ctx.redis

    cached = await r.get("all_categories")
    if cached:
        return json(body=json.loads(cached))

    categories = await asyncio.to_thread(request.app.ctx.db.get_all_categories)

    if not categories:
        raise exceptions.NotFound("No categories found.")

    await r.set("all_categories", json.dumps(categories), ex=3600)  # Cache for 1 hour
    return json(body=categories)


@bp.get("/question/<question_id:int>")
async def get_categories_of_question(request: Request, question_id: int):
    categories = await asyncio.to_thread(request.app.ctx.db.get_categories_of_question, question_id=question_id)

    if not categories:
        raise exceptions.NotFound("No categories found for the specified question.")

    return json(body=categories)


@bp.get("/<category_id:int>")
async def get_specific_category(request: Request, category_id: int):
    category = await asyncio.to_thread(request.app.ctx.db.get_specific_category, category_id=category_id)

    if not category:
        raise exceptions.NotFound("Category not found.")

    return json(body=category)


@bp.get("/by-city/<city_id:int>")
async def get_categories_with_stats_in_city(request: Request, city_id: int):
    r = request.app.ctx.redis

    cached = await r.get(f"{city_id}_city_categories_with_stats")
    if cached:
        return json(body=json.loads(cached))

    categories = await asyncio.to_thread(request.app.ctx.db.get_all_categories_of_city_with_stats, city_id=city_id)

    if not categories:
        raise exceptions.NotFound("No categories found for the specified city.")

    await r.set(f"{city_id}_city_categories_with_stats", json.dumps(categories), ex=600)  # Cache for 10 minutes
    return json(body=categories)


@bp.get("/by-country/<country_id:int>")
async def get_categories_with_stats_in_country(request: Request, country_id: int):
    r = request.app.ctx.redis

    cached = await r.get(f"{country_id}_country_categories_with_stats")
    if cached:
        return json(body=json.loads(cached))
    
    categories = await asyncio.to_thread(request.app.ctx.db.get_all_categories_of_country_with_stats, country_id=country_id)

    if not categories:
        raise exceptions.NotFound("No categories found for the specified country.")

    await r.set(f"{country_id}_country_categories_with_stats", json.dumps(categories), ex=600)  # Cache for 10 minutes
    return json(body=categories)