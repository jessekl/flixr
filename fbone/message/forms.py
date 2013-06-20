from flask.ext.wtf import (HiddenField, BooleanField, TextField, RadioField,PasswordField, SubmitField)
from flask.ext.wtf import Form, ValidationError, widgets
from flask.ext.wtf import Required
from .models import Message, StaredMessages, MessageResponses
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


class ResponseMessageForm(Form):
    list_options = [(True,'yes'),(False,'no')]
    message_id = HiddenField()
    offset = HiddenField()
    response = RadioField('Whats your take ?', choices=list_options,)
    comment = TextField("Comment",description=u"What do you have to say about this post")
    submit = SubmitField(u'Submit') 

    def add_response(self,user):
        self.populate_obj(user)
        comment = self.comment.data
        resp = self.response.data
        resp = None if resp == "None" else resp
        if(comment == '' and resp == None):
            	print "testing"
		return False
        response = MessageResponses()
        response.add(user_id = user.id,
                    message_id = self.data["message_id"],
                    comment = comment,
                    response = resp)
        return True
