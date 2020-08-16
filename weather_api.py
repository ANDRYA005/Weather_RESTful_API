from flask import Flask, request
import requests
import json
from functools import reduce
import itertools
from datetime import date, datetime
from statistics import median

API_KEY = "X6561E5DQHPZ7KGXEE8WMQMJ2"

weather_summary = {}
CITY = 'Johannesburg'
START_DATE = "2019-06-13"
END_DATE = "2019-06-30"


app = Flask(__name__)



@app.route('/weather')
def weather_conditions():
   city  = request.args.get('city', None, type=str)
   period  = request.args.get('period', None, type=str)
   return f'{summary} , {change}'

app.run()