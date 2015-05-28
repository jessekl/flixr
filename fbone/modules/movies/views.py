# -*- coding: utf-8 -*-
import re
import json
import datetime
import twilio.twiml

import requests
from bs4 import BeautifulSoup
from flask import Blueprint, render_template, request, flash, jsonify,redirect,url_for
from lxml import html
from flask.ext.login import login_required, current_user
from .models import Movie
from fbone.extensions import db

from fbone.modules.user import User

# Download the twilio-python library from http://twilio.com/docs/libraries
from twilio.rest import TwilioRestClient
 
# Find these values at https://twilio.com/user/account
ACCOUNT_SID = "AC1cc94a70c3902ceb9a089bcc84110d51" 
AUTH_TOKEN = "f6e627e528eebc61ae0987bcafef6541" 

client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)
 


movies = Blueprint('movies', __name__, url_prefix='/movies')

YEAR = 2015
BASE_URL = "http://www.imdb.com/movies-coming-soon/"
BASE_IMG_URL = "http://www.omdbapi.com/?t="

@movies.route('/upcoming', methods=['GET', 'POST'])
#@login_required
def list_upcoming():
    today = datetime.date.today()
    month = today.month
    movies_dict = {}
    movie_list = Movie.query.all()
    if len(movie_list) > 1:
        return render_template("movies/index.html", movies_list=movie_list)
    else:
        for m in range(month + 1, month + 7):
        	req = requests.get(BASE_URL + str(YEAR) + "-" + str(m).zfill(2))
        	data = req.text
        	s = BeautifulSoup(data)
        	for day in s.findAll("h4", {"class":"li_group"}):
        		release_date = day.text.split()
        		release_month = release_date[0]
        		release_day = release_date[1].zfill(2)
        		release_date = release_month + " " + release_day
        		movies = day.find_next_siblings()
        		movies_list = []
        		for movie in movies:
        			if movie.name != "div":
        				break
        			table = movie.find("table")
        			name = table.find("h4")
        			movie_name = re.sub('([0-9]+)', '', name.text.strip())
        			movie_name = movie_name[:-2].strip()
        			movie_year = name.text.split()[-1].strip('(').strip(')')
        			img_req = requests.get(BASE_IMG_URL + movie_name + "&y=" + movie_year + "&plot=short&r=json")
        			movie_json = json.loads(img_req.text)
        			if movie_json.has_key("Poster"):
        			    movie_db = Movie(name=movie_name, release_date=release_date, poster_url=movie_json["Poster"])
                        db.session.add(movie_db)
                        db.session.commit()

        		movies_dict[release_date] = movies_list
        movie_list = Movie.query.all()	
        return render_template("movies/index.html", movies_list=movie_list)


@movies.route('/add', methods=['GET', 'POST'])
#@login_required
def add():    
    the_id = request.json['id']
    the_movie = Movie.query.get(int(the_id))
    print the_movie.name
    #the_movie = Movie.query.get(id=movie_id)
    if request.method == 'POST':
        #add to movie reminder
        
        message = client.messages.create(to="+17726261816", from_="+17722667926",
                                      body="Your reminder is set for " + the_movie.name + "! You will get a text on the release date: " + the_movie.release_date)
        # flash('Movie saved.', 'success')
        return redirect(url_for('movies.list_upcoming'))
    else:
        return redirect(url_for('movies.list_upcoming'))

    





     