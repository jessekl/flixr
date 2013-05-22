
# -*- coding: utf-8 -*-

import os

from flask import Blueprint, render_template, send_from_directory, abort, redirect, url_for, request, flash
from flask import current_app as APP
from flask.ext.login import login_required, current_user
from .forms import CreateMessageForm
from .models import Message


message = Blueprint('message', __name__, url_prefix='/message')


@message.route('/add_message', methods=['POST'])
@login_required
def add_message():
	user = current_user
	form = CreateMessageForm()
	if form.validate_on_submit():
		form.add_message(user)
		flash("Your message has been added",'success')
	msg = Message()
	return render_template('user/index.html', form=form, user=user,messages = msg.get_all_messages())
