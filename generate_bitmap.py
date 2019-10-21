import sys
import numpy as np
from PIL import Image, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
import glob
import os
rootdir = os.getcwd()

# Function to get all the images we want
def selectAllImages(imageNum):
    element = 0
    imgList = []
    # Gets every file in each subdirectory of the parent directory
    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            filepath = subdir + os.sep + file
            # If the file is in the format we want ie. "#_error_img_.png" then we grab it and add it to the array of imges
            if filepath.startswith(subdir + os.sep + str(imageNum) + "_errors_img.png"):
                print (filepath)
                image = Image.open(filepath)
                imgList.append(image)
                element = element + 1
    return imgList
# Function to check if each pixel has GT
def checkGT(imgArray):
    # Dummy image uses the first image to get the width and height of the picture since it is consistent between algorithms
    dummyImage = imgArray[0]
    img_size = dummyImage.size
    width = img_size[0]
    height = img_size[1]
    GT = []
    exist = 0
    # For every pixel, we check for each image if it is equal to (0,0,0). If any single image is not (Indicating GT exists), 
    # then we append 1 to the array of GT pixels, otherwise we append 0
    for x in range(height):
        for y in range(width):
            for i in range(len(imgArray)):
                currImage = imgArray[i]
                pixels = currImage.load()
                rgb = pixels[y, x]
                if rgb != (0,0,0):
                    exist = 1
            GT.append(exist)
    return GT;            

def main():
    imgList = selectAllImages(0)
    truthPixels = checkGT(imgList)
    print(len(truthPixels))
main()