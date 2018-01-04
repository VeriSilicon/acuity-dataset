#!/usr/bin/env python3
from PIL import Image
import cv2 as cv2


def generate_training_picture(image_file_name, label_file_name):
    image_file = open(image_file_name,"rb")
    label_file = open(label_file_name,"rb")

    valfile = open("val.txt","a")
    
    image_data = image_file.read()
    label_data = label_file.read()
    image_filelen = len(image_data)
    image_filenum = int((image_filelen - 16)/28/28)

    jpgImage = Image.new("L",(28,28),0)

    label_filelen = len(label_data)
    label_filenum = int((label_filelen - 8))
    print(type(image_data))
    print("image_filelen = %d , image_filenum = %d" %(image_filelen,image_filenum))
    print("label_filelen = %d , label_filenum = %d" %(label_filelen,label_filenum))
    if label_filenum != label_filenum:
        print("The label and image file don't matched, please double checked")
        image_file.close()
        label_file.close()
        return 
    print("%d" %(image_data[0] << 24 | image_data[1] << 16 | image_data[2] << 8 | image_data[3]))
    print(type(image_filenum))
    i = 0
    while i < image_filenum:
        newfilename = "Lenet_image/Training_lenet_"+str(i)+"_"+str(label_data[8+i])+".jpg"
        val_content = "Lenet_image/Training_lenet_"+str(i)+"_"+str(label_data[8+i])+".jpg" +", "+str(label_data[8+i]) + ", , train"
        print(newfilename)
        Image.Image.putdata(jpgImage,image_data[16+i*28*28:16+(i+1)*28*28])
        valfile.write(val_content+"\n")
        Image.Image.save(jpgImage,newfilename)
        i = i + 1
        #return
    image_file.close()
    label_file.close()
    valfile.close()

def generate_testing_picture(image_file_name, label_file_name):
    image_file = open(image_file_name,"rb")
    label_file = open(label_file_name,"rb")

    valfile = open("val.txt","a")
    
    image_data = image_file.read()
    label_data = label_file.read()
    image_filelen = len(image_data)
    image_filenum = int((image_filelen - 16)/28/28)

    jpgImage = Image.new("L",(28,28),0)

    label_filelen = len(label_data)
    label_filenum = int((label_filelen - 8))
    print(type(image_data))
    print("image_filelen = %d , image_filenum = %d" %(image_filelen,image_filenum))
    print("label_filelen = %d , label_filenum = %d" %(label_filelen,label_filenum))
    if label_filenum != label_filenum:
        print("The label and image file don't matched, please double checked")
        image_file.close()
        label_file.close()
        return 
    print("%d" %(image_data[0] << 24 | image_data[1] << 16 | image_data[2] << 8 | image_data[3]))
    print(type(image_filenum))
    i = 0
    while i < image_filenum:
        newfilename = "Lenet_image/Testing_lenet_"+str(i)+"_"+str(label_data[8+i])+".jpg"
        val_content = "Lenet_image/Testing_lenet_"+str(i)+"_"+str(label_data[8+i])+".jpg" +", "+str(label_data[8+i]) + ", , validate"
        print(newfilename)
        Image.Image.putdata(jpgImage,image_data[16+i*28*28:16+(i+1)*28*28])
        valfile.write(val_content+"\n")
        Image.Image.save(jpgImage,newfilename)
        i = i + 1
        #return
    image_file.close()
    label_file.close()
    valfile.close()
def clear_val_file():
    valfile = open("val.txt","w")
    valfile.close()
if __name__ == "__main__":
     clear_val_file()
    generate_training_picture("train-images.idx3-ubyte","train-labels.idx1-ubyte")
    generate_testing_picture("t10k-images.idx3-ubyte","t10k-labels.idx1-ubyte")
