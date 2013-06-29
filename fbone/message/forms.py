from flask.ext.wtf import (HiddenField, BooleanField, TextField, RadioField,PasswordField, SubmitField)
from flask.ext.wtf import Form, ValidationError, widgets
from flask.ext.wtf import Required
from flaskext.babel import lazy_gettext as _
from .models import Message, StaredMessages
from ..extensions import db

class CreateMessageForm(Form):
    text = TextField(_('What\'s on your mind'), [Required()],
            description=_("Post will appear on your time line")) 
    submit = SubmitField(_('Share'))  

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
    response = RadioField(_('Whats your take ?'), choices=list_options,)
    comment = TextField(_("Comment"),description=_("What do you have to say about this post"))
    submit = SubmitField(_('Submit')) 

    def add_response(self,user):
        self.populate_obj(user)
        comment = self.comment.data
        resp = self.response.data
        resp = None if resp == "None" else resp
        if(comment == '' and resp == None):
            	print "testing"
		return False
        response = Message()
        response.user_id = user.id
        response.parent_id = self.data["message_id"]
        response.text = comment
        response.response = resp
        response.save()
        return True
