
import sys
import csv
import numpy


def perceptron(Fin, Fout_name):
    weight = numpy.zeros(len(Fin[0]))
    input1 = numpy.insert(Fin, 2, 1, axis=1)
    with open(Fout_name, 'w') as Fout:
        csv_w = csv.writer(Fout, delimiter=',')
        for i in range(1000):
            csv_w.writerow(weight)
            convg = True
            for sample in input1:
                feature = sample[0:-1]
                label = sample[-1]
                if weight.dot(feature) * label <= 0:
                    convg = False
                    weight += label * feature
            if convg:
                break
    return convg


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print "Invalid command."
        exit(1)
    Fin_name = sys.argv[1]
    Fout_name = sys.argv[2]
    out_data = perceptron(numpy.genfromtxt(Fin_name, delimiter=',', dtype=float), Fout_name)
