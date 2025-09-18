from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey, UniqueConstraint, Index
from typing import List, Optional

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(100), unique=True, index=True)

    albums: Mapped[List["Album"]] = relationship(back_populates="owner", cascade="all, delete-orphan")  # type: ignore

class Album(Base):
    __tablename__ = "albums"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(255), index=True)
    normalized_title: Mapped[str] = mapped_column(String(255), index=True)
    barcode: Mapped[Optional[str]] = mapped_column(String(64), nullable=True, index=True)
    artist: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    owner: Mapped[User] = relationship(back_populates="albums")  # type: ignore

    __table_args__ = (
        UniqueConstraint("owner_id", "normalized_title", name="uq_owner_title"),
        UniqueConstraint("owner_id", "barcode", name="uq_owner_barcode"),
        Index("ix_owner_title", "owner_id", "normalized_title"),
        Index("ix_owner_barcode", "owner_id", "barcode"),
    )
