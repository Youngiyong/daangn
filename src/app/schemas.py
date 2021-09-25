from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from typing import List, Optional


class ResponseSuccess(BaseModel):
    id: str
    msg: str
    code: str

    class Config:
        arbitrary_types_allowed = True
        schema_extra = {
            "example": {
                "msg": "Success",
                "code": "S000",
                "id": "506302",
            }
        }


class VoteBase(BaseModel):
    id: str
    post_id: int
    title: str
    content: str
    end_at: datetime
    created_at: datetime


class VoteItemUserBase(BaseModel):
    id: int
    vote_item_id: str
    user_id: str


class VoteItemUser(VoteItemUserBase):
    id: int
    vote_item_id: int
    user_id: str

    class Config:
        orm_mode = True


class VoteItemBase(BaseModel):
    id: int
    vote_id: str
    title: str
    count: int


class VoteItem(VoteItemBase):
    id: int
    vote_id: str
    title: str
    count: int
    vote_item_users: List[VoteItemUser] = []

    class Config:
        orm_mode = True


class Vote(VoteBase):
    id: str
    post_id: int
    title: str
    content: str
    end_at: datetime
    created_at: datetime
    vote_items: List[VoteItem] = []

    class Config:
        orm_mode = True


class RequestVote(BaseModel):
    post_id: int
    title: str
    content: Optional[str]
    end_at: Optional[datetime]
    vote_items: Optional[List[str]]

    class Config:
        schema_extra = {
            "example": {
                "post_id": 506302,
                "title": "This is Vote Title",
                "content": "This is Vote description....",
                "end_at": "2021-09-25 04:37:02",
                "vote_items": ["name1", "name2", "name3", "..."],
            }
        }


class RequestVoteItem(BaseModel):
    post_id: int
    vote_id: str
    vote_item_id: int

    class Config:
        arbitrary_types_allowed = True
        schema_extra = {
            "example": {
                "post_id": 506302,
                "vote_id": "iXrOQuIWMy",
                "vote_item_id": 101234
            }
        }