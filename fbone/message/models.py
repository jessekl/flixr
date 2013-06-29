# -*- coding: utf-8 -*-

from sqlalchemy import Column, ForeignKey, not_
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
    parent_id = Column(db.Integer,ForeignKey('message.message_id', onupdate="CASCADE", ondelete="RESTRICT"), nullable=True)
    response = Column(db.Boolean, nullable=True)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def get_responses(cls,id):
        query = cls.query.filter(Message.parent_id == id)
        return query.all()


    def get_all_messages(cls,limit=None,offset=0):
    	query = cls.query.filter(cls.parent_id == None)
    	if limit:
    		query = query.limit(limit)
    	if offset:
    		query = query.offset(offset)
    	return query.all()

    def get_message_from_user(cls,user,limit=None,offset=0):
        query = cls.query.filter(Message.user_id == user.id).filter(Message.parent_id == None)
        if limit:
            query = query.limit(limit)
        if offset:
            query = query.offset(offset)
        return query.all()

    def get_response_message(cls,user,offset):
        print user.id
        query = cls.query.with_entities(Message.parent_id).filter_by(user_id = user.id)
        # query = query.filter(not_(Message.parent_id == None))
        ids = query.all()
        # print ids
        ids = [x.parent_id for x in ids]
        ids = filter(lambda x: x is not None ,ids)
        print ids
        return cls.query.filter(Message.parent_id == None).filter(not_(Message.message_id.in_(ids))).offset(offset).first()
     
    @classmethod
    def get_by_id(cls, message_id):
        return cls.query.filter_by(id=message_id).first_or_404()



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

# class MessageResponses(db.Model):
#     __tablename__ = 'messages_responses'
#     id = Column(db.Integer, primary_key=True)
#     user_id = Column(db.Integer,ForeignKey('users.id', onupdate="CASCADE", ondelete="RESTRICT"), nullable=False)
#     message_id = Column(db.Integer,ForeignKey('message.message_id', onupdate="CASCADE", ondelete="RESTRICT"), nullable=False)
#     response = Column(db.Boolean, nullable=True)
#     comment = Column(db.Text, nullable=True)
#     publish_user = relationship('User', backref = 'messages_response', primaryjoin = "MessageResponses.user_id == User.id")
#     message = relationship('Message', backref = 'response', primaryjoin = "MessageResponses.message_id == Message.message_id")

#     def add(self,user_id,message_id,response,comment):
#         self.user_id = user_id
#         self.message_id = message_id
# 	self.response = response in ['True',True]
#         self.comment = comment
#         db.session.add(self)
#         db.session.commit()

#     def get_responses_from_user(cls,user_id):
#         query = cls.query.with_entities(MessageResponses.message_id).filter(MessageResponses.user_id == user_id)
#         messages=query.all()
#         return [x.message_id for x in messages]





