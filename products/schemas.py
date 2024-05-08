from pydantic import BaseModel, Field


class ProductOut(BaseModel):  # define your model
    id: int = Field(..., example=1)
    title: str = Field(..., example="Букет")
    thumb_photo: str = Field(...)
