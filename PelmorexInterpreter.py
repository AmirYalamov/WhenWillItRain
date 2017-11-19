import json
from datetime import datetime

import PelmorexController


def nextPrecipToString(location, displayRain = True):
    locationCode = getLocationCode(location)

    startRain = -1
    endRain = -1

    startSnow = -1
    endSnow = -1

    isCurrentPrecipitation = True

    initiallySnowing = False

    stringType = 0

    outStr = ""
    addStr = ""

    if isinstance(locationCode, int):
        if locationCode == 204:
            return "No location found."
        else:
            return "An error occurred finding a location: HTTP status code %d." % locationCode

    precipStartStop = PelmorexController.getShortTerm(locationCode)
    precipCurrent = PelmorexController.getPrecipStartStop(locationCode)

    if isinstance(precipStartStop, int) or isinstance(precipCurrent, int):
        return "An error occurred getting precipitation data: HTTP status code %d." % precipStartStop

    i = 0

    while i < 32:
        if float(precipStartStop["data"][i]["rain"]) != 0:
            startRain = i
            while i < 32:
                i += 1
                if float(precipStartStop["data"][i]["rain"]) == 0:
                    endRain = i - 1
                    break
            break
        i += 1

    if startRain >= 0:
        startRainDate = datetime.strptime(precipStartStop["data"][startRain]["time"], "%Y-%m-%dT%H:%M:%S")
        startRainPeriod = int(precipStartStop["data"][startRain]["period"])

    if endRain >= 0:
        endRainDate = datetime.strptime(precipStartStop["data"][endRain]["time"], "%Y-%m-%dT%H:%M:%S")
        endRainPeriod = int(precipStartStop["data"][endRain]["period"])
    else:
        endRainDate = datetime.strptime(precipStartStop["data"][31]["time"], "%Y-%m-%dT%H:%M:%S")
        endRainPeriod = int(precipStartStop["data"][31]["period"])

    i = 0

    while i < 32:
        if float(precipStartStop["data"][i]["snow"]) != 0:
            startSnow = i
            while i < 32:
                i += 1
                if float(precipStartStop["data"][i]["snow"]) == 0:
                    endSnow = i - 1
                    break
            break
        i += 1

    if startSnow >= 0:
        startSnowDate = datetime.strptime(precipStartStop["data"][startSnow]["time"], "%Y-%m-%dT%H:%M:%S")
        startSnowPeriod = int(precipStartStop["data"][startSnow]["period"])

    if endSnow >= 0:
        endSnowDate = datetime.strptime(precipStartStop["data"][endSnow]["time"], "%Y-%m-%dT%H:%M:%S")
        endSnowPeriod = int(precipStartStop["data"][endSnow]["period"])
    else:
        endSnowDate = datetime.strptime(precipStartStop["data"][31]["time"], "%Y-%m-%dT%H:%M:%S")
        endSnowPeriod = int(precipStartStop["data"][31]["period"])

    eventsArray = precipCurrent["data"]["events"]
    eventsArrayStr = json.dumps(eventsArray)
    if "[]" in eventsArrayStr:
        isCurrentPrecipitation = False

    if isCurrentPrecipitation:
        startPrecip = int(precipCurrent["data"]["events"][0]["startType"])

        if startPrecip == 3 or startPrecip == 4:
            initiallySnowing = True

    if displayRain:
        if isCurrentPrecipitation and not initiallySnowing:
            stringType = 1
            outStr = "It is currently raining. The rain will "
        elif startRain != -1:
            stringType = 2
            outStr = "It is going to rain on the "
        else:
            stringType = 3
            outStr = "There will be no rain over the next week."
    else:
        if isCurrentPrecipitation and initiallySnowing:
            stringType = 4
            outStr = "It is currently snowing. The snow will "
        elif startSnow != -1:
            stringType = 5
            outStr = "It is going to snow on the "
        else:
            stringType = 6
            outStr = "There will be no snow over the next week."

    if stringType == 1:
        if endRain >= 0:
            addStr = "continue until the " + getTimeOfDay(endRainPeriod) + " of " + endRainDate.strftime("%Y-%m-%d") + \
                "."
            outStr = outStr + addStr
        else:
            addStr = "continue past the " + getTimeOfDay(endRainPeriod) + " of " + endRainDate.strftime("%Y-%m-%d") + \
                "."
            outStr = outStr + addStr
    elif stringType == 2:
        if endRain >= 0:
            addStr = getTimeOfDay(startRainPeriod) + " of " + startRainDate.strftime("%Y-%m-%d") + \
                " and will continue until the " + getTimeOfDay(endRainPeriod) + " of " + \
                endRainDate.strftime("%Y-%m-%d") + "."
            outStr = outStr + addStr
        else:
            addStr = getTimeOfDay(startRainPeriod) + " of " + startRainDate.strftime("%Y-%m-%d") + \
                " and will continue past the " + getTimeOfDay(endRainPeriod) + " of " + \
                endRainDate.strftime("%Y-%m-%d") + "."
            outStr = outStr + addStr
    elif stringType == 4:
        if endSnow >= 0:
            addStr = "continue until the " + getTimeOfDay(endSnowPeriod) + " of " + endSnowDate.strftime("%Y-%m-%d") + \
                "."
            outStr = outStr + addStr
        else:
            addStr = "continue past the " + getTimeOfDay(endSnowPeriod) + " of " + endSnowDate.strftime("%Y-%m-%d") + \
                "."
            outStr = outStr + addStr
    elif stringType == 5:
        if endSnow >= 0:
            addStr = getTimeOfDay(startSnowPeriod) + " of " + startSnowDate.strftime("%Y-%m-%d") + \
                " and will continue until the " + getTimeOfDay(endSnowPeriod) + " of " + \
                endSnowDate.strftime("%Y-%m-%d") + "."
            outStr = outStr + addStr
        else:
            addStr = getTimeOfDay(startSnowPeriod) + " of " + startSnowDate.strftime("%Y-%m-%d") + \
                " and will continue past the " + getTimeOfDay(endSnowPeriod) + " of " + \
                endSnowDate.strftime("%Y-%m-%d") + "."
            outStr = outStr + addStr

    return outStr


def getLocationCode(location):
    locationData = PelmorexController.getLocationData(location)

    if isinstance(locationData, int):
        return locationData

    return locationData["dataCode"]


def getTimeOfDay(period):
    if period == 1:
        return "evening"
    elif period == 2:
        return "night"
    elif period == 3:
        return "morning"
    else:
        return "afternoon"

#print(nextPrecipToString("Toronto"));