import numpy as np
import scipy
from scipy.misc import imread
import maxflow

img = imread("E:\\a2.png")

g = maxflow.Graph[float]()
nodeids = g.add_grid_nodes(img.shape)
g.add_grid_edges(nodeids, 50)
g.add_grid_tedges(nodeids, img, 255-img)
g.maxflow()
sgm = g.get_grid_segments(nodeids)
img2 = np.int_(np.logical_not(sgm))

from matplotlib import pyplot as ppl

ppl.imshow(img2)
ppl.show()

