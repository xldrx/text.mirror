#! /usr/bin/env python -u
# coding=utf-8

__author__ = 'xl'

import sqlite3
import os
import re
import sys
import fnmatch
# import logging
import shutil
import tempfile


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
        #XL logging.warning("No SMS db found.")
        path = None
    elif len(paths) == 1:
        path = paths[0]
    else:
        #XL logging.warning("Multiple SMS dbs found. Using most recent db.")
        path = most_recent(paths)
    return path


def copy_contacts_db(db):
    """Copy db to a tmp file, and return filename of copy."""
    try:
        orig = open(db, 'rb')
    except:
        #XL logging.error("Unable to open DB file: %s" % db)
        sys.exit(1)

    try:
        copy = tempfile.NamedTemporaryFile(delete=False)
    except:
        #XL logging.error("Unable to make tmp file.")
        orig.close()
        sys.exit(1)

    try:
        shutil.copyfileobj(orig, copy)
    except:
        #XL logging.error("Unable to copy DB.")
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

        return contacts

    except sqlite3.Error as e:
        #XL logging.error("Unable to access %s: %s" % (COPY_DB, e))
        sys.exit(1)
    finally:
        if conn:
            conn.close()
        if COPY_DB:
            os.remove(COPY_DB)
            #XL logging.debug("Deleted COPY_DB: %s" % COPY_DB)


def normalize(address):
    return ''.join(re.findall('(\d)', address))[-11:]

if __name__ == '__main__':
    get_contacts()

