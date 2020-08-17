# Weather RESTful API

## Notes on how to use API

This is a Flask-based API for querying weather data for a given city and period. In order to obtain weather data, the Virtual Crossing Weather API is used (https://www.visualcrossing.com/weather-api). 


### Requests

#### Arguments:

1. city: The city that you would like the weather summary for.
2. period: The period of time to be considered.

Using these arguments, the general form of the requests are as follows:

#### Running locally:
```
http://127.0.0.1:5000/weather?city=<CITY>&period=<START_DATE>|<END_DATE>
```

#### Running deployed app (hosted on Heroku):
```
https://flask-weather-api-app.herokuapp.com/weather?city=<CITY>&period=<START_DATE>|<END_DATE>
```

If the request is succesful, the returned results are the min, max, average and median temperature and humidity for given city and period of time in json format.


## Limitations due to Virtual Crossing

As the API made use of the free Virtual Crossing API plan, there are daily request limits (250) and there are also limits on the results per query (100). To handle the latter, we used their ```aggregateHours``` parameter. When this parameter is set to 1, the data returned is hourly data; when it is set to 2, the hourly data is aggregated to two-hourly data; and so on...
In order to implement this we used the following lines of code:
```
aggregator = 1                                     # hourly data
    num_obs = get_num_obs(start, end, aggregator)  # results per query
    while num_obs > 100:                           # while too many results per query
        aggregator += 1                            # increase aggregation level
```
where ```aggregator``` is then used as their ```aggregateHours``` parameter.
