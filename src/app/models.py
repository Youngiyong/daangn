from datetime import datetime

from sqlalchemy import ForeignKey, Column, String, Integer, func, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Votes(Base):
    id = Column(String(length=10), primary_key=True)
    post_id = Column(Integer, nullable=False)
    title = Column(String(length=100), nullable=False)
    content = Column(String(length=10000), default=None, nullable=True)
    end_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, nullable=True, default=datetime.now())
    updated_at = Column(DateTime, nullable=True)
    deleted_at = Column(DateTime, nullable=True)
    vote_items = relationship("VoteItems", back_populates="votes")
    __tablename__ = "votes"


class VoteItems(Base):
    id = Column(Integer, primary_key=True, index=True)
    vote_id = Column(String(length=10), ForeignKey("votes.id"))
    title = Column(String(length=100), nullable=False)
    count = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, nullable=False, default=datetime.now())
    votes = relationship("Votes", back_populates="vote_items")
    vote_item_users = relationship("VoteItemUsers", back_populates="vote_items")
    __tablename__ = "vote_items"


class VoteItemUsers(Base):
    id = Column(Integer, primary_key=True)
    vote_item_id = Column(Integer, ForeignKey("vote_items.id"))
    user_id = Column(String(length=4), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now())
    vote_items = relationship("VoteItems", back_populates="vote_item_users")
    __tablename__ = "vote_item_users"
