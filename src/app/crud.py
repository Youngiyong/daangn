from sqlalchemy.orm import Session
from fastapi import HTTPException
from models import Votes, VoteItems, VoteItemUsers
from schemas import RequestVote, RequestVoteItem
from datetime import datetime, timedelta
import util


def get(db: Session, vote_id: str, post_id: str):
    vote = db.query(Votes).filter(Votes.deleted_at == None,
                                   Votes.id == vote_id,
                                   Votes.post_id == post_id).first()

    return vote


def delete(db: Session, vote_id: str, post_id: str):
    vote = db.query(Votes).filter(Votes.deleted_at == None,
                                  Votes.id == vote_id,
                                  Votes.post_id == post_id).first()

    if vote is None:
        raise HTTPException(status_code=404, detail="존재하지 않는 투표 번호입니다.")

    vote.updated_at = datetime.now()
    vote.deleted_at = datetime.now()

    db.commit()
    res = {"id": vote.id}
    return res


def create_vote_user(db: Session, payload:RequestVoteItem, user_id: str):
    # 투표가 유효한지 체크
    vote = db.query(Votes).filter(Votes.deleted_at == None,
                                  Votes.end_at > datetime.now(),
                                  Votes.id == payload.vote_id,
                                  Votes.post_id == payload.post_id).first()

    if vote is None:
        raise HTTPException(status_code=400, detail="투표 기간이 종료되었거나 삭제된 투표 정보이거나 유효하지 않은 투표 정보입니다.")

    try:
        vote_item = db.query(VoteItems).filter(VoteItems.id == payload.vote_item_id).first()
        vote_item.count += 1

        vote_item_user = VoteItemUsers(user_id=user_id, vote_item_id=payload.vote_item_id)
        db.add(vote_item_user)
        db.commit()
        db.refresh(vote_item_user)

        res = {
            "id": vote_item.id,
            "msg": "Success",
            "code": "S000"
        }

        return res

    except:
        raise HTTPException(status_code=500, detail="Internal Error")
        db.rollback()



def create(db: Session, payload: RequestVote):
    if payload.vote_items is None or len(payload.vote_items) < 2 or len(payload.vote_items) > 100:
        raise HTTPException(status_code=400, detail="투표 항목을 두개 이상 생성해주세요.")

    if payload.end_at is None:
        payload.end_at = datetime.now() + timedelta(days=1)

    try:
        # 투표 생성
        uuid = util.uuid()
        vote = Votes(
            id=uuid,
            post_id=payload.post_id,
            title=payload.title,
            content=payload.content,
            end_at=payload.end_at)
        db.add(vote)

        for item in payload.vote_items:
            vote_item = VoteItems(
                vote_id=uuid,
                title=item
            )
            db.add(vote_item)

        db.commit()

        res = {
            "id": uuid,
            "msg": "Success",
            "code": "S000"
        }

        return res


    except:
        raise HTTPException(status_code=500, detail="Internal Error")
        db.rollback()



#
# def get(db_session: Session, id: int):
#     return db_session.query(Note).filter(Note.id == id).first()
#
#
# def get_all(db_session: Session):
#     return db_session.query(Note).all()
#
#
# def put(db_session: Session, note: Note, title: str, description: str):
#     note.title = title
#     note.description = description
#     db_session.commit()
#     return note
#
#
