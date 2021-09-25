
from typing import Any, List, Optional
import time
from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session

# from app.deps import get_db
import schemas

router = APIRouter()


@router.post("")
def create_vote(*, x_user_id: Optional[str] = Header(None), payload: schemas.VoteCreate):
    """
    create vote.
    """
    time.sleep(10)
    print(payload, x_user_id)


@router.delete("/{post_id}/{vote_id}")
def delete_vote(*, x_user_id: Optional[str] = Header(None), post_id: int, vote_id: str):
    """
    delete vote
    """

    print(post_id, vote_id, x_user_id)


@router.get("/{post_id}/{vote_id}")
def find_vote(*, x_user_id: Optional[str] = Header(None), post_id: int, vote_id: str):
    """
    get vote
    """
    print(post_id, vote_id, x_user_id)


@router.post("")
def create_vote_item_user(*, x_user_id: Optional[str] = Header(None), payload: schemas.VoteItemUserCreate):
    """
    create vote item user
    """
    time.sleep(10)
    print(payload, x_user_id)