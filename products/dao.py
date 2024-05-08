from sqlalchemy import insert, select

from database import get_async_session
from products.models import Product


class ProductDAO:
    @classmethod
    async def add(cls, **data):
        async with get_async_session() as session:
            await session.execute(insert(Product).values(**data))
            await session.commit()

    @classmethod
    async def get(cls, limit) -> list[Product]:
        async with get_async_session() as session:
            res = await session.execute(select(Product).limit(limit))
            res = res.scalars().all()
        return res


