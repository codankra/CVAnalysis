import sys
import numpy as np
from PIL import Image, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
import glob
import os
rootdir = os.getcwd()
np.set_printoptions(threshold=sys.maxsize)

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
                image = Image.open(filepath)
                imgList.append(image)
                element = element + 1
    return imgList
# Function to check if each pixel has GT
def checkGT(imgArray, height, width):
    GT = []

    # For every pixel, we check for each image if it is equal to (0,0,0). If any single image is not (Indicating GT exists), 
    # then we append 1 to the array of GT pixels, otherwise we append 0
    for x in range(height):
        for y in range(width):
            exist = 1
            for i in range(len(imgArray)):
                currImage = imgArray[i]
                pixels = currImage.load()
                rgb = pixels[y, x]
                # If the pixel is not (0,0,0) then it exists unless its occluded
                if rgb == (0, 0, 0):
                    exist = 0
                    break
                # Occluded pixels don't exist
                if rgb[2] == 0 and rgb[0] != 0:
                    exist = 0
                    break
            GT.append(exist)
    return GT
# Functon for checking which pixels GT exists for using GT images
def GTCon(img):
    img_size = img.size
    width = img_size[0]
    height = img_size[1]
    GT = []
    for x in range(height):
        for y in range(width):
            exist = 1
            pixels = img.load()
            rgb = pixels[y, x]
            if rgb == 0: 
                exist = 0
            GT.append(exist)
            exist = 0
    return GT
         
def main():
    # Create a Bitmaps directory if it does not exist
    if not os.path.exists("./Bitmaps"):
        os.makedirs("./Bitmaps")
    # Check the if the user input is correct
    if(len(sys.argv) != 2):
        print("ERROR: Usage - py {} Image#".format(sys.argv[0]))
        sys.exit()
    # Get a list of all the images needed and also width/height of the images
    imgList = selectAllImages(sys.argv[1])
    print(sys.argv[1])
    dummyImage = imgList[0]
    img_size = dummyImage.size
    width = img_size[0]
    height = img_size[1]
    # Get a list of all pixels containing GT with checkGT then convert to a numpy array to turn into a grayscaled image
    truthList = checkGT(imgList, height, width)
    truthPixels = np.append([], truthList).astype(np.uint8)
    img = Image.fromarray(truthPixels.reshape(height, width), 'L')
    img.save("./Bitmaps/Bitmap_{}.PBM".format(sys.argv[1]))

    print(len(truthList))
    print(truthList.count(1)/ len(truthList))

if __name__ == "__main__":
    main()