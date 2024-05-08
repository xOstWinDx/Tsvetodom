import json
from pathlib import Path

from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from database import engine, Base
from products.dao import ProductDAO

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


@app.get('/products')
async def products(request: Request):
    products = await ProductDAO.get(50)

    return templates.TemplateResponse(request=request, name='products.html',
                                      context={'products': products})
