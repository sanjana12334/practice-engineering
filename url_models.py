from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from url_database import Base


class URLModel(Base):
    __tablename__ = "urls"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    original_url: Mapped[str] = mapped_column(
        String(2048),
        nullable=False
    )

    short_code: Mapped[str] = mapped_column(
        String(20),
        unique=True,
        nullable=False,
        index=True
    )