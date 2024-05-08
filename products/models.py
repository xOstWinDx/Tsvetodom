from database import Base
from sqlalchemy.orm import Mapped, mapped_column


class Product(Base):
    __tablename__ = 'products'
    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    title: Mapped[str] = mapped_column(nullable=False)
    thumb_photo: Mapped[str] = mapped_column(nullable=False)
