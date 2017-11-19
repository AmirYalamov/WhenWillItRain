import json
from datetime import datetime

import PelmorexController


def nextPrecipToString(location):
    locationCode = getLocationCode(location)

    if isinstance(locationCode, int):
        if locationCode == 204:
            return "No location found."
        else:
            return "An error occurred finding a location: HTTP status code %d." % locationCode

    precipStartStop = PelmorexController.getShortTerm(locationCode)
    precipCurrent = PelmorexController.getPrecipStartStop(locationCode)

    if isinstance(precipStartStop, int) or isinstance(precipCurrent, int):
        return "An error occurred getting precipitation data: HTTP status code %d." % precipStartStop

    startRain = -1
    endRain = -1

    i = 0

    while i < 32:
        if float(precipStartStop["data"][i]["rain"]) != 0:
            startRain = i
            while i < 32:
                i += 1
                if float(precipStartStop["data"][i]["rain"]) == 0:
                    endRain = i
                    break
            break
        i += 1

    startSnow = -1
    endSnow = -1

    i = 0

    while i < 32:
        if float(precipStartStop["data"][i]["snow"]) != 0:
            startSnow = i
            while i < 32:
                i += 1
                if float(precipStartStop["data"][i]["snow"]) == 0:
                    endSnow = i
                    break
            break
        i += 1

    isCurrentPrecipitation = True

    eventsArray = precipCurrent["data"]["events"]
    eventsArrayStr = json.dumps(eventsArray)
    if "[]" in eventsArrayStr:
        isCurrentPrecipitation = False

    print(startRain)
    print(endRain)
    print(startSnow)
    print(endSnow)
    print(isCurrentPrecipitation)


def getLocationCode(location):
    locationData = PelmorexController.getLocationData(location)

    if isinstance(locationData, int):
        return locationData

    return locationData["dataCode"]


nextPrecipToString("london%20on")
