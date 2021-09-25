from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional, List


class VoteBase(BaseModel):
    id: Optional[str]
    post_id: Optional[int]
    user_id: Optional[str]
    title: Optional[str]
    description: Optional[str]
    end_at: Optional[datetime]
    created_at: Optional[datetime]
    created_at: Optional[datetime]
    deleted_at: Optional[datetime]


class VoteItemBase(BaseModel):
    id: Optional[int]
    vote_id: Optional[str]
    name: Optional[str]
    count: Optional[int]
    created_at: Optional[datetime]


class VoteItemUserBase(BaseModel):
    id: Optional[int]
    vote_item_id: Optional[str]
    user_id: Optional[str]
    created_at: Optional[datetime]


class VoteItemUserCreate(VoteItemUserBase):
    vote_item_id: Optional[int]

    class Config:
        arbitrary_types_allowed = True
        schema_extra = {
            "example": {
                "vote_item_id": 123456,
            }
        }


class VoteItemCreate(VoteItemBase):
    vote_id: Optional[str]
    name: Optional[str]

    class Config:
        arbitrary_types_allowed = True
        schema_extra = {
            "example": {
                "vote_id": "501234",
                "name": "Vote name",
            }
        }


class VoteCreate(VoteBase):
    post_id: Optional[int]
    title: Optional[str]
    description: Optional[str]
    end_at: Optional[datetime]
    vote_item: List[VoteItemCreate]

    class Config:
        arbitrary_types_allowed = True
        schema_extra = {
            "example": {
                "post_id": 501284,
                "title": "This is Vote Title",
                "description": "This is Vote description....",
                "end_at": "blogs/2021092012345678.png",
                "vote_item": ["name1", "name2", "name3", "..."],
            }
        }
