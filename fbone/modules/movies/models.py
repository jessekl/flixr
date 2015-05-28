
# -*- coding: utf-8 -*-

from sqlalchemy import Column, func
from fbone.modules.base import Base 
from fbone.extensions import db
from fbone.utils import get_current_time, STRING_LEN

class Movie(Base):
    
    
    name = Column(db.String(STRING_LEN))
    release_date = Column(db.String(STRING_LEN))
    poster_url = Column(db.String(STRING_LEN))

    
    def to_dict(self):
        return {
            'id' : self.id,
            'name' : self.name,
           	'release_date': self.release_date,
           	'poster_url': self.poster_url
        }

