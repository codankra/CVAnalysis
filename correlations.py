import sys
import numpy as np
from PIL import Image, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
import glob

error_vals = { # middle of error range that the rgb value represents
    (49,  54, 149): 0.09375, 
    (69, 117, 180): 0.28125,
    (116, 173, 209): 0.5625,
    (171, 217, 233): 1.125,
    (224, 243, 248): 2.25,
    (254, 224, 144): 4.5,
    (253, 174,  97): 9.0,
    (244, 109,  67): 18.0,
    (215,  48,  39): 36.0,
    (165,   0,  38): 72.0
} 
# ^^ instead of using dict, just get pixel val of grayscale image from nate's program


# for algorithms, take average of 20 image corr coef.
# Main - 2 ver: (correlate errors or disparities)
# cor function is fine and final

# getImageStats is fine for disparities (Nate) - change .get(rgb) to .get(scale[0-255])
# make new function to handle Jason's images (Jason)

def getImageStats2015(filepath):
    image = Image.open(filepath)
    img_pixels = image.convert('RGB').load()
    img_size = image.size
    width = img_size[0]
    height = img_size[1]
    print(height)
    result_errors = []
    for x in range(height):
        for y in range(width):
            rgb = img_pixels[y,x]
            err = error_vals.get(rgb)
            # print(rgb)
            if err != None: # found in dict
                result_errors.append(err)

    mean, std = np.mean(result_errors), np.std(result_errors) # x *0
    # print("Image filepath: {} \n\tStats (X3)...\t MEAN: {}\t STD: {}\n".format(filepath, mean, std))
    
    diffs = []
    for index in range(len(result_errors)):
        diffs.append((result_errors[index] - mean))

    return (std, diffs)

# 2012 version: the error maps are in mostly grayscale so GTLists are needed
def getImageStats(filepath, numTest):
    image = Image.open(filepath)
    img_pixels = image.convert('L').load()
    gtArray = list(Image.open("generators/Bitmaps/Bitmap_{}.PBM".format(numTest)).getdata())
    img_size = image.size
    width = img_size[0]
    height = img_size[1]
    result_errors = []
    for x in range(height):
        for y in range(width):
            if(gtArray[x*y + y]): # ground truth detected at this spot
                # print(img_pixels[y,x])
                result_errors.append(img_pixels[y,x])
    mean, std = np.mean(result_errors), np.std(result_errors) # x *0
    # print("Image filepath: {} \n\tStats (X3)...\t MEAN: {}\t STD: {}\n".format(filepath, mean, std))
    
    diffs = []
    for index in range(len(result_errors)):
        diffs.append((result_errors[index] - mean))

    return (std, diffs)


def getGreyscaleStats(filepath):
    image = Image.open(filepath)
    img_pixels = image.convert('L').load()
    img_size = image.size
    width = img_size[0]
    height = img_size[1]
    result_errors = []
    for x in range(height):
        for y in range(width):
            result_errors.append(img_pixels[y,x])

    mean, std = np.mean(result_errors), np.std(result_errors) # x *0
    # print("Image filepath: {} \n\tStats...\t MEAN: {}\t STD: {}\n".format(filepath, mean, std))
    
    diffs = []
    for index in range(len(result_errors)):
        diffs.append((result_errors[index] - mean))

    return (std, diffs) # IMPORTANT MODIFICATION: using result_errors correlates errors, using diffs correlates location of errors


def cor(stats1, stats2): # 0: std, 1: diffs
    topSum = np.dot(np.array(stats1[1]), np.array(stats2[1])) # multiply together the difference to mean from both lists for each index to get sum for numerator of correlation coefficient equation
    topSum /= (len(stats1[1])-1) # divide by degrees of freedom
    return (topSum / (stats1[0] * stats2[0])) # divide by denominator (the two standard deviations)



def main():
    if len(sys.argv) != 5:
        print("ERROR: Usage - python3 {} type[error/disp] year algorithm1 algorithm2".format(sys.argv[0]))
        sys.exit()

    fileEndingError= "{}/*_errors_img.png"
    fileEndingImg = "{}/*_disp_ipol.png"

    if sys.argv[2] == '2015':
        fileEndingError = "{}/*_errors_disp_img_0.png"
        fileEndingImg2015 = "{}/*_result_disp_img_0.png"

    errorImages1 = glob.glob("{}/*_errors_img_0.png".format(sys.argv[3])) #glob lists images in an arbitrary order that is consistent for similar queries
    errorImages2 = glob.glob("{}/*_errors_img_0.png".format(sys.argv[4])) #so this usage is sketchy but fit for our purposes
    #error images will be used later on, once more steps are done to analyze them
    dispImages1 = glob.glob("{}/*_result_disp_img_0.png".format(sys.argv[3]))
    dispImages2 = glob.glob("{}/*_result_disp_img_0.png".format(sys.argv[4]))
    '''print(errorImages1)
    print(errorImages2)
    print(dispImages1)
    print(dispImages2)'''
    corList = [] * 20
    for index in range(len(dispImages1)): #both globs expected to have same range and order
        # Use next two lines for correlating heatmaps
        imgStats1 = None
        imgStats2 = None
        if (sys.argv[1] == "error" and sys.argv[2] == "2012"):
            numTest = errorImages1[index][errorImages1[index].rfind('/')+1:errorImages1[index].index("_", errorImages1[index].rfind('/'))]
            # Splits image file path between last / and first _ to find #
            imgStats1 = getImageStats(errorImages1[index], numTest)
            imgStats2 = getImageStats(errorImages2[index], numTest)
        elif (sys.argv[1] == "error" and sys.argv[2] == "2015"):
            imgStats1 = getImageStats2015(errorImages1[index])
            imgStats2 = getImageStats2015(errorImages2[index])
        elif (sys.argv[1] == "heat"):
            imgStats1 = getGreyscaleStats(dispImages1[index])
            imgStats2 = getGreyscaleStats(dispImages2[index])
        else:
            print("ERROR: type of images being correlated is unknown: {}".format(sys.argv[1]))
        # print("Correlation coefficient for the two images: {}".format(correlationCoefficient))
        corList.append(cor(imgStats1, imgStats2))
    
    # print(corList)
    print(np.mean(corList))


if __name__ == "__main__":
    main()
