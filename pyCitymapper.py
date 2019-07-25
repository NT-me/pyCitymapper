# -*- coding: utf-8 -*-

import os
import sys
import json
import math
import requests
import unidecode

API_KEY = "NONE"
REQ_BASE = "https://developer.citymapper.com"
BASE_H = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:32.0)"
SPEC_H = " Gecko/20100101 Firefox/32.0"
USER_AGENT = BASE_H + SPEC_H
HEADERS = {'user-agent': USER_AGENT}

def checkCoverage(pos):
    """
    Return if point is covered by citymapper.

    #############
    pos: WGS84 '<latitude>,<longitude>' format.
    ex : \"51.578973,-0.124147\"

    return true or false

    """
    if API_KEY == "NONE":
        return "API_KEY is not init"
    check = requests.get("https://developer.citymapper.com/api/1/singlepointcoverage/?coord="+ pos +"&key="+API_KEY)
    if check.json()["points"]:
        if check.json()["points"][0]["covered"] == True:
            return True
        elif check.json()["points"][0]["covered"] == False:
            return False
    return "Error code: "+r.status_code


def travelTime(posA, posB, TIME="NONE"):
    """
    Return time transit travel beteween A --> B in minutes.

    ##############
    posA and posB : WGS84 '<latitude>,<longitude>' format.
    ---
    TIME (optionnal): A date & time in ISO-8601
    format, including time zone information.
    If omitted, the travel time is computed for travel at the time of the
    request.
    Results should be most reliable for -1 and +7 days from the current time,
    but times further in the future should give reasonable times
    (not accounting for any holiday schedules).
    """
    if API_KEY == "NONE":
        return "API_KEY is not init"
    if checkCoverage(posA) == True and checkCoverage(posB) == True:
        req = REQ_BASE + "/api/1/traveltime/?startcoord=" + posA + "&endcoord=" + posB
        if TIME != "NONE":
            req = req + "&time=" + TIME +"&time_type=arrival"

        req = req+"&key="+API_KEY
        r=requests.get(req)
        if r.status_code == 200:
            time = r.json()["travel_time_minutes"]
            return time
        else:
            return "Error code: "+r.status_code
    else :
        return "Your points are not covered"

def travelWay(posA, posB):
    """
    Return an json file with all informations for transit beteween posA and posB.

    ############
    posA and posB : WGS84 '<latitude>,<longitude>' format.
    """
    
    BASE_URL = "https://citymapper.com/"
    ENDPOINT = "api/7/journeys?start=FROM&end=TO&region_id=fr-paris"
    unformatted_url = BASE_URL + ENDPOINT
    formatted = unformatted_url.replace("FROM", posA).replace("TO", posB)

    try:
        response = requests.get(formatted, headers=HEADERS)
    except Exception as e:
        raise e
    content = response.content
    content = unidecode.unidecode(content.decode('utf-8'))
    content = json.loads(content)

    return content
