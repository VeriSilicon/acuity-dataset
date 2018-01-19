# ACUITY Dataset Examples

This package contains information about the database format used by ACUITY
for storing Training and Testing images. Sample scripts for ImageNet and 
PASCAL VOC are also provided. 

## ACUITY supported dataset
### SQLite Database format
ImageNet Example (SQlite)
   
> See ReadMe.md in ImageNet folder for details
   
PASCAL Example (SQlite)
   
> See ReadMe.md in PASCAL folder for details

MNIST and INRIA Example (SQlite)

> Pre-built Dataset for Mnist and INRIA

### Text format
ImageNet Exmaple (Text)

> ImageNet/dataset.txt contains example of the text dataset format

## SQLite Database Format

   Default.dsx is an empty ACUITY SQlite dataset file

    # Use sqlitebrowser to view Dataset schema and content
    sqlitebrowser Default.dsx

    # Tables
    There are 5 tables in the Dataset

    "files" Table
    This table contains the path to the resource files (typically Images) in the
    Database.
        -id: Unique key identifying the file
        -name: File name without extension
        -ext: File extension

    "groups" Table
    This table contains the group entry - "Training" and "Testing"
        - id-name: 1-Training, 2-Testing

    "labels" Table
    This table contains the labels or classes for associated with the dataset. For
    example, ILSVRC dataset contains 1000 classes with each class identifying a
    particular type of objects 
        - id: Unique key identifying the label
        - name: String name for the label
        - description: String description

    "boxed_annotations" Table
    This is the master table which contains information about all the images in the
    dataset using the metadata in the other tables. 
    
        - id: Unique key identifying this annotation
        - label_id: label id associated with this annotation
        - group_id: Identify whether this annotation is used for Training or Testing
        - file_id: The image file for this annotation
        - x/y/w/h: ROI window from the image where this annotation is located

    "validation_results" Table
    This table stores the validation result from running Validation of the network
        - id: Unique key identifying the result
        - session_timestamp: Time Stamp for the inference
        - file_id: Image file used for this inference
        - boxed_annotation: id key into the box_annotation table
        - expected_label/calculated_label
        - score: Top1 score of the inference
        - result_vector: Values from the output vector of the network
 
## Text Dataset format
    
    Text Dataset format is a comma separated text file with each line containing
    the file location and label.

     ./data/ILSVRC2012_val_00000347.JPEG, 472, 0 0 28 28, validate # Use for validate only, crop pad "0,0,28,28", lable is 472.
     ./data/ILSVRC2012_val_00000355.JPEG, 260, 1 1 29 29, train    # Use for traine only, crop pad "1,1,29,29", lable is 260
     ./data/ILSVRC2012_val_00000361.JPEG, 300, , train             # Use for train only, no crop pad, label is 300

