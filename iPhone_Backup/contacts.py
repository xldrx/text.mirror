#! /usr/bin/env python -u
# coding=utf-8

__author__ = 'xl'

import sqlite3
import os
import re
import sys
import fnmatch
import logging
import shutil
import tempfile

from time import localtime, strftime

# Global variables
ORIG_DB = 'test.db'
COPY_DB = None


def most_recent(paths):
    """Return path of most recently modified file."""
    paths.sort(key=lambda x: os.path.getmtime(x))
    return paths[-1]


def find_contacts_db():
    """Find contacts db and return its filename."""
    db_name = '31bb7ba8914766d4ba40d6dfb6113c8b614be442'
    mac_dir = '%s/Library/Application Support/MobileSync' % os.path.expanduser('~')
    paths = []
    for root, dirs, files in os.walk(mac_dir):
        for basename in files:
            if fnmatch.fnmatch(basename, db_name):
                path = os.path.join(root, basename)
                paths.append(path)
    if len(paths) == 0:
        logging.warning("No SMS db found.")
        path = None
    elif len(paths) == 1:
        path = paths[0]
    else:
        logging.warning("Multiple SMS dbs found. Using most recent db.")
        path = most_recent(paths)
    return path


def copy_contacts_db(db):
    """Copy db to a tmp file, and return filename of copy."""
    try:
        orig = open(db, 'rb')
    except:
        logging.error("Unable to open DB file: %s" % db)
        sys.exit(1)

    try:
        copy = tempfile.NamedTemporaryFile(delete=False)
    except:
        logging.error("Unable to make tmp file.")
        orig.close()
        sys.exit(1)

    try:
        shutil.copyfileobj(orig, copy)
    except:
        logging.error("Unable to copy DB.")
        sys.exit(1)
    finally:
        orig.close()
        copy.close()
    return copy.name


def get_contacts():
    ORIG_DB = find_contacts_db()
    COPY_DB = copy_contacts_db(ORIG_DB)

    conn = None

    try:
        conn = sqlite3.connect(COPY_DB)
        cur = conn.cursor()
        query = 'SELECT value, First, Last FROM ABMultiValue as v, ABPerson as p WHERE v.record_id = p.ROWID AND v.property = 3'
        cur.execute(query)

        contacts = []
        for value, first, last in cur.fetchall():
            contacts.append(((first, last), normalize(value)))

        # groups = {}
        # for address, date, text, flags in fetchall(sms, 'SELECT address, date, text, flags FROM message'):
        # address = normalize(address)
        #     assert address
        #     conversation = (strftime('%Y-%m-%d %H:%M:%S %a', localtime(date)), text, flags)
        #     if address in groups:
        #         groups[address].append(conversation)
        #     else:
        #         groups[address] = [conversation]

        return contacts

    except sqlite3.Error as e:
        logging.error("Unable to access %s: %s" % (COPY_DB, e))
        sys.exit(1)
    finally:
        if conn:
            conn.close()
        if COPY_DB:
            os.remove(COPY_DB)
            logging.debug("Deleted COPY_DB: %s" % COPY_DB)


def normalize(address):
    return ''.join(re.findall('(\d)', address))[-11:]

if __name__ == '__main__':
    get_contacts()

