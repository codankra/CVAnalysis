# This file is pseudocode (while Jason works on the real code) for generating the locations of ground truths for the 2012 error grayscale heatmap correlation algorithm.
import sys
import json
import random
import numpy as np
from PIL import Image, ImageFile
# For now, generate 17 random lists of image length IMG.numPixels
def main():
    data = []
    for index in range(20):
        filepath = 'CVdata/images_2012/AMNet/{}_errors_img.png'.format(index)
        with Image.open(filepath) as curImage:
            img_size = curImage.size[0]*curImage.size[1]
            GTarray = []
            for i in range(img_size):
                GTarray.append(round(random.random()))
            data.append(GTarray)

    with open('GTLists.txt'.format(), 'w') as dest:
        json.dump(data, dest)
                


if __name__ == "__main__":
    main()
