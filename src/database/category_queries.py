import marshmallow as ma

from database.models import PostCategories


async def get_category_by_title(conn, title):
    stmt = await conn.execute(PostCategories.select().where(PostCategories.c.title == title))
    category = await stmt.first()
    if not category:
        raise ma.ValidationError(message=f'No category with title {title}')
    return category['id']
