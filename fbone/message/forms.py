from flask.ext.wtf import (HiddenField, BooleanField, TextField,
        PasswordField, SubmitField)
from flask.ext.wtf import Form, ValidationError
from flask.ext.wtf import Required
from .models import Message, StaredMessages
from ..extensions import db

class CreateMessageForm(Form):
    text = TextField(u'What\'s on your mind', [Required()],
            description=u"Post will appear on your time line") 
    submit = SubmitField(u'Share')  

    def add_message(self,user):
    	self.populate_obj(user)
    	message = Message()
        message.text = self.text.data
        message.user_id = user.id

        db.session.add(message)
        db.session.commit() 
