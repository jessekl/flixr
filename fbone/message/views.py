
# -*- coding: utf-8 -*-

import os

from flask import Blueprint, render_template, send_from_directory, abort, redirect, url_for, request, flash
from flask import current_app as app
from flaskext.babel import gettext as _

from flask.ext.login import login_required, current_user
from .forms import CreateMessageForm, ResponseMessageForm
from .models import Message, StaredMessages , MessageResponses


message = Blueprint('message', __name__, url_prefix='/message')


@message.route('/add_message', methods=['POST'])
@login_required
def add_message():
	user = current_user
	form = CreateMessageForm()
	if form.validate_on_submit():
		form.add_message(user)
		flash(_("Your message has been added"),'success')
	msg = Message()
	return render_template('user/index.html', form=form, user=user,messages = msg.get_all_messages())

@message.route('/add_starred_message/<int:message_id>/<int:offset>', methods=['GET'])
def add_star_message(message_id,offset):
	user = current_user
	star_message = StaredMessages()
	star_message.add(
		user_id = current_user.id,
		message_id = message_id
		)
	return redirect(url_for('user.index',offset = offset))

@message.route('/remove_starred_message/<int:message_id>/<int:offset>', methods=['GET'])
def remove_star_message(message_id,offset):
	user = current_user
	star_message = StaredMessages()
	star_message.delete_by_id(message_id)
	return redirect(url_for('user.index',offset = offset))

@message.route('/message_response', methods=['GET'])
@message.route('/message_response/<int:offset>', methods=['GET'])
def message_response(offset=0):
	user = current_user
	msg = Message()
	msg = msg.get_response_message(user,offset)
	if(msg is not None):
		form = ResponseMessageForm(offset = offset,message_id = msg.message_id)
	else:
		form = ResponseMessageForm(offset = offset)
	return render_template('user/responses.html', user=user,message = msg,offset=offset,form=form)

@message.route('/message_response', methods=['POST'])
def add_message_response():
	user = current_user
	form = ResponseMessageForm()
	msg = Message()
	offset = int(form.data["offset"])
	if(form.add_response(user) == False):
		offset = offset + 1
	msg = msg.get_response_message(user,offset)
	if(msg is None and offset > 0):
		msg = Message()
		msg = msg.get_response_message(user,0)
	if(msg is not None):
		form.message_id.data = msg.message_id
	return redirect(url_for('user.index',offset = offset))




