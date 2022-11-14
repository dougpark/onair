
#import time
import json
import logging
from aqi import datastore
from dotmap import DotMap
from purpleair import PurpleAir

# Import Requests Library
import requests

# load token from external file
# https://stackoverflow.com/a/67948155
# copy config/.token_example to config/.token
# put your token codes between the single quotes
# ensure .token is in your .gitignore so it is not checked into version control
exec(open('aqi/aqi_config/.token').read())

# api_base_url = 'https://www.purpleair.com/json?show='
# api_url = 'https://www.purpleair.com/json?show=104402'

p = PurpleAir(purpleAir_token)

# http://tech.thejoestory.com/2020/09/air-quality-calculation-purple-air-api.html



def calcAQ(Cp, Ih, Il, BPh, BPl):
    a = (Ih - Il)
    b = (BPh - BPl)
    c = (Cp - BPl)
    aq = ((a/b) * c + Il)
    return aq


def purpleAir():
    aqiColor = "#00FF00"
    api_data = ""
    error = None

    # concat base_url with selected sensor_id
    sensor_id = datastore.get_sensor_id()
    # api_url = api_base_url+sensor_id
    logging.info('retrieved sensor_id from database: ' + sensor_id)

    # PurpleAir data!
    try:
        # api_data = requests.get(api_url)
        api_data = p.get_sensor_data(sensor_id)
        logging.info('aqistore - New data received from PurpleAir api.')

        # data = json.loads(api_data.text)
        # results = data['results'][0]
        results = api_data['sensor']
        sensor_label = results['name']
        PM25 = results['pm2.5_atm']
        humidity = results['humidity']
        temp = results['temperature']
        pressure = results['pressure']

        # http://tech.thejoestory.com/2020/09/air-quality-calculation-purple-air-api.html
        pm2 = PM25

        # for row in data["results"]:
        #     pm2 = float(row["PM2_5Value"])
        #     pm2 = pm2 + pm2
        # pm2 = pm2 / 2

        if (pm2 > 350.5):
            aq = calcAQ(pm2, 500, 401, 500, 350.5)
            aqiColor = "#FF0000"
        elif (pm2 > 250.5):
            aq = calcAQ(pm2, 400, 301, 350.4, 250.5)
            aqiColor = "#FF0000"
        elif (pm2 > 150.5):
            aq = calcAQ(pm2, 300, 201, 250.4, 150.5)
            aqiColor = "#FF0000"
        elif (pm2 > 55.5):
            aq = calcAQ(pm2, 200, 151, 150.4, 55.5)
            aqiColor = "#FF0000"
        elif (pm2 > 35.5):
            aq = calcAQ(pm2, 150, 101, 55.4, 35.5)
            aqiColor = "#FF4500"
        elif (pm2 > 12.1):
            aq = calcAQ(pm2, 100, 51, 35.4, 12.1)
            aqiColor = "#FFFF00"
        elif (pm2 > 0):
            aq = calcAQ(pm2, 50, 0, 12, 0)
            aqiColor = "#00FF00"
        aqi = str(round(aq))
    except Exception as e:
        error = 'aqistore - Error getting data from PurpleAir api.'
        logging.warning(error, e)
        return

    data = DotMap()
    data.aqi = aqi
    data.label = sensor_label
    data.aqiColor = aqiColor
    data.temp = temp
    data.humidity = humidity
    data.pressure = pressure
    data.api_error = error
    logging.info('Processed data from PurpleAir api: ')
    logging.info(data.toDict())

    return data
