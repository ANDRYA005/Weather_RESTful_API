# Weather RESTful API

## Notes on how to use API

This is a Flask-based API for querying weather data for a given city and period. In order to obtain weather data, the Virtual Crossing Weather API is used (https://www.visualcrossing.com/weather-api). 


### Requests
The general form of the requests are as follows:

#### Running locally:
```
http://127.0.0.1:5000/weather?city=<CITY>&period=<START_DATE>|<END_DATE>
```

#### Running deployed app (hosted on Heroku):
```
https://flask-weather-api-app.herokuapp.com/weather?city=<CITY>&period=<START_DATE>|<END_DATE>
```

If the request is succesful, the returned results are the min, max, average and median temperature and humidity for given city and period of time in json format.
