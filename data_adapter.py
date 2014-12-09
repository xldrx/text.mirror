#! /usr/bin/env python -u
# coding=utf-8
import calendar
from copy import deepcopy
import dateutil.parser
from iPhone_Backup import messages

__author__ = 'xl'


def init():
    global data
    global contacts

    data = messages.get_processed_messages()
    contacts = sorted(
        list(set([m['to'] for m in data if m["to"] != "Me"] + [m['from'] for m in data if m['from'] != "Me"])))


init()


def get_contacts():
    return list(enumerate(contacts))


def get_messages(include_sends=True, include_recieves=True, from_date=None, to_date=None, only_from=[]):
    ret = []
    from_date = dateutil.parser.parse(from_date) if from_date and isinstance(from_date, unicode) else from_date
    to_date = dateutil.parser.parse(to_date) if to_date and isinstance(to_date, unicode) else to_date
    for index, contact in enumerate(only_from):
        if isinstance(contact, int):
            only_from[index] = contacts[contact]
        if isinstance(contact, str):
            only_from[index] = contacts[int(contact)]

    for m in data:
        if not include_sends and m['from'] == 'Me':
            continue

        if not include_recieves and m['to'] == 'Me':
            continue

        if to_date and m['date'] > to_date:
            continue

        if from_date and m['date'] < from_date:
            continue

        if len(only_from) > 0 and m['to'] not in only_from and m['from'] not in only_from:
            continue

        record = deepcopy(m)
        record['date'] = record['date'].isoformat()

        ret.append(record)

    return ret


def get_overview():
    return [
        [{
             "name": 'Girls',
             "count": len([m for m in data if 'gender' in m and m['gender'] == 'f'])
         },
         {
             "name": 'Boys',
             "count": len([m for m in data if 'gender' in m and m['gender'] == 'm'])
         }],

        [{
             "name": 'Girls',
             "count": len([m for m in data if 'gender' in m and m['gender'] == 'f' and m['is_sender']])
         },
         {
             "name": 'Boys',
             "count": len([m for m in data if 'gender' in m and m['gender'] == 'm' and m['is_sender']])
         }],

        [{
             "name": 'Girls',
             "count": len([m for m in data if 'gender' in m and m['gender'] == 'f' and not m['is_sender']])
         },
         {
             "name": 'Boys',
             "count": len([m for m in data if 'gender' in m and m['gender'] == 'm' and not m['is_sender']])
         }],


    ]


def get_locations():
    return [
        [{'lng': m['location'][0], 'lat': m['location'][1]} for m in data if m['location']],
        [{'lng': m['location'][0], 'lat': m['location'][1]} for m in data if
         m['location'] and 'gender' in m and m['gender'] == 'm'],
        [{'lng': m['location'][0], 'lat': m['location'][1]} for m in data if
         m['location'] and 'gender' in m and m['gender'] == 'f']
    ]


def get_times():
    ret = [
        [
            [0] * 7,
            [0] * 24,
            [0] * 12
        ],
        [
            [0] * 7,
            [0] * 24,
            [0] * 12
        ],
        [
            [0] * 7,
            [0] * 24,
            [0] * 12
        ]
    ]
    time_dict = [[], [], []]

    for m in data:
        ret[0][0][m['date'].weekday()] += 1
        ret[0][1][m['date'].hour] += 1
        ret[0][2][m['date'].month - 1] += 1

        ret[1][0][m['date'].weekday()] += 1 if 'gender' in m and m['gender'] == 'm' else 0
        ret[1][1][m['date'].hour] += 1 if 'gender' in m and m['gender'] == 'm' else 0
        ret[1][2][m['date'].month - 1] += 1 if 'gender' in m and m['gender'] == 'm' else 0

        ret[2][0][m['date'].weekday()] += 1 if 'gender' in m and m['gender'] == 'f' else 0
        ret[2][1][m['date'].hour] += 1 if 'gender' in m and m['gender'] == 'f' else 0
        ret[2][2][m['date'].month - 1] += 1 if 'gender' in m and m['gender'] == 'f' else 0

    for i in range(12):
        time_dict[2].append({
            "Name": calendar.month_name[i + 1],
            "id": i,
            "gender":"m",
            "count": ret[1][2][i],
            "percentage": 1.0 * ret[1][2][i] / (ret[1][2][i]+ret[2][2][i])
        })

        time_dict[2].append({
            "Name": calendar.month_name[i + 1],
            "id": i,
            "gender": "f",
            "count": ret[2][2][i],
            "percentage": 1.0 * ret[2][2][i] / (ret[1][2][i]+ret[2][2][i])
        })

    for i in range(24):
        time_dict[1].append({
            "Name": i,
            "id": i,
            "gender":"m",
            "count": ret[1][1][i],
            "percentage": 1.0 * ret[1][1][i] / (ret[1][1][i]+ret[2][1][i])
        })

        time_dict[1].append({
            "Name": i,
            "id": i,
            "gender": "f",
            "count": ret[2][1][i],
            "percentage": 1.0 * ret[2][1][i] / (ret[1][1][i]+ret[2][1][i])
        })

    for i in range(7):
        time_dict[0].append({
            "Name": calendar.day_name[i],
            "id": i,
            "gender":"m",
            "count": ret[1][0][i],
            "percentage": 1.0 * ret[1][0][i] / (ret[1][0][i]+ret[2][0][i])
        })

        time_dict[0].append({
            "Name": calendar.day_name[i],
            "id": i,
            "gender": "f",
            "count": ret[2][0][i],
            "percentage": 1.0 * ret[2][0][i] / (ret[1][0][i]+ret[2][0][i])
        })

    return ret, time_dict


def get_time_ranges():
    return {
        'min': min([m['date'] for m in data]).isoformat(),
        'max': max([m['date'] for m in data]).isoformat()
    }