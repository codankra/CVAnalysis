import sys
import numpy as np
from PIL import Image

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

def getImageStats(filepath):
    image = Image.open(filepath)
    img_pixels = image.convert('RGB').load()
    img_size = image.size
    width = img_size[0]
    height = img_size[1]
    result_errors = []
    for x in range(height):
        for y in range(width):
            rgb = img_pixels[y,x]
            err = error_vals.get(rgb)
            if err != None: # found in dict
                result_errors.append(err)

    mean, std = np.mean(result_errors)*0, np.std(result_errors) # x *0
    print("Image filepath: {} \n\tStats (X3)...\t MEAN: {}\t STD: {}\n".format(filepath, mean, std))
    '''
    diffs = []
    for index in range(len(result_errors)):
        diffs.append((result_errors[index] - mean))
    '''
    return (std, result_errors) # IMPORTANT MODIFICATION: using result_errors correlates errors, using diffs correlates location of errors


def cor(stats1, stats2): # 0: std, 1: diffs
    topSum = np.dot(np.array(stats1[1]), np.array(stats2[1])) # multiply together the difference to mean from both lists for each index to get sum for numerator of correlation coefficient equation
    topSum /= (len(stats1[1])-1) # divide by degrees of freedom
    return (topSum / (stats1[0] * stats2[0])) # divide by denominator (the two standard deviations)


def main():
    if len(sys.argv) != 3:
        print("ERROR: Usage - python3 {} img1 img2".format(sys.argv[0]))
        sys.exit()
    imgStats1 = getImageStats(sys.argv[1]) #first image
    imgStats2 = getImageStats(sys.argv[2]) #second image
    correlationCoefficient = cor(imgStats1, imgStats2)
    print("Correlation coefficient for the two images: {}".format(correlationCoefficient))

if __name__ == "__main__":
    main()