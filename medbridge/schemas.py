from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class TodoBase(BaseModel):
    task: str = Field(..., min_length=1, max_length=200)
    done: bool = False


class TodoCreate(TodoBase):
    owner_id: Optional[int] = None


class TodoRead(TodoBase):
    id: int
    owner_id: Optional[int] = None
    # Support for both Pydantic v1 and v2:
    # - v1 expects Config.orm_mode = True
    # - v2 expects model_config = {"from_attributes": True}
    class Config:
        orm_mode = True

    try:
        # pydantic v2 compatibility
        model_config = {"from_attributes": True}
    except Exception:
        pass


class UserBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=128)


class UserRead(UserBase):
    id: int
    class Config:
        orm_mode = True

    try:
        model_config = {"from_attributes": True}
    except Exception:
        pass
