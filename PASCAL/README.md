ACUITY PASCAL VOC2007 Dataset

 This folder contains sample scripts to create ACUITY PASCAL dataset for VOC2007 dataset

 - Default.dsx
   Empty ACUITY dataset file, this is a simple sqlite database

   # Use sqlitebrowser to view Dataset schema and content
   sqlitebrowser Default.dsx

 - create_pascal_database.py
   This script will create a database for Pascal dataset

   # Download VOCtrainval_06-Nov-2007.tar and VOCdevkit_08-June-2007.tar from official 
     PASCAL challenge website
   # Untar VOCtrainval_06-Nov-2007.tar
   # Copy Default.dsx and create_pascal_database.py into 'VOCdevkit/VOC2007' folder
   # Run 'python create_pascal_database.py'

