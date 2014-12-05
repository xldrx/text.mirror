#! /usr/bin/env python -u
# coding=utf-8
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


init()
