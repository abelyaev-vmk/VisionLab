import subprocess
from skimage.io import imread
from GUI_consts import *


if __name__ == '__main__':
    img = imread('SOURCE-2.jpg')
    height, width = 896 + 20 + 20, 506 + 10 + 110
    newSize = str(height) + "x" + str(width)
    print "--size=" + newSize
    subprocess.call(["python", "GUI.py", "--size=" + newSize])
