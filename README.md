# CVAnalysis 

### Working with cvlibs images to compare properties of submitted algorithms.

Currently, `correlations.py` takes in two error disparity maps (see [CVdata](https://github.com/codankra/CVdata) for example images) and computes the correlation coefficient between the two selected algorithms' errors.

correlation_matrix.csv is the matrix of the correlations on the drive

generate_csv.py takes in the name of the csv you want and the path to the images_2012 folder and produces a csv of the correlations using hello.py
compare_sheets.py takes the created csv and compares it with another 