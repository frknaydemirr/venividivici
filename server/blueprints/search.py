from sanic import Blueprint, Request, exceptions, json

bp = Blueprint("Search", url_prefix="/search")

@bp.get("/cities/<query:str>")
async def search_cities(request: Request, query: str):
    offset = int(request.args.get("offset", 0))
    limit = int(request.args.get("limit", 10))

    cities = request.app.ctx.db.get_cities_matching_query(query_string=query, offset=offset, limit=limit)

    if not cities:
        raise exceptions.NotFound("No cities found matching the query.")

    return json(body=cities)


@bp.get("/countries/<query:str>")
async def search_countries(request: Request, query: str):
    offset = int(request.args.get("offset", 0))
    limit = int(request.args.get("limit", 10))

    countries = request.app.ctx.db.get_countries_matching_query(query_string=query, offset=offset, limit=limit)

    if not countries:
        raise exceptions.NotFound("No countries found matching the query.")

    return json(body=countries)


@bp.get("/questions/<query:str>")
async def search_questions(request: Request, query: str):
    offset = int(request.args.get("offset", 0))
    limit = int(request.args.get("limit", 10))

    questions = request.app.ctx.db.get_questions_matching_query(query_string=query, offset=offset, limit=limit)

    if not questions:
        raise exceptions.NotFound("No questions found matching the query.")

    return json(body=questions)