import numpy
import pandas
from sklearn.manifold import TSNE
from matplotlib import pyplot as plt
if __name__ == "__main__":
    labels = numpy.array(pandas.read_csv('kitti2015error.csv',skiprows=0))[:,0]
    print(labels)
    my_data = numpy.genfromtxt('kitti2015error.csv', delimiter=',')[1:,1:]
    my_data = 1 - my_data
    for i in range(0,len(my_data[0])):
        for j in range(0,len(my_data[0])):
            if i == j:
                my_data[i][j] = 0
            if j < i:
                my_data[i][j] = my_data[j][i]
    X_embedded = TSNE(n_components=2).fit_transform(my_data)
    colors = [i for i in range(len(labels))]
    print(X_embedded)
    plt.figure(figsize=(10, 5))
    for i in range(len(X_embedded[:,0])):
        x = X_embedded[:,0][i]
        y = X_embedded[:,1][i]
        plt.scatter(x, y)
        plt.text(x+0.5, y+0.5, labels[i], fontsize=12)
    plt.suptitle('2015 Error', fontsize =20)
    plt.show()
