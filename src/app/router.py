
from typing import Any, List, Optional
from fastapi import APIRouter,Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from db import get_db
import schemas, time, crud

router = APIRouter()


@router.post("", status_code=status.HTTP_201_CREATED, response_model=schemas.ResponseSuccess)
def create_vote(*, db: Session = Depends(get_db), x_user_id: str = Header(None), payload: schemas.RequestVote):
    """
    create vote
    """
    # post check, user check 생략
    return crud.create(db=db, payload=payload)


@router.delete("/{post_id}/{vote_id}", status_code=status.HTTP_200_OK, response_model=schemas.ResponseSuccess)
def delete_vote(*, db: Session = Depends(get_db), x_user_id: str = Header(None), post_id: int, vote_id: str):
    """
    delete vote
    """
    # post check, user check 생략
    return crud.delete(db=db, vote_id=vote_id, post_id=post_id)


@router.get("/{post_id}/{vote_id}", response_model=schemas.Vote)
def find_vote(*, db: Session = Depends(get_db), x_user_id: str = Header(None), post_id: int, vote_id: str):
    """
    get vote
    """
    vote = crud.get(db=db, vote_id=vote_id, post_id=post_id)

    if vote is None:
        raise HTTPException(status_code=404, detail="삭제되었거나 존재하지 않는 투표 번호입니다.")

    return vote


@router.post("/items/users", status_code=status.HTTP_200_OK)
def create_vote_item_user(*, db: Session = Depends(get_db), x_user_id: str = Header(None), payload: schemas.RequestVoteItem):
    """
    create vote item user
    """
    vote_item_user = crud.create_vote_user(db=db, user_id=x_user_id, payload=payload )
    return vote_item_user