from typing import Dict

from database.models import Post


async def add_post(conn, data: Dict[str, str]):
    stmt = Post.insert().values(category_id=data['category_id'],
                                title=data['title'],
                                text=data['text'],
                                main_img=data['main_img'],
                                created_at=data['created_at'],
                                last_updated=data['last_updated'])
    await conn.execute(stmt)


async def get_all(conn, data):
    # query chaining not working

    if data.get('limit') and data.get('offset'):
        query = Post.select().order_by(Post.c.last_updated.desc()).limit(data['limit']).offset(data['offset'])
    elif data.get('limit'):
        query = Post.select().order_by(Post.c.last_updated.desc()).limit(data['limit'])
    elif data.get('offset'):
        query = Post.select().order_by(Post.c.last_updated.desc()).offset(data['offset'])
    else:
        query = Post.select().order_by(Post.c.last_updated.desc())

    result = await conn.execute(query)
    return await result.fetchall()
