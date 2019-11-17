import sys
import csv

# compare two excel sheets of generated values 
if __name__ == "__main__":
    with open(sys.argv[1]) as f1:
        with open(sys.argv[2]) as f2:
            errors = []
            headers = f1.readline().split(',')
            f2.readline()
            while True:
                line = f1.readline()
                if not line:
                    break
                array1 = line.split(',')
                array2 = f2.readline().split(',')
                for i in range(1,len(array1)):
                    if array1[i]!='' and array2[i]!='':
                        if abs(float(array1[i]) - float(array2[i])) > .001:
                            errors.append(array1[0] + " and " + headers[i])
            for error in errors:
                print (error)
