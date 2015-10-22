## Python 2.7.10

import numpy as np
from skimage.io import imread
from skimage.color import rgb2gray
from matplotlib import pyplot
import maxflow


if __name__ == '__main__':
    img1 = rgb2gray(imread("c1.png"))
    img2 = rgb2gray(imread("c2.png"))
    if not all(img1.ravel() > 1):
        img1 *= 255
    if not all(img2.ravel() > 1):
        img2 *= 255
    try:
        assert img1.shape == img2.shape, "Images must be the same size"
    except AssertionError, e:
        raise Exception(e)

    # initialWeight, blackPixelWeight

    nPixels = img1.shape[0] * img2.shape[0]
    # Make new graph
    g = maxflow.GraphFloat()
    # Add nodes as a grid
    nodeids = g.add_grid_nodes(list(img1.shape) + [2])
    # Add edges with initial weight = 1000
    g.add_grid_edges(nodeids, 1000)

    for i in range(nodeids.shape[0]):
        for j in range(nodeids.shape[1]):
            # Add weights to each SOURCE->node and node->SINK edges
            # Weights satisfy the condition that black pixels have less probability to
            # get the final sample than non-black pixels
            g.add_tedge(nodeids[i, j, 0], 1 if img1[i, j] > 10 else 700, 500 - img1[i, j])
            g.add_tedge(nodeids[i, j, 1], 1 if img2[i, j] > 10 else 700, 500 - img2[i, j])
            # Add weight to img1[pixel_number]->img2[pixel_number] edges
            g.add_edge(nodeids[i, j, 0], nodeids[i, j, 1], abs(img1[i, j] - img2[i, j]), abs(img1[i, j] - img2[i, j]))

    # Search for maximum flow path
    g.maxflow()
    sgm = g.get_grid_segments(nodeids)
    # sgm[i] == False if i-th node belongs to the source segment, else sgm[i] == True
    img = np.int_(np.logical_not(sgm[:, :, 1]))

    pyplot.imshow(img)
    pyplot.show()


