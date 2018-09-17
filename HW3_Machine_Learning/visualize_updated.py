import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys
from matplotlib import cm
import matplotlib.lines as mlines
from mpl_toolkits.mplot3d import Axes3D
from sklearn import preprocessing


def visualize_scatter(df, feat1=0, feat2=1, labels=2, weights=[-1, -1, 1],
                      title=''):
    """
        Scatter plot feat1 vs feat2.
        Assumes +/- binary labels.
        Plots first and second columns by default.
        Args:
          - df: dataframe with feat1, feat2, and labels
          - feat1: column name of first feature
          - feat2: column name of second feature
          - labels: column name of labels
          - weights: [w1, w2, b]
    """

    # Draw color-coded scatter plot
    colors = pd.Series(['r' if label > 0 else 'b' for label in df[labels]])
    ax = df.plot(x=feat1, y=feat2, kind='scatter', c=colors)

    # Get scatter plot boundaries to define line boundaries
    xmin, xmax = ax.get_xlim()

    # Compute and draw line. ax + by + c = 0  =>  y = -a/b*x - c/b
    a = weights[0]
    b = weights[1]
    c = weights[2]

    def y(x):
        return (-a/b)*x - c/b

    line_start = (xmin, y(xmin))
    line_end = (xmax, y(xmax))
    line = mlines.Line2D(line_start, line_end, color='red')
    ax.add_line(line)


    if title == '':
        title = 'Scatter of feature %s vs %s' %(str(feat1), str(feat2))
    ax.set_title(title)

    plt.show()


def visualize_3d(df, lin_reg_weights=[1,1,1], feat1=0, feat2=1, labels=2,
                 xlim=(-1, 1), ylim=(-1, 1), zlim=(0, 2),
                 alpha=0.005, xlabel='age', ylabel='weight', zlabel='height',
                 title=''):
    """
    3D surface plot.
    Main args:
      - df: dataframe with feat1, feat2, and labels
      - feat1: int/string column name of first feature
      - feat2: int/string column name of second feature
      - labels: int/string column name of labels
      - lin_reg_weights: [b_0, b_1 , b_2] list of float weights in order
    Optional args:
      - x,y,zlim: axes boundaries. Default to -1 to 1 normalized feature values.
      - alpha: step size of this model, for title only
      - x,y,z labels: for display only
      - title: title of plot
    """

    # Setup 3D figure
    ax = plt.figure().gca(projection='3d')
    plt.hold(True)

    # Add scatter plot
    ax.scatter(df[feat1], df[feat2], df[labels])

    # Set axes spacings for age, weight, height
    axes1 = np.arange(xlim[0], xlim[1], step=.05)  # age
    axes2 = np.arange(xlim[0], ylim[1], step=.05)  # weight
    axes1, axes2 = np.meshgrid(axes1, axes2)
    axes3 = np.array( [lin_reg_weights[0] +
                       lin_reg_weights[1]*f1 +
                       lin_reg_weights[2]*f2  # height
                       for f1, f2 in zip(axes1, axes2)])
    plane = ax.plot_surface(axes1, axes2, axes3, cmap=cm.Spectral,
                            antialiased=False, rstride=1, cstride=1)

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_zlabel(zlabel)
    ax.set_xlim3d(xlim)
    ax.set_ylim3d(ylim)
    ax.set_zlim3d(zlim)

    if title == '':
        title = 'LinReg Height with Alpha %f' % alpha
    ax.set_title(title)

    plt.show()


if __name__ == "__main__":

    #======== INPUT1.CSV =======#
    print("Visualizing input1.csv")

    # Import input1.csv, without headers for easier indexing
    data = pd.read_csv('input1.csv', header=None)
    # Note, these weights just happen to look good.
    visualize_scatter(data, weights=[-5.0, -2.0, 39.0])

    # ======== SAMPLE PLOTS =======#
    print('Generating default sample plots.')
    data = np.genfromtxt('input2.csv', delimiter=',', dtype=float)
    feature = data[:,:-1]
    label = data[:,-1]
    feature = preprocessing.scale(feature)
    # Example random data
    print feature[:,0]
    print feature[:,1]
    print label
    data = {'age': feature[:,0],
            'weight': feature[:,1],
            'height': label}
    df = pd.DataFrame(data)
    # Sample scatter plot
    visualize_scatter(df, feat1='age', feat2='weight', labels='height', weights=[0.1286, 0.0014, 1.0964])

    # Sample meshgrid using arbitrary linreg weights
    col_names = list(df)
    bias = 1.1600535598470282e+105
    w1 = -1.3061206571859423e+120
    w2 = -1.3061206571859423e+120
    lin_reg_weights = [bias, w1, w2]

    visualize_3d(df, lin_reg_weights=lin_reg_weights,
                 feat1='age', feat2='weight', labels='height',
                 xlabel=col_names[0], ylabel=col_names[1], zlabel=col_names[2])
