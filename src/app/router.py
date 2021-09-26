from fastapi import APIRouter,Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from db import get_db
import schemas, crud

router = APIRouter()


@router.post("", status_code=status.HTTP_201_CREATED, response_model=schemas.ResponseCreate)
def post_vote(*, db: Session = Depends(get_db), x_user_id: str = Header(None), payload: schemas.RequestVote):
    """
    투표 생성 API
    """
    return crud.create(db=db, payload=payload)


@router.put("/{post_id}/{vote_id}", status_code=status.HTTP_200_OK, response_model=schemas.ResponseSuccess)
def put_vote_end_at(*, db: Session = Depends(get_db), x_user_id: str = Header(None), post_id: int, vote_id: str):
    """
    투표 종료 API
    """
    return crud.put(db=db, post_id=post_id, vote_id=vote_id)


@router.delete("/{post_id}/{vote_id}", status_code=status.HTTP_200_OK, response_model=schemas.ResponseSuccess)
def delete_vote(*, db: Session = Depends(get_db), x_user_id: str = Header(None), post_id: int, vote_id: str):
    """
    투표 삭제 API
    """
    return crud.delete(db=db, vote_id=vote_id, post_id=post_id)


@router.get("/{post_id}/{vote_id}", response_model=schemas.Vote)
def get_vote(*, db: Session = Depends(get_db), x_user_id: str = Header(None), post_id: int, vote_id: str):
    """
    투표 조회 API
    """
    return crud.get(db=db, vote_id=vote_id, post_id=post_id, user_id=x_user_id)


@router.post("/items/users", status_code=status.HTTP_200_OK, response_model=schemas.ResponseVoteItemCreate)
def post_vote_item_user(*, db: Session = Depends(get_db), x_user_id: str = Header(None), payload: schemas.RequestVoteItem):
    """
    투표 선택 API
    """
    return crud.create_vote_user(db=db, user_id=x_user_id, payload=payload)