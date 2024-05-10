from typing import Generic, T

from pydantic import BaseModel, Field
from fastapi_pagination.links import Page as BasePage


class ProductOut(BaseModel):  # define your model
    id: int = Field(..., example=1)
    title: str = Field(..., example="Букет")
    thumb_photo: str = Field(...)


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
