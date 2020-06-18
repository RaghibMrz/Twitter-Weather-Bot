from datetime import datetime

import schedule as schedule
import tweepy
import requests
import json


# Authenticate to Twitter
def authToTwitter():
    consumerKey = ""  # Api key
    consumerSecret = ""  # Api secret key
    accesstoken = ""
    accessTokenSecret = ""

    auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
    auth.set_access_token(accesstoken, accessTokenSecret)

    api = tweepy.API(auth, wait_on_rate_limit=True,
                     wait_on_rate_limit_notify=True)

    try:
        api.update_status(getText())
    except:
        print("Error during authentication")


def getData():
    res = requests.get("http://api.openweathermap.org/data/2.5/weather?q=London&appid=d4fc4390acd937bab628275acb03540a")
    if res.status_code == 404:
        return False
    return json.loads(res.text)


def getTemp(kelvinTemp):
    return str(round(float(kelvinTemp) - 273.15, 2)) + '\u00b0C'


def formattedTime(utcString):
    date = datetime.utcfromtimestamp(utcString)
    return str(date.hour) + ":" + str(date.minute) + ":" + str(date.second)


def mkReport(dictionary):
    weather = dictionary['weather']
    mainBody = dictionary['main']
    sys = dictionary['sys']

    text = getTemp(mainBody['temp']) + ', ' + str(weather[0]['main']) + " (" + str(weather[0]['description'] + ").\n")
    text += "Actually feels like " + str(getTemp(mainBody['feels_like'])) + \
            ". Temperature today will lie between [" + str(getTemp(mainBody['temp_min'])) + ", " \
            + str(getTemp(mainBody['temp_max'])) + "].\n" + \
            "Sunrise today is at: " + formattedTime(sys['sunrise']) + ", " + \
            "sunset: " + formattedTime(sys['sunset']) + "."
    return text


def getText():
    # make class that breaks weather json into object, make readable string, put onto twitter
    if not getData():
        return "There is no data available at the moment. "
    print(mkReport(getData()))
    return mkReport(getData())


schedule.every().hour.do(authToTwitter)

while(True):
    schedule.run_pending()
