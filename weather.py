from datetime import datetime

import schedule as schedule
import tweepy
import requests
import json

# Authenticate to Twitter
consumerKey = ""  # Api key
consumerSecret = ""  # Api secret key
accesstoken = ""
accessTokenSecret = ""


def tweetHourlyText():
    auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
    auth.set_access_token(accesstoken, accessTokenSecret)

    api = tweepy.API(auth, wait_on_rate_limit=True,
                     wait_on_rate_limit_notify=True)

    try:
        api.update_status(getHourlyText())
        print("Tweeted! ")
    except:
        print("Error during authentication")


def tweetDailyText():
    auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
    auth.set_access_token(accesstoken, accessTokenSecret)

    api = tweepy.API(auth, wait_on_rate_limit=True,
                     wait_on_rate_limit_notify=True)

    try:
        api.update_status(getDailyText())
        print("Tweeted! ")
    except:
        print("Error during authentication")


def getIcon(attribList):
    weatherIconsDict = {
        "sunrise": '\U0001F305',
        "sunset": '\U0001F307',
        "210 211 212": '\U0001F329',  # just thunder
        "201 202 203 230 231 232": '\U000026C8',  # thunder with rain
        "300 301 302 310 311 312 313 314 321": '\U0001F327',  # light drizzle
        "500 501 502 503": '\U0001F326',  # light rain
        "511": '\U00002744',  # freezing rain
        "504 520 521 522 531": '\U00002614',  # rain with umbrella
        "611 612 613": '\U0001F328',  # sleet
        "600 601 602 615 615 620 621 622": '\U00002603',  # snow
        "701 711 721 731 741 751 761 762": '\U0001F32B',  # mist
        "771": '\U0001F300',  # cyclone
        "781": '\U0001F32A',  # tornado
        "01d": '\U00002600',  # if 800, CHECK IF DAY OR NIGHT
        "01n": '\U0001F311',
        "801": '\U000026C5',  # barely clouds
        "802": '\U0001F324',  # less clouds
        "803 804": '\U00002601',  # overcast clouds
    }
    id = str(attribList[0]['id'])
    if id == '800':
        id = str(attribList[0]['icon'])
    for idList in weatherIconsDict.keys():
        separatedString = idList.split(" ")
        if id in separatedString:
            return weatherIconsDict[idList]
    return False


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


def mkHourlyReport(dictionary):
    weather = dictionary['weather']
    mainBody = dictionary['main']
    sys = dictionary['sys']

    text = getTemp(mainBody['temp']) + ', ' + getIcon(weather) + " " + str(weather[0]['main']) + " (" + str(
        weather[0]['description'] + ").\n") + \
           "Actual Feel: " + str(getTemp(mainBody['feels_like'])) + ".\n"
    text += "Temperature across London ranges between [" + str(getTemp(mainBody['temp_min'])) + ", " \
            + str(getTemp(mainBody['temp_max'])) + "]."
    return text


def mkDailyReport(dictionary):
    sys = dictionary['sys']
    date = datetime.utcnow()

    text = "Sunrise & Sunset Times for London, " + str(date.day) + "/" + str(date.month) + "/" + str(
        date.year) + ":\n" + \
           "Sunrise \U0001F305: " + formattedTime(sys['sunrise']) + ".\n" + \
           "Sunset \U0001F307: " + formattedTime(sys['sunset']) + "."
    return text


def getHourlyText():
    # make class that breaks weather json into object, make readable string, put onto twitter
    if not getData():
        return "There is no data available at the moment. "
    return mkHourlyReport(getData())


def getDailyText():
    # make class that breaks weather json into object, make readable string, put onto twitter
    if not getData():
        return "There is no data available at the moment. "
    return mkDailyReport(getData())


schedule.every().hour.do(tweetHourlyText)
schedule.every().day.at("00:00").do(tweetDailyText)

while True:
    print("Running")
    schedule.run_pending()
