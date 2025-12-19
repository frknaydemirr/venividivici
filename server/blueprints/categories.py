from sanic import Blueprint, Request, exceptions, json

bp = Blueprint("Categories", url_prefix="/categories")

@bp.get("/")
async def get_all_categories(request: Request):
    categories = request.app.ctx.db.get_all_categories()

    if not categories:
        raise exceptions.NotFound("No categories found.")

    return json(body=categories)

# TODO: Add this fix to swagger
@bp.get("/question/<question_id:int>")
async def get_categories_of_question(request: Request, question_id: int):
    categories = request.app.ctx.db.get_categories_of_question(question_id=question_id)

    if not categories:
        raise exceptions.NotFound("No categories found for the specified question.")

    return json(body=categories)


@bp.get("/<category_id:int>")
async def get_specific_category(request: Request, category_id: int):
    category = request.app.ctx.db.get_specific_category(category_id=category_id)

    if not category:
        raise exceptions.NotFound("Category not found.")

    return json(body=category)


@bp.get("/by-city/<city_id:int>")
async def get_categories_with_stats_in_city(request: Request, city_id: int):
    categories = request.app.ctx.db.get_all_categories_of_city_with_stats(city_id=city_id)

    if not categories:
        raise exceptions.NotFound("No categories found for the specified city.")

    return json(body=categories)


@bp.get("/by-country/<country_id:int>")
async def get_categories_with_stats_in_country(request: Request, country_id: int):
    categories = request.app.ctx.db.get_all_categories_of_country_with_stats(country_id=country_id)

    if not categories:
        raise exceptions.NotFound("No categories found for the specified country.")

    return json(body=categories)