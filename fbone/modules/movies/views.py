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
BASE_URL = "http://www.imdb.com/movies-coming-soon/"
@movies.route('/upcoming', methods=['GET', 'POST'])
@login_required
def list_upcoming():
    today = datetime.date.today()
    month = today.month
    for m in range(month, month + 6):
    	req = requests.get(BASE_URL + str(YEAR) + "-" + str(m))
    	data = req.text
    	s = BeautifulSoup(data)
    	
    return render_template("movies/index.html", movies=movies)
     