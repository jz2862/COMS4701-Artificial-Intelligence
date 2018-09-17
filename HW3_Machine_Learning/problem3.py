from scipy import misc
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
k = 123


def recreate_image(codebook, labels, w, h):
    image = np.zeros([w, h, 3])
    label_idx = 0
    for i in range(w):
        for j in range(h):
            image[i][j] = codebook[labels[label_idx]]
            label_idx += 1
    return np.array(image, dtype=np.uint8)


if __name__ == '__main__':

    im = np.array(misc.imread('trees.png'), dtype=float)
    w, h, d = im.shape
    image_array = np.reshape(im, (w * h, d))
    kmeans = KMeans(n_clusters=k, random_state=0).fit(image_array)
    labels = kmeans.predict(image_array)
    print kmeans.inertia_
    plt.figure(1)
    plt.clf()
    plt.axis('off')
    plt.title('Original Graph')
    plt.imshow(im/255)

    plt.figure(2)
    plt.clf()
    plt.axis('off')
    plt.title('Kmeans Graph')
    plt.imshow(recreate_image(kmeans.cluster_centers_, labels, w, h)/255.0)
    plt.show()
