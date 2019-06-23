import sys
import numpy as np
from PIL import Image

error_vals = { # middle of error range that the rgb value represents
    (49,  54, 149): 0.03125*3.0,
    (69, 117, 180): 0.09375*3.0,
    (116, 173, 209): 0.1875*3.0,
    (171, 217, 233): 0.375*3.0,
    (224, 243, 248): 0.75*3.0,
    (254, 224, 144): 1.5*3.0,
    (253, 174,  97): 3.0*3.0,
    (244, 109,  67): 6.0*3.0,
    (215,  48,  39): 12.0*3.0,
    (165,   0,  38): 24.0*3.0,
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
                # print(err)
                result_errors.append(err)

    mean, std = np.mean(result_errors), np.std(result_errors)
    diffs = []
    for index in range(len(result_errors)):
        diffs.append((result_errors[index] - mean))

    return (std, diffs)


def cor(stats1, stats2): #0: std, 1: diffs
    topSum = 0
    for index in range(len(stats1[1])):
        topSum += stats1[1][index] * stats2[1][index]

    topSum /= (len(stats1[1])-1)
    return (topSum / (stats1[0] * stats2[0]) )


def main():
    # python(3) hello.py algo1 algo2
    if len(sys.argv) != 3: #change to 3
        print("ERROR: Usage - python3 {} img1 img2".format(sys.argv[0]))
        sys.exit()
    img1 = getImageStats(sys.argv[1])
    img2 = getImageStats(sys.argv[2])
    correlationCoefficient = cor(img1, img2)
    print(correlationCoefficient)

if __name__ == "__main__":
    main()