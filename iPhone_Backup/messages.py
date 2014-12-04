#! /usr/bin/env python -u
# coding=utf-8
import json
import re
from iPhone_Backup.contacts import get_contacts

__author__ = 'xl'

from iPhone_Backup._sms_backup import main, strip, trunc

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
    for i in messages: del i['text']
    return messages


if __name__ == "__main__":
    messages = get_messages()
    with open("../messages.json", "w") as fp:
        json.dump(messages, fp, indent=4, separators=(',', ': '))