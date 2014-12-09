#! /usr/bin/env python -u
# coding=utf-8
import csv
import json
import pickle
import re
import dateutil.parser
from iPhone_Backup.contacts import get_contacts
from iPhone_Backup.location import get_location

__author__ = 'xl'

from iPhone_Backup._sms_backup import main, trunc


def alias_generator(contacts):
    amap = {}
    if contacts:
        for a in contacts:
            key = a[1]
            alias = a[0]
            # Is key an email address?
            m2 = re.search('@', key)
            if not m2:
                key = trunc(key)
            amap[key] = alias
            # amap[key] = alias.decode('utf-8')
    return amap


def get_messages():
    args = ['-m', 'Me']
    aliases = alias_generator(get_contacts())
    messages = main(args, aliases)
    return messages


def is_unknown(m):
    if m['to'] != "Me" and not isinstance(m['to'], tuple):
        return False

    if m['from'] != "Me" and not isinstance(m['from'], tuple):
        return False

    return True


def filter_message(messages=None):
    messages = messages or get_messages()
    messages = [m for m in messages if is_unknown(m)]
    for m in messages:
        del m['text']
    return messages


def save_first_names(messages):
    names = get_name_dict()
    all_names = set([m['to'] for m in messages] + [m['from'] for m in messages])
    first_names = set([m[0] for m in all_names])
    with open("first_name.csv", "w") as fp:
        for name in sorted(first_names):
            if name not in names:
                fp.write("%s\tm\n" % name)


def get_name_dict():
    names = {}
    with open("first_name.csv", "r") as fp:
        for row in csv.reader(fp, delimiter='\t'):
            names[row[0].lower()] = row[1]
    return names


def add_gender(messages):
    names = get_name_dict()

    for m in messages:

        if m['to'] != "Me" and isinstance(m['to'], tuple) and m['to'][0]:
            m['gender'] = names.get(m['to'][0].lower(), "u")

        if m['from'] != "Me" and isinstance(m['from'], tuple) and m['from'][0]:
            m['gender'] = names.get(m['from'][0].lower(), "u")

    return messages


def add_sender_status(messages):
    for m in messages:
        m['is_sender'] = True if m['from'] == "Me" else False

    return messages


def fix_dates(messages):
    for m in messages:
        m['date'] = dateutil.parser.parse(m['date'])
    return messages

def add_location(messages):
    for m in messages:
        m['location'] = get_location(m['date'])
    return messages


def save_object(ret, name):
    with open(name, "wb") as fp:
        pickle.dump(ret, fp)


def get_processed_messages():
    return load_processed_messages()
    ret = filter_message()
    ret = add_gender(ret)
    ret = add_sender_status(ret)
    ret = add_location(ret)
    save_object(ret, "cache.pickle")
    return ret


def load_object(name):
    with open(name, "rb") as fp:
        return pickle.load(fp)


def load_processed_messages():
    return load_object("cache.pickle")

if __name__ == "__main__":
    data = get_processed_messages()
    save_first_names(data)
    with open("../messages.json", "a") as fp:
        json.dump(data, fp, indent=4, separators=(',', ': '))

        # save_first_names(messages)