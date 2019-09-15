import sys
import csv
import subprocess
import json

# Run the results to generate the csv
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Use Case: python results.py {example.csv} {photo_directory}")
        exit(1)
    with open(sys.argv[1], 'w') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        root_of_photos = sys.argv[2]
        #used a json array instead of read directory name to maintain the order that the output is displayed
        with open('AlgorithmNames.json', 'r') as data_file:
            json_data = data_file.read()
        photos = json.loads(json_data)
        photos.insert(0,'')
        filewriter.writerow(photos)
        for i in range(1,len(photos)):
            row = [photos[i]]
            for j in range(i):
                row.append('')
            for j in range(i+1,len(photos)):
                results = subprocess.check_output("python hello.py " + root_of_photos + photos[i] + " " + root_of_photos + photos[j],shell=True) 
                print(photos[i]," and ",photos[j]," results: ",results.decode('ascii')[:-1])
                row.append(results.decode('ascii')[:-1])
            filewriter.writerow(row)