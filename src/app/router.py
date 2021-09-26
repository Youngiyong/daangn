from fastapi import APIRouter,Depends, status, Header
from sqlalchemy.orm import Session
from app.db import get_db
from app.schemas import RequestVote, ResponseCreate, ResponseSuccess, Vote, RequestVoteItem, ResponseVoteItemCreate
from app.crud import create, create_vote_user, put, delete, get
router = APIRouter()


@router.post("", status_code=status.HTTP_201_CREATED, response_model=ResponseCreate)
def post_vote(*, db: Session = Depends(get_db), x_user_id: str = Header(None), payload: RequestVote):
    """
    투표 생성 API
    """
    return create(db=db, payload=payload)


@router.put("/{post_id}/{vote_id}", status_code=status.HTTP_200_OK, response_model=ResponseSuccess)
def put_vote_end_at(*, db: Session = Depends(get_db), x_user_id: str = Header(None), post_id: int, vote_id: str):
    """
    투표 종료 API
    """
    return put(db=db, post_id=post_id, vote_id=vote_id)


@router.delete("/{post_id}/{vote_id}", status_code=status.HTTP_200_OK, response_model=ResponseSuccess)
def delete_vote(*, db: Session = Depends(get_db), x_user_id: str = Header(None), post_id: int, vote_id: str):
    """
    투표 삭제 API
    """
    return delete(db=db, vote_id=vote_id, post_id=post_id)


@router.get("/{post_id}/{vote_id}", response_model=Vote)
def get_vote(*, db: Session = Depends(get_db), x_user_id: str = Header(None), post_id: int, vote_id: str):
    """
    투표 조회 API
    """
    return get(db=db, vote_id=vote_id, post_id=post_id, user_id=x_user_id)


@router.post("/items/users", status_code=status.HTTP_200_OK, response_model=ResponseVoteItemCreate)
def post_vote_item_user(*, db: Session = Depends(get_db), x_user_id: str = Header(None), payload: RequestVoteItem):
    """
    투표 선택 API
    """
    return create_vote_user(db=db, user_id=x_user_id, payload=payload)