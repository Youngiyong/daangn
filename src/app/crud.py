from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException
from app.models import Votes, VoteItems, VoteItemUsers
from app.schemas import RequestVote, RequestVoteItem
from datetime import datetime, timedelta
from app.util import uuid

def put(db: Session, vote_id: str, post_id: str):

    # 투표 정보를 얻어온다.
    vote = db.query(Votes).filter(Votes.deleted_at == None,
                                   Votes.id == vote_id,
                                   Votes.post_id == post_id).first()

    if vote is None:
        raise HTTPException(status_code=404, detail="존재하지 않는 투표 번호입니다.")

    vote.end_at = datetime.now()
    vote.updated_at = datetime.now()
    db.commit()

    res = {
        "msg": "Success",
        "code": "S000",
        "id": vote.id
    }

    return res


def get(db: Session, vote_id: str, post_id: str, user_id: str):

    # 투표 정보를 얻어온다.
    vote = db.query(Votes).filter(Votes.deleted_at == None,
                                   Votes.id == vote_id,
                                   Votes.post_id == post_id).first()

    if vote is None:
        raise HTTPException(status_code=404, detail="존재하지 않는 투표 번호입니다.")

    vote_items = vote.vote_items

    if vote_items is None:
        raise HTTPException(status_code=500, detail="투표 항목이 존재하지 않습니다.")

    vote_item_id = list()

    for i in range(len(vote_items)):
        vote_item_id.append(vote_items[i].id)

    vote_item_user = db.query(VoteItemUsers)\
                        .filter(VoteItemUsers.vote_item_id.in_(vote_item_id),
                                VoteItemUsers.user_id == user_id).all()

    now = datetime.now()
    is_active = True
    is_pick = False

    if vote.end_at < now:
        is_active = False

    if vote_item_user:
        is_pick = True

    res = {
        "id": vote.id,
        "post_id": vote.post_id,
        "title": vote.title,
        "content": vote.content,
        "end_at": vote.end_at,
        "is_active": is_active,
        "is_pick": is_pick,
        "vote_items": vote.vote_items,
        "created_at": vote.created_at
    }

    return res


def delete(db: Session, vote_id: str, post_id: str):

    # 투표가 존재하는지 확인
    vote = db.query(Votes).filter(Votes.deleted_at == None,
                                  Votes.id == vote_id,
                                  Votes.post_id == post_id).first()

    if vote is None:
        raise HTTPException(status_code=404, detail="존재하지 않는 투표 번호입니다.")

    try:
        vote.updated_at = datetime.now()
        vote.deleted_at = datetime.now()

        db.commit()

        res = {
            "msg": "Success",
            "code": "S000",
            "id": vote.id
        }

    except:
        raise HTTPException(status_code=500, detail="Internal Error")
        db.rollback()

    return res


def create_vote_user(db: Session, payload:RequestVoteItem, user_id: str):

    # 투표가 유효한지 확인
    vote = db.query(Votes).filter(Votes.deleted_at == None,
                                  Votes.end_at > datetime.now(),
                                  Votes.id == payload.vote_id,
                                  Votes.post_id == payload.post_id).first()

    if vote is None:
        raise HTTPException(status_code=400, detail="투표 기간이 종료되었거나 삭제된 투표라 투표가 불가합니다.")

    # 포스트에 해당하는 투묘 항목을 얻어온다.
    vote_item = db.query(VoteItems).filter(VoteItems.id == payload.vote_item_id).first()
    vote_items = vote.vote_items

    # 투표 항목 아이디를 담는다.
    vote_item_id = list()
    for i in range(len(vote_items)):
        vote_item_id.append(vote_items[i].id)

    # 기존에 투표한 사용자인지 확인한다.
    user = db.query(VoteItems).join(VoteItems.vote_item_users) \
            .filter(VoteItems.id.in_(vote_item_id),
                    VoteItemUsers.user_id == user_id).all()

    if user:
        raise HTTPException(status_code=400, detail="중복 투표가 불가합니다.")

    try:

        # 투표 항목 카운트 증가
        vote_item.count += 1
        vote_item_user = VoteItemUsers(user_id=user_id, vote_item_id=payload.vote_item_id)
        db.add(vote_item_user)
        db.commit()
        db.refresh(vote_item_user)

        res = {
            "msg": "Success",
            "code": "S000",
            "id": vote_item.id
        }

    except:
        raise HTTPException(status_code=500, detail="Internal Error")
        db.rollback()

    return res


def create(db: Session, payload: RequestVote):

    # 항목이 존재하고 2개 이상 100개 미만인지 확인한다.
    if payload.vote_items is None or len(payload.vote_items) < 2 or len(payload.vote_items) > 100:
        raise HTTPException(status_code=400, detail="투표 항목을 두개 이상 생성해주세요.")

    # 투표 종료시간 체크 없으면 + 1 day
    if payload.end_at is None:
        payload.end_at = datetime.now() + timedelta(days=1)

    try:
        # 투표 생성
        id = uuid()
        vote = Votes(
            id=id,
            post_id=payload.post_id,
            title=payload.title,
            content=payload.content,
            end_at=payload.end_at)
        db.add(vote)

        # 투표 항목 생성
        for item in payload.vote_items:
            vote_item = VoteItems(
                vote_id=id,
                title=item
            )
            db.add(vote_item)

        db.commit()

        res = {
            "msg": "Success",
            "code": "S000",
            "id": id,
        }

    except:
        raise HTTPException(status_code=500, detail="Internal Error")
        db.rollback()

    return res

