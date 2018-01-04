#!/usr/bin/env python3
import xml.etree.ElementTree as ET
import sqlite3
from hashlib import sha1
import os
import shutil
import cv2



def create_or_open_database(db_file):
    global db
    db = sqlite3.connect(db_file)
    


def close_database():
    db.commit()
    db.close()

def create_words_table():
    conn = db.cursor()
    conn.execute('drop table IF EXISTS words')
    db.commit()
    sql="CREATE TABLE words(id INTEGER primary key,label_id INTEGER,name TEXT)"
    conn.execute(sql)
    sql="insert or ignore into words(id,label_id,name) values(?,?,?)"

    
def create_groups_table():
    conn = db.cursor()
    conn.execute('drop table IF EXISTS groups')
    db.commit()
    sql="CREATE TABLE groups(id INTEGER primary key,name TEXT)"
    conn.execute(sql)
    sql="insert or ignore into groups(id,name) values(?,?)"
    conn.execute(sql,(1,'Training'))
    conn.execute(sql,(2,'Testing'))
    
def create_validation_results_table():
    conn = db.cursor()
    conn.execute('drop table IF EXISTS validation_results')
    db.commit()
    sql="CREATE TABLE validation_results(id INTEGER primary key,session_timestamp,file_id,boxed_annotation,expected_label,calculated_label,score,result_vector)"
    conn.execute(sql)
    sql="insert or ignore into validation_results(id,session_timestamp,file_id,boxed_annotation,expected_label,calculated_label,score,result_vector) values(?,?,?,?,?,?,?,?)"
    #conn.execute(sql,(1,'Training'))


            
def create_other_table():
    conn = db.cursor()
    conn.execute('drop table IF EXISTS files')
    conn.execute('drop table IF EXISTS boxed_annotations')
    conn.execute('drop table IF EXISTS labels')
    db.commit()
    conn.execute("CREATE TABLE files(id INTEGER primary key,name TEXT,ext TEXT)")
    conn.execute("CREATE TABLE boxed_annotations(id INTEGER primary key,label_id INTEGER,group_id INTEGER,file_id INTEGER,x INTEGER,y INTEGER,w INTEGER,h INTEGER)")
    conn.execute("CREATE TABLE labels(id INTEGER primary key,name TEXT,description TEXT)")

    label_list = list()
    
    files_sql="insert or ignore into files(id,name,ext) values(?,?,?)"
    labels_sql="insert or ignore into labels(id,name,description) values(?,?,?)"
    boxed_annotations_sql="insert or ignore into boxed_annotations(id,label_id,group_id,file_id,x,y,w,h) values(?,?,?,?,?,?,?,?)"
    fileNum = 1;
    labels = []
    with open('val.txt') as f:
        for l in f:
            filename, label ,roi, groups = l.split(', ')
            
            basename = os.path.basename(filename)
            name, ext = os.path.splitext(basename)
            groups = groups.strip('\n')
            #print(groups)
            #print(len(groups))
            # Source file path
            src = os.path.abspath(filename)

            if(len(roi) == 0):
                x = y = w = h = 0;
            elif(len(roi) < 8):
                print("Error roi format")
                exit
            else:
                x, y, w, h = roi.split(' ')
                x = int(x)
                y = int(y)
                w = int(w)
                h = int(h)
                
            if(fileNum == 1):
                labels.append(label)
            else:
                if(labels.count(label) == 0):
                    labels.append(label)
                
            # Destination file path
            checksum = sha1(name.encode()).hexdigest()
            dst = os.path.join('data', checksum[0:2])
            dst = os.path.join(dst, checksum[2:4])
            if not os.path.exists(dst):
                os.makedirs(dst)
            dst = os.path.join(dst, name + ext)

            shutil.copyfile( src, dst )

            cursor = db.cursor()
            # Insert File into database
            cursor.execute("insert into files (id, name, ext) values (?,?,?)", (fileNum,name, ext))
            fileid = cursor.lastrowid
            #cursor.execute("insert into files (id, name) values (?,?,?)", (fileNum,name, ext))
            # Insert Images with ROI into the database

            if groups == 'train':
                cursor.execute("insert into boxed_annotations \
                        (id,group_id, file_id, label_id, x, y, w, h) values (?,?,?,?,?,?,?,?)",
                        (fileNum,1, fileid, (labels.index(label))+1, x, y, w, h, ))
            elif groups == 'validate':
                cursor.execute("insert into boxed_annotations \
                        (id,group_id, file_id, label_id, x, y, w, h) values (?,?,?,?,?,?,?,?)",
                        (fileNum,2, fileid, (labels.index(label))+1, x, y, w, h, ))
            else:
                print("Error groups type")
                exit
            fileNum = fileNum + 1
            
    labels_len = len(labels)
    for i in range(0,labels_len):
       cursor.execute("insert or ignore into labels(id,name) values(?,?)",((i+1),labels[i]))
if __name__=='__main__':
    create_or_open_database("mnist_test.dsx")
    create_groups_table()
    create_validation_results_table()
    create_words_table()
    create_other_table()
    close_database()  

    
