#! /usr/bin/env python -u
# coding=utf-8
from datetime import datetime
import dateutil.parser
import pytz

__author__ = 'xl'

import xml.etree.ElementTree as ET

namespaces = {
    '': "http://www.opengis.net/kml/2.2",
    'gx': "http://www.google.com/kml/ext/2.2",
    'kml': "http://www.opengis.net/kml/2.2",
    'atom': "http://www.w3.org/2005/Atom"
}


def load_history(filename="history-11-13-1982.kml"):
    tree = ET.parse(filename)
    root = tree.getroot()
    return root


def read_locations(root):
    ret = []
    all = root.findall('kml:Document[1]/kml:Placemark[1]/gx:Track[1]/', namespaces=namespaces)
    i = 1
    while i < len(all):
        position = all[i + 1].text.split(' ')
        date = dateutil.parser.parse(all[i].text)
        record = {
            "date": date,
            "location": map(float, position)
        }
        ret.append(record)
        i += 2
    return ret


def get_location(date):
    global locations
    try:
        locations
    except NameError:
        locations = read_locations(load_history())

    last_time = locations[0]['date']
    position = None
    for loc in locations_dict.get(date.date(), []):
        period = (date - last_time).total_seconds() / 3600
        if date > loc['date'] and period <= 4:
            position = loc['location']
        last_time = loc['date']

    return position


def init():
    global locations
    global locations_dict
    locations = read_locations(load_history())
    locations_dict = {}
    for loc in locations:
        date = loc['date'].date()
        locations_dict[date] = locations_dict.get(date, [])
        locations_dict[date].append(loc)



init()