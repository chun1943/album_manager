from pydantic import BaseModel, Field
from typing import Optional

class UserCreate(BaseModel):
    username: str = Field(min_length=1, max_length=100)

class UserOut(BaseModel):
    id: int
    username: str
    class Config:
        from_attributes = True

class AlbumCreate(BaseModel):
    title: Optional[str] = Field(default=None, max_length=255)
    barcode: Optional[str] = Field(default=None, max_length=64)
    artist: Optional[str] = Field(default=None, max_length=255)
    year: Optional[int] = Field(default=None)
    genre: Optional[str] = Field(default=None, max_length=100)
    cover_url: Optional[str] = Field(default=None, max_length=500)

class AlbumUpdate(BaseModel):
    title: Optional[str] = Field(default=None, max_length=255)
    barcode: Optional[str] = Field(default=None, max_length=64)
    artist: Optional[str] = Field(default=None, max_length=255)
    year: Optional[int] = Field(default=None)
    genre: Optional[str] = Field(default=None, max_length=100)
    cover_url: Optional[str] = Field(default=None, max_length=500)

class AlbumOut(BaseModel):
    id: int
    title: str
    barcode: Optional[str]
    artist: Optional[str]
    owner_id: int
    year: Optional[int] = None
    genre: Optional[str] = None
    cover_url: Optional[str] = None
    class Config:
        from_attributes = True

class ExistsOut(BaseModel):
    exists: bool
    album: Optional[AlbumOut] = None
