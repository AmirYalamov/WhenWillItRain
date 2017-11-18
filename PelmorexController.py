import requests
import json


def getLocationCode(location):
    baseURL = getBaseURL() + "/search/string?keyword="

    finalURL = baseURL + location

    return getResponse(finalURL)


def getPrecipStartStop(locationCode):
    baseURL = getBaseURL() + "/data/ssp?locationcode="

    finalURL = baseURL + locationCode

    return getResponse(finalURL)


def getShortTerm(locationCode):
    baseURL = getBaseURL() + "/data/shortterm?locationcode="

    finalURL = baseURL + locationCode

    return getResponse(finalURL)


def getLongTerm(locationCode):
    baseURL = getBaseURL() + "/data/longterm?locationcode="

    finalURL = baseURL + locationCode

    return getResponse(finalURL)


def getBaseURL():
    return "https://hackathon.pic.pelmorex.com/api"


def getResponse(URL):
    response = requests.get(URL, headers={"accept": "application/json"})

    statusCode = response.status_code

    if statusCode != 200:
        return statusCode

    outStr = response.content.decode('utf8')

    return json.loads(outStr)
