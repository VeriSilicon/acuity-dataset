# ACUITY ImageNet example

 This folder contains some sample scripts on how to create ImageNet dataset from 
 original Images

 - ImageNet.dsx
   Empty ACUITY dataset file, this is a simple sqlite database

    Use sqlitebrowser to view Dataset schema and content
    sqlitebrowser ImageNet.dsx

 - create_imagenet_empty.py 
   This script will parse synset_words.txt and create an empty ImageNet database
   containing only 1000 labels

 - create_imagenet_val_no_resize.py
   This script will parse val.txt and create a dataset for 50000 ILSVRC2012
   validation set. Images will not be in its original format, and not scaled.

    > Need to download original ILSVRC2012 dataset and put into ILSVRC2012 folder

 - create imagenet_val_with_resize.py
   This script will parse val.txt and create a dataset for 50000 ILSVRC2012
   validation set. Images will be prescaled to the size specified. 

    > Need to download original ILSVRC2012 dataset and put into ILSVRC2012 folder
