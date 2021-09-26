from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional


class VoteBase(BaseModel):
    id: str
    post_id: int
    title: str
    content: str
    end_at: datetime
    created_at: datetime


class VoteItem(BaseModel):
    id: int
    vote_id: str
    title: str
    count: int

    class Config:
        orm_mode = True


class Vote(BaseModel):
    id: str
    post_id: int
    title: str
    content: str
    end_at: datetime
    is_active: str = Field(description="투표 활성 여부")
    is_vote: str = Field(description="투표 가능 여부")
    vote_items: List[VoteItem] = []
    created_at: datetime

    class Config:
        schema_extra = {
            "example": {
                "id": "ivxEoCAcHM",
                "post_id": 100,
                "title": "This is Vote Title",
                "content": "This is Vote description....",
                "end_at": "2021-09-25 04:37:02",
                "is_vote" : "True",
                "is_active" : "True",
                "vote_items": [
                    {
                        "id": 14,
                        "vote_id": "ivxEoCAcHM",
                        "title": "항목1",
                        "count": 0
                    },
                    {
                        "id": 15,
                        "vote_id": "ivxEoCAcHM",
                        "title": "항목2",
                        "count": 0
                    }
                ],
                "created_at": "2021-09-25 04:37:02",
            }
        }


class RequestVote(BaseModel):
    post_id: int
    title: str
    content: Optional[str]
    end_at: Optional[datetime]
    vote_items: Optional[List[str]]

    class Config:
        schema_extra = {
            "example": {
                "post_id": 100,
                "title": "This is Vote Title",
                "content": "This is Vote description....",
                "end_at": "2021-09-25 04:37:02",
                "vote_items": ["항목1", "항목2", "항목3", "..."],
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
                "post_id": 100,
                "vote_id": "ivxEoCAcHM",
                "vote_item_id": 14
            }
        }


class ResponseCreate(BaseModel):
    msg: str
    code: str
    id: str

    class Config:
        arbitrary_types_allowed = True
        schema_extra = {
            "example": {
                "msg": "Success",
                "code": "S000",
                "id": "ivxEoCAcHM",
            }
        }


class ResponseVoteItemCreate(BaseModel):
    code: str
    msg: str
    id: str

    class Config:
        arbitrary_types_allowed = True
        schema_extra = {
            "example": {
                "msg": "Success",
                "code": "S000",
                "id": "17",
            }
        }


class ResponseSuccess(BaseModel):
    code: str
    msg: str

    class Config:
        arbitrary_types_allowed = True
        schema_extra = {
            "example": {
                "msg": "Success",
                "code": "S000",
            }
        }