from typing import Generic, T

from fastapi import FastAPI, Depends
from fastapi_pagination import add_pagination, Params

from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from fastapi_pagination.links import Page as BasePage
from starlette.requests import Request

from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from database import get_db
from products.dao import ProductDAO
from products.models import Product
from products.schemas import ProductOut


class Page(BasePage[T], Generic[T]):
    @property
    def info(self) -> str:
        ru_title = {
            'first': "Начало",
            'last': "Конец",
            'self': "Наверх",
            'next': "Дальше",
            'prev': "Назад",
        }

        def _get_wrap_link(title: str, link: str) -> str:
            if link is None:
                return ''
            return f'<a href="{link}"><button>{ru_title[title]}</button><a/>'

        gg = self.links.model_dump(include={'first', 'prev', 'next', 'last'})
        opt = []
        opt.append(_get_wrap_link('first', gg['first']))
        opt.append(_get_wrap_link('prev', gg['prev']))
        opt.append(_get_wrap_link('next', gg['next']))
        opt.append(_get_wrap_link('last', gg['last']))
        options = "\n".join(opt)
        return f"<div>{options}</div>"


app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.add_exception_handler(404, lambda r, y: templates.TemplateResponse(request=r, name='not_found.html'))

app.mount("/pages", StaticFiles(directory="static"), name="pages")


@app.get('/')
async def index(request: Request):
    return templates.TemplateResponse(request=request, name='index.html')


@app.get('/info')
async def info(request: Request):
    return templates.TemplateResponse(request=request, name='info.html')


# @app.get('/load')
# async def load(request: Request):
#     file = Path("data.json")
#     data: dict = json.loads(file.read_text(encoding='utf-8'))
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
#     for i in data['response']["items"]:
#         if i.get('thumb_photo'):
#             await ProductDAO.add(id=i['id'], title=i['title'], thumb_photo=i['thumb_photo'])
#
#
# @app.get('/gets')
# async def gets(request: Request):
#     r = await ProductDAO.get()
#     for i in r:
#         print(i.id)


@app.get('/products', response_model=Page[ProductOut])
async def get_products(request: Request, page: int = 1, db: AsyncSession = Depends(get_db)):
    page = await paginate(db, select(Product).order_by(Product.id.desc()), params=Params(size=21, page=page))

    return templates.TemplateResponse(request=request, name='products.html',
                                      context={'products': page.items, 'page': page})


add_pagination(app)
