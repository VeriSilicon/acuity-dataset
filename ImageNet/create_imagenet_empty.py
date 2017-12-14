#!/usr/bin/python
#
# This script creates an empty ACUITY dataset containing 1000-class labels
#
import xml.etree.ElementTree as ET
import sqlite3
from hashlib import sha1
import os
import shutil

groups = {'Training':1, 'Testing':2}
labels = {}
descriptions = {}

def open_db():
    global db
    db = sqlite3.connect('ImageNet.dsx')

    # Insert Groups
    cursor = db.cursor()
    cursor.execute("insert or ignore into groups (name,id) values (?,?)", ('Training', groups['Training'],))
    cursor.execute("insert or ignore into groups (name,id) values (?,?)", ('Testing', groups['Testing'],))

    # Insert Labels
    for l,i in labels.items():
        cursor.execute("insert or ignore into labels (name, id, description) values (?,?,?)", (l,i,descriptions[i]))


def close_db():
    db.commit()
    db.close()

def parse_labels():
    with open('synset_words.txt') as f:
        idx = 1
        for l in f:
            pair = l.split(' ', 1)
            labels[pair[0]] = idx
            descriptions[idx] = pair[1]
            idx = idx + 1

def main():
    print("Start progress\n")
    parse_labels()
    open_db()
    close_db()

if __name__ == '__main__':
    try:
        main()
    except Exception as err:
        print('Error: {}'.format(err))

