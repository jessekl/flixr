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
 
    for m in range(month, month + 7):
    	req = requests.get(BASE_URL + str(YEAR) + "-" + str(m).zfill(2))
    	data = req.text
    	s = BeautifulSoup(data)
    	for day in s.findAll("h4", {"class":"li_group"}):
    		release_date = day.text.split()
    		release_month = release_date[0]
    		release_day = release_date[1].zfill(2)
    		print release_month + " " + release_day
    	
    return render_template("movies/index.html", movies=movies)
     