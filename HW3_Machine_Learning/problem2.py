
import sys
import csv
import numpy
from sklearn import preprocessing


def gradient_descent(in_data, alpha, max_iter):

    feature = in_data[:, :-1]
    label = in_data[:, -1]

    feature = preprocessing.scale(feature)
    feature = numpy.insert(feature, 0, 1, axis=1)

    n = len(label)
    beta = numpy.zeros(len(feature[0]))
    for i in range(max_iter):
        beta -= feature.T.dot((beta.dot(feature.T) - label)) * alpha / n

    loss = beta.dot(feature.T) - label
    cost = sum([i*i for i in loss])/(2*n)
    return beta, cost

if __name__ == '__main__':

    if len(sys.argv) != 3:
        print "Invalid command."
        exit(1)
    Fin_name = sys.argv[1]
    Fout_name = sys.argv[2]
    in_data = numpy.genfromtxt(Fin_name, delimiter=',', dtype=float)
    with open(Fout_name, 'w') as Fout:
        csv_w = csv.writer(Fout, delimiter=',')
        for alpha in (0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1, 5, 10):
            beta, loss = gradient_descent(in_data, alpha, 100)
            csv_w.writerow([alpha, 100] + list(beta))
        best_loss = float('inf')
        for iter in numpy.arange(100, 1000, 10):
            for alpha in numpy.arange(0.1, 2.0, 0.1):
                beta, loss = gradient_descent(in_data, alpha, iter)
                row = [alpha, iter] + list(beta)
                if loss < best_loss:
                    best_loss = loss
                    best_row = row
        csv_w.writerow(best_row)
