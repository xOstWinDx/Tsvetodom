from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.add_exception_handler(404, lambda x, y: RedirectResponse('/index.html'))

app.mount("/", StaticFiles(directory="static"), name="static")
