import sys
import numpy as np
import matplotlib.pylab as plt
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

def generateDisparityErrorMap(err_file, heatmap_file):
    errors = Image.open(err_file)
    err_pixels = errors.convert('RGB').load()
    heats = Image.open(heatmap_file)
    disps = heats.convert('L').load()
    img_size = heats.size
    width = img_size[0]
    height = img_size[1]
    disp_err_map = {}
    errCount=0
    disp_map= {}
    # for key in error_vals.keys():
    #     disp_err_map[key] = 0
    #initialize each disparity to 0 errors
    for index in range(256):
        disp_err_map[index] = 0
        disp_map[index] = 0
    for x in range(height): #loop through disparity map
        for y in range(width):
            rgb = err_pixels[y,x]
            disp = disps[y,x]
            err = error_vals.get(rgb) #Get error at this point (same spot in err_map)
            disp_map[disp] = disp_map[disp] + 1
            if(err != None and err>3): # Is there a significant error at this pixel? err != None: found in dict
                disp_err_map[disp] = disp_err_map[disp]+1 #increment error count for current disp
                errCount = errCount + 1
    percentsList = []
    for index in range(256):
        percentsList.append (disp_err_map[index]/(disp_map[index] + .00001))
    return (errCount,disp_err_map, disp_map, percentsList)



def main():
    if len(sys.argv) != 3:
        print("ERROR: Usage - python3 {} errorImg dispImg".format(sys.argv[0]))
        sys.exit()
    stats = generateDisparityErrorMap(sys.argv[1], sys.argv[2])
    print(stats[1])
    print("-------------------")
    print(stats[2])
    print("================")
    print(stats[3])
    print("Total Number of errors: {}".format(stats[0]))
    # percents = sorted(stats[3].items())
    plt.plot(stats[3])
    plt.show()

if __name__ == "__main__":
    main()
