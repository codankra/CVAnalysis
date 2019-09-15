# CVAnalysis 

### Working with cvlibs images to compare properties of submitted algorithms.

Currently, `hello.py` takes in two error disparity maps (see [CVdata](https://github.com/codankra/CVdata) for example images) and computes the correlation coefficient between the two selected algorithms' errors.

correlation_matrix.csv is the matrix of the correlations on the drive

results.py takes in the name of the csv and the path to the images_2012 folder and produces a csv of the correlations using hello.py