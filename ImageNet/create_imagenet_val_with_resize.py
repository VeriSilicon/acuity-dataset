#!/usr/bin/python3
import xml.etree.ElementTree as ET
import sqlite3
from hashlib import sha1
import os
import shutil
import cv2

#
# Define newsize to be the size of the input
#  Alexnet/VGG/Resnet/googlenet_v1 - set to 256
#  googlenet_v4 - set to 320
#

newsize = 320
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

def resize_and_crop_image( input_file, output_file, output_side_length = 256):
    '''Takes an image name, resize it and crop the center square
    '''
    img = cv2.imread(input_file)
    height, width, depth = img.shape
    scale = output_side_length * 1.0 / min( height, width )
    if height > width:
        new_height, new_width = int( scale * height ), output_side_length
    else:
        new_height, new_width = output_side_length, int( scale * width )
    resized_img = cv2.resize(img, (new_width, new_height))
    #height_offset = int((new_height - output_side_length) / 2)
    #width_offset = int((new_width - output_side_length) / 2)
    #cropped_img = resized_img[height_offset:height_offset + output_side_length,
    #                          width_offset:width_offset + output_side_length]
    cv2.imwrite(output_file, resized_img)

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

            #shutil.copyfile( src, dst )
            resize_and_crop_image( src, dst, newsize )

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

