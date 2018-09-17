import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D


def visualize_scatter(df, feat1=0, feat2=1, labels=2):
    """
        Scatter plot feat1 vs feat2.
        Assumes +/- binary labels.
        Plots first and second columns by default.
    """
    colors = pd.Series(['r' if label > 0 else 'b' for label in df[labels]])
    ax = df.plot(x=feat1, y=feat2, kind='scatter', c=colors)
    plt.show()


def visualize_3d(df, feat1, feat2, labels, lin_reg_weights,
    xlabel='age', ylabel='weight', zlabel='height'):
    """ 3D surface plot. """

    # Setup 3D figure
    ax = plt.figure().gca(projection='3d')
    plt.hold(True)

    # Add scatter plot
    ax.scatter(df[feat1], df[feat2], df[labels])

    # Set axes spacings for age, weight, height
    axes1 = np.arange(10, step=.1)  # age
    axes2 = np.arange(50, step=.5)  # weight
    axes1, axes2 = np.meshgrid(axes1, axes2)
    axes3 = np.array( [lin_reg_weights[0] + lin_reg_weights[1]*f1 + lin_reg_weights[2]*f2  # height
                       for f1, f2 in zip(axes1, axes2)] )
    plane = ax.plot_surface(axes1, axes2, axes3, cmap=cm.Spectral,
                            antialiased=False, rstride=1, cstride=1)

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_zlabel(zlabel)

    plt.show()


if __name__ == "__main__":

    #======== INPUT1.CSV =======#
    print("Visualizing input1.csv")

    # Import input1.csv, without headers for easier indexing
    data = pd.read_csv('input1.csv', header=None)
    visualize_scatter(data)

    # ======== SAMPLE PLOTS =======#
    print('Generating default sample plots.')

    # Example random data
    data = {'feat1': np.random.rand(50),
            'feat2': np.random.rand(50),
            'labels': np.random.rand(50) > 0.5}
    df = pd.DataFrame(data)

    # Sample scatter plot
    visualize_scatter(df, feat1='feat1', feat2='feat2', labels='labels')

    # Sample meshgrid using arbitrary linreg weights
    labels = list(df)
    bias = np.random.rand() * 0.1
    w1 = np.random.rand()
    w2 = np.random.rand()
    lin_reg_weights = [39.0, -5.0, -2.0]

    visualize_3d(df, 'feat1', 'feat2', 'labels', lin_reg_weights,
                 xlabel=labels[0], ylabel=labels[1], zlabel=labels[2])
