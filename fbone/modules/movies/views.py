# -*- coding: utf-8 -*-
import re
import datetime

import requests
from bs4 import BeautifulSoup
from flask import Blueprint, render_template, request, flash
from lxml import html
from flask.ext.login import login_required, current_user


from fbone.modules.user import User


movies = Blueprint('movies', __name__, url_prefix='/movies')

YEAR = 2015
BASE_URL = "http://www.imdb.com/movies-coming-soon"
@movies.route('/upcoming', methods=['GET', 'POST'])
@login_required
def list_upcoming():
    req = requests.get("http://www.imdb.com/movies-coming-soon")
    today = datetime.date.today()
    month = today.month
    data = req.text
    s = BeautifulSoup(data)
    for m in range(month, month + 6):
    	pass
     
