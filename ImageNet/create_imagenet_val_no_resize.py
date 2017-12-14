#!/usr/bin/python3
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


def insert_val():
    group = 'Testing'
    with open('val.txt') as f:
        for l in f:
            filename, label = l.split(' ')
            name, ext = os.path.splitext(filename)
            label = int(label.strip('\n')) + 1

            # Source file path
            src = os.path.join('ILSVRC2012', filename)

            # Destination file path
            checksum = sha1(name.encode()).hexdigest()
            dst = os.path.join('data', checksum[0:2])
            dst = os.path.join(dst, checksum[2:4])
            if not os.path.exists(dst):
                os.makedirs(dst)
            dst = os.path.join(dst, name + ext)

            #shutil.copyfile(src, dst)
            cursor = db.cursor()
            # Insert File into database
            cursor.execute("insert into files (name, ext) values (?,?)", (name, ext))
            fileid = cursor.lastrowid

            # Insert Images with ROI into the database
            cursor.execute("insert into boxed_annotations \
                        (group_id, file_id, label_id, x, y, w, h) values (?,?,?,?,?,?,?)",
                        (groups[group], fileid, label, 0, 0, 0, 0, ))


def main():
    print("Start progress\n")
    parse_labels()
    open_db()
    insert_val()
    close_db()

if __name__ == '__main__':
    try:
        main()
    except Exception as err:
        print('Error: {}'.format(err))

