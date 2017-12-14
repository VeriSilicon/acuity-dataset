#!/usr/bin/python
import xml.etree.ElementTree as ET
import sqlite3
from hashlib import sha1
import os
import shutil

groups = {'Training':1, 'Testing':2}
labels = {'aeroplane':1, 'bicycle':2, 'bird':3, 'boat':4, 'bottle':5, 'bus':6, 'car':7,
          'cat':8, 'chair':9, 'cow':10, 'diningtable':11, 'dog':12, 'horse':13, 'motorbike':14,
          'person':15, 'pottedplant':16, 'sheep':17, 'sofa':18, 'train':19, 'tvmonitor':20}

def open_db():
    global db
    db = sqlite3.connect('Default.dsx')

    # Insert Groups
    cursor = db.cursor()
    cursor.execute("insert or ignore into groups (name,id) values (?,?)", ('Training', groups['Training'],))
    cursor.execute("insert or ignore into groups (name,id) values (?,?)", ('Testing', groups['Testing'],))

    # Insert Labels
    for l,i in labels.iteritems():
        cursor.execute("insert or ignore into labels (name, id) values (?,?)", (l,i,))

def close_db():
    db.commit()
    db.close()

def import_data():
    with open('ImageSets/Main/train.txt') as t:
        for l in t:
            parse_xml('Training', 'Annotations/' + l.rstrip() + '.xml')
    with open('ImageSets/Main/val.txt') as v:
        for l in v:
            parse_xml('Testing', 'Annotations/' + l.rstrip() + '.xml')

def parse_xml(group, source):
    tree = ET.parse(source)
    root = tree.getroot()

    # Parse XML to understand filename
    folder = root.find('folder').text
    filename = root.find('filename').text
    name, ext = os.path.splitext(filename)
    entry = group + '_' + name

    # Source file path
    src = os.path.join('JPEGImages', filename)

    # Destination file path
    checksum = sha1(entry.encode()).hexdigest()
    dst = os.path.join('data', checksum[0:2])
    dst = os.path.join(dst, checksum[2:4])
    if not os.path.exists(dst):
        os.makedirs(dst)
    dst = os.path.join(dst, entry + ext)

    shutil.copyfile(src, dst)

    cursor = db.cursor()

    # Insert File into database
    cursor.execute("insert into files (name, ext) values (?,?)", (entry, ext))
    fileid = cursor.lastrowid

    # Insert Images with ROI into the database
    for obj in root.findall('object'):
        label = obj.find('name').text
        box = obj.find('bndbox')
        x = int(box.find('xmin').text)
        y = int(box.find('ymin').text)
        w = int(box.find('xmax').text) - x
        h = int(box.find('ymax').text) - y

        cursor.execute("insert into boxed_annotations \
                        (group_id, file_id, label_id, x, y, w, h) values (?,?,?,?,?,?,?)",
                        (groups[group], fileid, labels[label], x, y, w, h, ))


def main():
    print("Start progress\n")
    open_db()
    import_data()
    #parse_xml('Training', 'Annotations/000005.xml')
    close_db()

if __name__ == '__main__':
    try:
        main()
    except Exception as err:
        print('Error: {}'.format(err))

