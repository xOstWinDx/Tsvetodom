from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.add_exception_handler(404, lambda r, y: templates.TemplateResponse(request=r, name='not_found.html'))

app.mount("/pages", StaticFiles(directory="static"), name="pages")


@app.get('/')
async def index(request: Request):
    return templates.TemplateResponse(request=request, name='index.html')


@app.get('/info')
async def index(request: Request):
    return templates.TemplateResponse(request=request, name='info.html')


@app.get('/products')
async def products(request: Request):
    return templates.TemplateResponse(request=request, name='products.html')
