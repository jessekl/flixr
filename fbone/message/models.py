# -*- coding: utf-8 -*-

from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from ..extensions import db
from ..utils import get_current_time
from fbone.user.models import User

class Message(db.Model):

    __tablename__ = 'message'

    message_id = Column(db.Integer, primary_key=True)
    user_id = Column(db.Integer,ForeignKey('users.id', onupdate="CASCADE", ondelete="RESTRICT"), nullable=False)
    text = Column(db.Text, nullable=False)
    pub_date = Column(db.DateTime, default=get_current_time)
    publish_user = relationship('User', backref = 'message', primaryjoin = "Message.user_id == User.id")


    def save(self):
        db.session.add(self)
        db.session.commit()

    def get_all_messages(cls,limit=None,offset=0):
    	query = cls.query.filter()
    	if limit:
    		query = query.limit(limit)
    	if offset:
    		query = query.offset(offset)
    	return query.all()

    def get_message_from_user(cls,user,limit=None,offset=0):
        query = cls.query.filter(cls.user_id == User.id)
        if limit:
            query = query.limit(limit)
        if offset:
            query = query.offset(offset)
        return query.all()


class StaredMessages(db.Model):
    __tablename__ = 'stared_messages'

    id = Column(db.Integer, primary_key=True)
    user_id = Column(db.Integer,ForeignKey('users.id', onupdate="CASCADE", ondelete="RESTRICT"), nullable=False)
    message_id = Column(db.Integer,ForeignKey('message.message_id', onupdate="CASCADE", ondelete="RESTRICT"), nullable=False)
    publish_user = relationship('User', backref = 'star_message', primaryjoin = "StaredMessages.user_id == User.id")
    message = relationship('Message', backref = 'star_id', primaryjoin = "StaredMessages.message_id == Message.message_id")

    def add(self,user_id,message_id):
        self.user_id = user_id
        self.message_id = message_id
        db.session.add(self)
        db.session.commit()

    def get_by_id(cls, star_id):
        return cls.query.filter_by(id=star_id).first_or_404()

    def delete_by_id(cls, message_id):
        print message_id
        cls.query.filter_by(message_id=message_id).delete(synchronize_session='fetch')
        db.session.commit()
