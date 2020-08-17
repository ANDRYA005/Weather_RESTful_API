from flask import Flask, request, jsonify
import requests
import json
from functools import reduce
import itertools
from datetime import date, datetime
from statistics import median

API_KEY = "X6561E5DQHPZ7KGXEE8WMQMJ2"

app = Flask(__name__)


def average(lst): 
    return reduce(lambda a, b: a + b, lst) / len(lst) 

def period_to_start_end(period):
    start = period.split('|')[0]
    end = period.split('|')[1]
    return start, end

def get_num_days(start, end):
    start_date = datetime.strptime(start, '%Y-%m-%d')
    end_date = datetime.strptime(end, '%Y-%m-%d')
    delta = end_date - start_date
    return delta.days


def get_num_obs(start, end, aggregator):
    num_days = get_num_days(start, end)
    num_hours = num_days*24
    num_obs = num_hours//aggregator
    return num_obs


def get_weather(city, start, end):
    aggregator = 1
    num_obs = get_num_obs(start, end, aggregator)
    while num_obs > 100:
        aggregator += 1
        num_obs = get_num_obs(start, end, aggregator)
    url = f'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/weatherdata/history?&aggregateHours={aggregator}&startDateTime={start}T00:00:00&endDateTime={end}T00:00:00&unitGroup=uk&contentType=json&dayStartTime=0:0:00&dayEndTime=0:0:00&location={city}&key={API_KEY}'
    # HTTP requests
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        return e, 1

    # response = requests.get(url)

    return response.json(), 0

def is_valid_dates(start, end):
    try:
        datetime.strptime(start, '%Y-%m-%d')
        datetime.strptime(end, '%Y-%m-%d')
        return True
    except:
        return False

def get_weather_results(city, period):
    weather_summary = {}

    try:
        start_date, end_date = period_to_start_end(period)
    except:
        error = "Your period is invalid. The correct format is 'start_date|end_date' in the following date format '%Y-%m-%d|%Y-%m-%d'."
        return error, 1

    if not is_valid_dates(start_date, end_date):
        error = "One of your dates are invalid. The correct date format is '%Y-%m-%d'."
        return error, 1

    weather_json, status = get_weather(city, start_date, end_date)
    
    if status == 1:
        error = weather_json
        return error, 1

    if 'errorCode' in weather_json:
        error = weather_json['message']
        return error, 1
    
    weather_periods_info = weather_json['locations'][city]['values']
    
    temps = [weather_dict['temp'] for weather_dict in weather_periods_info]
    min_temps = [weather_dict['mint'] for weather_dict in weather_periods_info]
    max_temps = [weather_dict['maxt'] for weather_dict in weather_periods_info]
    humidities = [weather_dict['humidity'] for weather_dict in weather_periods_info]

    weather_summary['average_temp'] = round(average(temps), 2)
    weather_summary['median_temp'] = round(median(temps), 2)
    weather_summary['min_temp'] = min(min_temps)
    weather_summary['max_temp'] = max(max_temps)

    weather_summary['average_humidity'] = round(average(humidities), 2)
    weather_summary['median_humidity'] = round(median(humidities), 2)
    weather_summary['min_humidity'] = min(humidities)
    weather_summary['max_humidity'] = max(humidities)

    return weather_summary, 0


@app.route('/weather')
def weather_conditions():
    city  = request.args.get('city', None, type=str)
    period  = request.args.get('period', None, type=str)
   
    weather_results, indicator = get_weather_results(city, period)
    if indicator == 1:
       return f'Error: {weather_results}' 
    return jsonify(weather_results)


@app.route('/')
def home():
    return 'Made it!'


app.run()