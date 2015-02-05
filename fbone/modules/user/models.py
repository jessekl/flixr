# -*- coding: utf-8 -*-

from sqlalchemy import Column, types
from sqlalchemy.ext.mutable import Mutable
from werkzeug import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin

from fbone.types import DenormalizedText
from fbone.extensions import db
from fbone.utils import get_current_time, GENDER_TYPE, STRING_LEN
from .constants import USER, USER_ROLE, ADMIN, INACTIVE, USER_STATUS


class UserDetail(db.Model):

    __tablename__ = 'user_details'

    id = Column(db.Integer, primary_key=True)

    age = Column(db.Integer)
    phone = Column(db.String(STRING_LEN))
    url = Column(db.String(STRING_LEN))
    location = Column(db.String(STRING_LEN))
    bio = Column(db.String(STRING_LEN))

    gender_code = db.Column(db.Integer)

    @property
    def gender(self):
        return GENDER_TYPE.get(self.gender_code)

    created_time = Column(db.DateTime, default=get_current_time)


class User(db.Model, UserMixin):

    __tablename__ = 'users'

    id = Column(db.Integer, primary_key=True)
    name = Column(db.String(STRING_LEN), nullable=False, unique=True)
    email = Column(db.String(STRING_LEN), nullable=False, unique=True)
    openid = Column(db.String(STRING_LEN), unique=True)
    activation_key = Column(db.String(STRING_LEN))
    created_time = Column(db.DateTime, default=get_current_time)

    avatar = Column(db.String(STRING_LEN))

    _password = Column('password', db.String(STRING_LEN), nullable=False)

    def _get_password(self):
        return self._password

    def _set_password(self, password):
        self._password = generate_password_hash(password)
    # Hide password encryption by exposing password field only.
    password = db.synonym('_password',
                          descriptor=property(_get_password,
                                              _set_password))

    def check_password(self, password):
        if self.password is None:
            return False
        return check_password_hash(self.password, password)

    def reset_password(self):
        self.activation_key = str(uuid4())
        db.session.add(self)
        db.session.commit()

    def change_password(self):
        self.password = self.password.data
        self.activation_key = None
        db.session.add(self)
        db.session.commit()

    # ================================================================
    # One-to-many relationship between users and roles.
    role_code = Column(db.SmallInteger, default=USER)

    @property
    def role(self):
        return USER_ROLE[self.role_code]

    def is_admin(self):
        return self.role_code == ADMIN

    # ================================================================
    # One-to-many relationship between users and user_statuses.
    status_code = Column(db.SmallInteger, default=INACTIVE)

    @property
    def status(self):
        return USER_STATUS[self.status_code]

    # ================================================================
    # One-to-one (uselist=False) relationship between users and user_details.
    user_detail_id = Column(db.Integer, db.ForeignKey("user_details.id"))
    user_detail = db.relationship("UserDetail", uselist=False, backref="user")

    # ================================================================
    # Follow / Following
    followers = Column(DenormalizedText)
    following = Column(DenormalizedText)

    @property
    def num_followers(self):
        if self.followers:
            return len(self.followers)
        return 0

    @property
    def num_following(self):
        return len(self.following)

    def follow(self, user):
        user.followers.add(self.id)
        self.following.add(user.id)
        user.followers=list(user.followers)
        self.following=list(self.following)
        # user.followers=
        # db.session.add(self)
        # db.session.add(user)
        # print "1.0"
        db.session.commit()

    def unfollow(self, user):
        if self.id in user.followers:
            print "1.0:%s"%user.followers
            user.followers.remove(self.id)
            user.followers=list(user.followers)
            print "2.0:%s"%user.followers
            db.session.add(user)

        if user.id in self.following:
            self.following.remove(user.id)
            self.following=list(self.following)
            db.session.add(self)

        db.session.commit()

    def get_following_query(self):
        return User.query.filter(User.id.in_(self.following or set()))

    def get_followers_query(self):
        return User.query.filter(User.id.in_(self.followers or set()))

    def is_following(self,follower):
        return follower.id in self.following and self.id in follower.followers


    # ================================================================
    # Class methods

    @classmethod
    def authenticate(cls, login, password):
        user = cls.query.filter(db.or_(User.name == login, User.email == login)).first()

        if user:
            authenticated = user.check_password(password)
        else:
            authenticated = False

        return user, authenticated

    @classmethod
    def search(cls, keywords):
        criteria = []
        for keyword in keywords.split():
            keyword = '%' + keyword + '%'
            criteria.append(db.or_(
                User.name.ilike(keyword),
                User.email.ilike(keyword),
            ))
        q = reduce(db.and_, criteria)
        return cls.query.filter(q)

    @classmethod
    def get_by_id(cls, user_id):
        return cls.query.filter_by(id=user_id).first_or_404()

    def check_name(self, name):
        return User.query.filter(db.and_(User.name == name, User.email != self.id)).count() == 0